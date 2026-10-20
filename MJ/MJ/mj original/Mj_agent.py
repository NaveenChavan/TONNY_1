import asyncio
from livekit import rtc
from livekit.agents.utils import images
import asyncio
from livekit.rtc import VideoBufferType
from typing import Any, List, Optional
from dotenv import load_dotenv
from datetime import datetime
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import noise_cancellation
from livekit.plugins import google
from livekit.agents.llm.chat_context import ChatContext
import numpy as np
import cv2
from collections import deque
import json
import base64
import logging
import time
import asyncio

# From your LiveKit / RTC package
from livekit import rtc
from livekit.rtc import VideoBufferType
import asyncio
from livekit import rtc
from livekit.agents import Agent, get_job_context
from livekit.agents.llm import ImageContent
import base64
from livekit.agents.utils.images import encode, EncodeOptions, ResizeOptions



# Import prompts and tools
from prompts_mj import (
    AGENT_INSTRUCTION,
    SESSION_INSTRUCTION,
    AGENT_INSTRUCTION_FOR_TOOLS
)

from tools import (
    get_weather,
    search_web,
    play_media,
    get_time_info,
    system_power_action,
    manage_window,
    desktop_control,
    list_active_windows,
    manage_window_state,
    get_today_reminder_message_from_db,
    say_reminder,
    send_whatsapp_message,
    write_in_notepad,
    open_app,
    press_key,
    get_system_info,
    type_user_message_auto,
    scan_system_for_viruses,
    control_ac_bulb,
    use_smart_clipboard,
    control_system_volume,
    control_screen_brightness,
    execute_multi_task,
    send_email,
    # analyze_dataset,
    analyze_groundwater_dataset,
    open_app_on_screen,
    use_smart_selector,
    control_media,
    # generate_image_from_prompt
    generate_ai_image,
    generate_ai_video
    # enable_camera_analysis,
    # analyze_visual_scene,
    
    
)



import time
import logging
import os
from logging.handlers import RotatingFileHandler  # For log rotation


load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        import tools
        tools.assistant_instance = self

        self._last_frame_sent = 0
        self._frame_send_interval = 0.5 

        # --- Define Feature Mapping ---
        FEATURE_MAP = {
            "base": [
                search_web,
                get_time_info,
                open_app,
                get_system_info,
            ],
            "premium": [
                search_web,
                get_time_info,
                open_app,
                get_system_info,
                system_power_action,
                get_weather,
                manage_window,
                list_active_windows,
                play_media,
                press_key,
                manage_window_state,
                type_user_message_auto,
            ],
            "elite": [
                search_web,
                get_time_info,
                open_app,
                get_system_info,
                system_power_action,
                get_weather,
                manage_window,
                list_active_windows,
                play_media,
                press_key,
                manage_window_state,
                type_user_message_auto,
                desktop_control,
                scan_system_for_viruses,
                send_whatsapp_message,
                write_in_notepad,
                # send_email,
                # control_ac_bulb, 
                use_smart_clipboard, control_system_volume, control_screen_brightness,execute_multi_task,analyze_groundwater_dataset,open_app_on_screen,
                use_smart_selector,control_media,generate_ai_image
            ],
        }

        # --- Decide Variant (from ENV) ---
        variant = os.getenv("NOVA_VARIANT", "base").lower()
        if variant not in FEATURE_MAP:
            print(f"[WARN] Unknown variant '{variant}', defaulting to Base.")
            variant = "base"

        # --- Initialize Only Allowed Tools ---
        allowed_tools = FEATURE_MAP[variant]
        self._tools = self._initialize_tools(allowed_tools)

        print(f"[INFO] Assistant initialized with variant: {variant} ({len(allowed_tools)} tools)")

        # self._tools = self._initialize_tools([

        #         get_time_info,
        #         open_app,
        #         get_system_info,
        #         system_power_action,
        #         get_weather,
        #         manage_window,
        #         list_active_windows,
        #         play_media,
        #         press_key,
        #         manage_window_state,
        #         type_user_message_auto,
        #         desktop_control,
        #         scan_system_for_viruses,
        #         send_whatsapp_message,
        #         write_in_notepad,
        #         # send_email,
        #         control_ac_bulb, use_smart_clipboard, control_system_volume, control_screen_brightness,execute_multi_task,open_app_on_screen,
        #         use_smart_selector,
        #         control_media
        # ])


        super().__init__(
            instructions=self._build_instructions(),
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.5,
                top_p=0.9,
                
            ),
            tools=self._tools,
        )
        
        # State tracking
        self._last_tool_used: Optional[str] = None
        self._last_tool_success: bool = False
        self._chat_log_path = "chat_log.txt"
 
        self._min_frame_interval: float = 2  # Process one frame every 0.5s (2 FPS max)
        self._max_buffer_size: int = 20        # Store a max of 20 frames (~10 seconds of context)
        self._max_frames_to_send: int = 1      # Send a maximum of 3 frames to the API
        
        # Visual Analysis Runtime State
        self._frame_buffer = deque(maxlen=self._max_buffer_size) # Use deque for efficiency
        self._last_frame_time: float = 0
        self._visual_analysis_enabled: bool = False
        self._is_analyzing: bool = False
        self._last_analysis_time: float = 0  # Track last time analyze_current_scene() was called
        self._analysis_throttle: float = 2.0 
        self._analysis_lock = asyncio.Lock()
        self._latest_frame: Optional[rtc.VideoFrame] = None
        

    async def process_visual_frame(self, video_frame: rtc.VideoFrame):
        """Process incoming video frames and send to realtime session"""
        try:
            # ✅ FIXED: Add frame rate control
            current_time = time.time()
            if current_time - self._last_frame_sent < self._frame_send_interval:
                return
                
            self._last_frame_sent = current_time
            
            print(f"📹 Processing video frame: {video_frame.width}x{video_frame.height}")
            
            # Store the latest frame for potential analysis
            self._latest_frame = video_frame
            
            # Send frame to realtime session if available
            if hasattr(self, '_activity') and self._activity:
                processed_frame = self._prepare_video_frame(video_frame)
                self._activity.push_video(processed_frame)
                print("✅ Frame sent to activity")
                
                # Optional: Add to buffer for analysis
                await self._add_frame_to_buffer(processed_frame)
            else:
                print("❌ No activity available for video frame")
                
        except Exception as e:
            print(f"❌ Video frame processing error: {str(e)}")

    def _prepare_video_frame(self, frame: rtc.VideoFrame) -> rtc.VideoFrame:
        """Ensure video frame is in the correct format for the realtime model"""
        # Convert to RGBA if needed
        if frame.type != VideoBufferType.RGBA:
            # Convert frame data to RGBA
            rgba_data = self._convert_to_rgba(frame)
            return rtc.VideoFrame(
                width=frame.width,
                height=frame.height,
                type=VideoBufferType.RGBA,
                data=rgba_data
            )
        return frame

    def _convert_to_rgba(self, frame: rtc.VideoFrame) -> bytes:
        """Convert frame data to RGBA format"""
        # Implementation depends on your frame type
        if frame.type == VideoBufferType.RGB:
            # Convert RGB to RGBA
            rgb_array = np.frombuffer(frame.data, dtype=np.uint8)
            rgb_array = rgb_array.reshape((frame.height, frame.width, 3))
            rgba_array = np.dstack([rgb_array, np.full((frame.height, frame.width), 255, dtype=np.uint8)])
            return rgba_array.tobytes()
        # Add other conversions as needed
        return frame.data

    async def _add_frame_to_buffer(self, frame: rtc.VideoFrame):
        """Add frame to buffer for potential analysis"""
        current_time = time.time()
        
        # Throttle frame processing
        if current_time - self._last_frame_time < self._min_frame_interval:
            return
            
        self._last_frame_time = current_time
        
        # Add to buffer
        self._frame_buffer.append({
            'frame': frame,
            'timestamp': current_time
        })
        
        # Optionally trigger analysis if enabled
        if self._visual_analysis_enabled and not self._is_analyzing:
            await self._analyze_if_needed()

    
    async def _analyze_if_needed(self):
        """Trigger visual analysis if conditions are met"""
        current_time = time.time()
        
        # Throttle analysis to avoid overwhelming the system
        if current_time - self._last_analysis_time < self._analysis_throttle:
            return
            
        async with self._analysis_lock:
            if self._is_analyzing:
                return
                
            self._is_analyzing = True
            try:
                # Get recent frames for analysis
                recent_frames = list(self._frame_buffer)[-self._max_frames_to_send:]
                if recent_frames:
                    await self._analyze_visual_scene(recent_frames)
            finally:
                self._is_analyzing = False
                self._last_analysis_time = current_time

    async def _analyze_visual_scene(self, frames: list):
        """Analyze visual scene using the LLM"""
        try:
            # Convert frames to base64 for the LLM
            frame_contents = []
            for frame_data in frames:
                frame = frame_data['frame']
                
                # Convert frame to image content
                image_content = await self._frame_to_image_content(frame)
                if image_content:
                    frame_contents.append(image_content)
            
            if frame_contents:
                # Create a chat context with the visual analysis
                visual_context = ChatContext()
                visual_context.add_message(
                    role="system",
                    content="Analyze the visual scene and provide a brief description."
                )
                
                # Add image contents
                for img_content in frame_contents:
                    visual_context.add_message(
                        role="user",
                        content=[img_content]
                    )
                
                # Generate analysis (you might want to modify this based on your LLM capabilities)
                if hasattr(self, '_activity') and self._activity:
                    # Use the activity to generate a response based on visual input
                    await self._activity.generate_reply(
                        chat_ctx=visual_context,
                        instructions="Analyze the visual scene and describe what you see."
                    )
                    
        except Exception as e:
            print(f"Visual analysis error: {str(e)}")

    async def _frame_to_image_content(self, frame: rtc.VideoFrame) -> Optional[ImageContent]:
        """Convert VideoFrame to ImageContent for the LLM"""
        try:
            # Convert frame to base64
            if frame.type == VideoBufferType.RGBA:
                # Convert RGBA to JPEG for smaller size
                rgba_array = np.frombuffer(frame.data, dtype=np.uint8)
                rgba_array = rgba_array.reshape((frame.height, frame.width, 4))
                
                # Convert to RGB (remove alpha channel)
                rgb_array = rgba_array[:, :, :3]
                
                # Encode as JPEG
                success, jpeg_data = cv2.imencode('.jpg', rgb_array)
                if success:
                    base64_data = base64.b64encode(jpeg_data.tobytes()).decode('utf-8')
                    return ImageContent(
                        type="image/jpeg",
                        data=base64_data
                    )
                    
        except Exception as e:
            print(f"Frame conversion error: {str(e)}")
        return None



    


    def _trigger_gui_effect(self):
        # This will be called by the plugin system
        pass  # Implementation in nova_gui.py

    def _initialize_tools(self, tools: List[Any]) -> List[Any]:
        """Validate and initialize tools with proper error handling."""
        validated_tools = []
        for tool in tools:
            try:
                if not callable(tool):
                    raise ValueError(f"Tool {getattr(tool, '__name__', str(tool))} is not callable")
                if not tool.__doc__:
                    print(f"⚠️ Warning: Tool {tool.__name__} missing docstring")
                
                # Add tool description metadata
                tool.metadata = {
                    'description': tool.__doc__.strip() if tool.__doc__ else f"Tool: {tool.__name__}",
                    'last_used': None,
                    'usage_count': 0
                }
                validated_tools.append(tool)
                print(f"✅ Initialized tool: {tool.__name__}")
            except Exception as e:
                print(f"⚠️ Failed to initialize tool {getattr(tool, '__name__', str(tool))}: {str(e)}")
        
        print(f"📋 Total tools initialized: {len(validated_tools)}")
        return validated_tools



    def _build_instructions(self) -> str:
        """Construct the complete instruction set for the agent."""
        tool_descriptions = []
        for tool in self._tools:
            tool_name = tool.__name__
            tool_doc = tool.__doc__ if tool.__doc__ else "No description available"
            tool_descriptions.append(f"- {tool_name}: {tool_doc.strip()}")
        
        available_tools = "\n".join(tool_descriptions)
        
        return "\n".join([
            AGENT_INSTRUCTION,
            SESSION_INSTRUCTION,
            AGENT_INSTRUCTION_FOR_TOOLS,
            "You are a multilingual assistant capable of understanding and responding in multiple languages.",
            f"\nAvailable tools:\n{available_tools}",
            "\nWhen a user request requires tool usage, actively use the appropriate tool and provide feedback about the action taken."
        ])

    async def on_tool_call_start(self, tool_call):
        """Handle tool call start event."""
        print(f"🔧 Starting tool call: {tool_call.function_info.name}")
        self._last_tool_used = tool_call.function_info.name
        return await super().on_tool_call_start(tool_call)

    async def on_tool_call_end(self, tool_call, result):
        """Handle tool call completion."""
        success = result and not isinstance(result, Exception)
        self._last_tool_success = success
        
        print(f"🔧 Tool call completed: {tool_call.function_info.name} - {'✅ Success' if success else '❌ Failed'}")
        if not success and result:
            print(f"   Error: {result}")
        
        return await super().on_tool_call_end(tool_call, result)

    async def on_user_turn_completed(self, turn_ctx, new_message):
        """Handle post-processing after user turn completion."""
        user_message = turn_ctx.user_message.text_content if turn_ctx.user_message else "[no user input]"
        assistant_message = new_message.text_content if new_message else "[no assistant reply]"

        # Log conversation
        print(f"\n🗣️ USER: {user_message}")
        print(f"🤖 ASSISTANT: {assistant_message}")
        await self._log_conversation("User", user_message)
        await self._log_conversation("Assistant", assistant_message)

        # Update tool usage tracking
        if self._last_tool_used:
            for tool in self._tools:
                if tool.__name__ == self._last_tool_used:
                    tool.metadata['last_used'] = datetime.now()
                    tool.metadata['usage_count'] += 1
                    break

        return await super().on_user_turn_completed(turn_ctx, new_message)

    async def _log_conversation(self, sender: str, message: str) -> None:
        """Log conversation to file with proper encoding and error handling."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self._chat_log_path, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {sender}: {message}\n")
        except IOError as e:
            print(f"⚠️ Failed to log conversation: {str(e)}")

    async def _check_reminders(self) -> None:
        """Check and announce any reminders."""
        try:
            # Fix: Add await keyword here since get_today_reminder_message_from_db is async
            reminder_text = await get_today_reminder_message_from_db()
            if reminder_text:
                await say_reminder(reminder_text)
        except Exception as e:
            print(f"⚠️ Failed to check reminders: {str(e)}")


# In your Assistant class

    # In your Assistant class

    async def generate_startup_message(self, session: AgentSession):
        """
        Dynamically constructs startup instructions by combining the base SESSION_INSTRUCTION
        with a summary of the last conversation, then generates a context-aware greeting.
        """
        try:
            # It's good practice to import DB functions inside the method that uses them.
            from nova_db import get_last_n_messages 
            import json # Ensure json is imported

            # Start with the base instructions you've already written.
            final_instructions = SESSION_INSTRUCTION
            
            # Fetch the last 4 messages for context.
            last_messages = get_last_n_messages(n=4)

            if last_messages:
                print("✅ Found recent messages. Adding conversational context to startup instructions.")
                
                # Format the last messages into a clean, readable summary.
                # This handles potential JSON errors gracefully.
                summary_lines = []
                for msg in last_messages:
                    try:
                        content = json.loads(msg[1])[0]
                        summary_lines.append(f"- {msg[0]}: {content}")
                    except (json.JSONDecodeError, IndexError):
                        continue # Skip malformed messages
                
                last_convo_summary = "\n".join(summary_lines)

                # Append the new, dynamic instructions to the existing ones.
                final_instructions = (
                    "\n\n"
                    "🔰 विशेष संदर्भ:\n"
                    "यह हमारी पिछली बातचीत का अंतिम अंश है। कृपया इसका उपयोग करके अपना अभिवादन व्यक्तिगत और प्रासंगिक बनाएं।\n"
                    "उदाहरण: यदि अंतिम संदेश कॉलेज जाने के बारे में था, तो आप कह सकते हैं, 'नमस्कार अंकित सर, कॉलेज से वापस स्वागत है! आपका दिन कैसा रहा?'\n\n"
                    "--- पिछली बातचीत का अंत ---\n"
                    f"{last_convo_summary}\n"
                    "--------------------------"
                )
            else:
                # If there's no history, we don't need to add anything.
                # The base SESSION_INSTRUCTION is sufficient for a first-time greeting.
                print("✅ No message history found. Using standard startup instructions.")

            # Use the final, combined instructions to generate the spoken reply.
            await session.generate_reply(instructions=SESSION_INSTRUCTION)

        except Exception as e:
            print(f"⚠️ Failed to generate startup message: {e}")
            # Fallback to a simple greeting if there's an error.
            await session.generate_reply(instructions="नमस्कार सर, मैं आपकी सेवा में प्रस्तुत हूँ।")








async def entrypoint(ctx: agents.JobContext):
    """Main entry point for the agent with retry logic."""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(1, max_retries + 1):
        try:
            # Create agent first
            agent = Assistant()
            
            # Create session with the agent
            session = AgentSession()

            # Start session with proper configuration
            try:
                await asyncio.wait_for(
                    session.start(
                        room=ctx.room,
                        agent=agent,
                        room_input_options=RoomInputOptions(
                            video_enabled=True,
                            noise_cancellation=noise_cancellation.BVC(),
                        ),
                    ),
                    timeout=30.0
                )
            except asyncio.TimeoutError:
                raise Exception("Connection timeout")
            
            # Connect to the room
            await ctx.connect()
            
            # ==================================================
            # START: MODIFIED BLOCK
            # ==================================================
            
            # Instead of sending a generic instruction, call our new method.
            # This will handle the startup message generation.
            await session.generate_reply(instructions=SESSION_INSTRUCTION)
            
            # ==================================================
            # END: MODIFIED BLOCK
            # ==================================================
            
            # Check for reminders (this can stay here)
            await agent._check_reminders()
            
            print("✅ Agent session started successfully and is now live.")
            break
            
        except Exception as e:
            print(f"❌ Entrypoint failed on attempt {attempt}: {e}")
            if attempt < max_retries:
                await asyncio.sleep(retry_delay)
            else:
                raise  # Re-raise if all retries failed

# async def entrypoint(ctx: agents.JobContext):
#     """Main entry point for the agent"""
#     try:
#         print("🎯 Agent entrypoint starting...")
        
#         # Wait for room to be ready
#         await ctx.connect()
#         print("✅ Connected to LiveKit room")
        
#         # Create VideoSource FIRST
#         from livekit.rtc import VideoSource
#         video_source = VideoSource(640, 480)
#         print("✅ VideoSource created")
        
#         # Create and publish video track
#         video_track = rtc.LocalVideoTrack.create_video_track("camera", video_source)
#         publication = await ctx.room.local_participant.publish_track(video_track)
#         print(f"✅ Camera video track published: {publication.sid}")
        
#         # IMPORTANT: Set video source in GUI BEFORE creating agent
#         print("🔄 Setting video source in GUI...")
#         max_retries = 10
#         for attempt in range(max_retries):
#             try:
#                 import __main__
#                 if hasattr(__main__, 'nova_window'):
#                     # Use QTimer to ensure GUI thread safety
#                     from PyQt5.QtCore import QTimer
#                     from PyQt5.QtWidgets import QApplication
                    
#                     def set_video_track_in_gui():
#                         try:
#                             if (hasattr(__main__.nova_window, 'nova_widget') and 
#                                 hasattr(__main__.nova_window.nova_widget, 'right_panel')):
                                
#                                 __main__.nova_window.nova_widget.right_panel.set_video_track(video_source)
#                                 print("✅ Video source successfully set in GUI right panel")
                                
#                                 # Verify it was set
#                                 if hasattr(__main__.nova_window.nova_widget.right_panel, '_video_source'):
#                                     vs = __main__.nova_window.nova_widget.right_panel._video_source
#                                     print(f"✅ Video source verification: {vs is not None}")
#                                 else:
#                                     print("❌ Video source not found in right panel")
#                             else:
#                                 print("❌ Right panel not accessible")
#                         except Exception as e:
#                             print(f"❌ Error setting video source in GUI: {e}")
                    
#                     # Execute in GUI thread
#                     QTimer.singleShot(0, set_video_track_in_gui)
                    
#                     # Process events to ensure the timer fires
#                     QApplication.processEvents()
#                     await asyncio.sleep(0.5)  # Give time for GUI update
#                     break
                    
#             except Exception as e:
#                 print(f"⚠️ Attempt {attempt + 1} to set video track failed: {e}")
#                 if attempt < max_retries - 1:
#                     await asyncio.sleep(0.5)
#                 else:
#                     print("❌ Failed to set video source in GUI after all retries")
        
#         # Now create agent and session
#         print("🤖 Creating assistant agent...")
#         agent = Assistant()
#         session = AgentSession()
        
#         print("🚀 Starting agent session...")
#         await session.start(
#             room=ctx.room,
#             agent=agent,
#             room_input_options=RoomInputOptions(
#                 video_enabled=True,
#                 noise_cancellation=noise_cancellation.BVC(),
#             ),
#         )
#         print("✅ Session started")
        
#         # Set assistant reference in main window
#         if hasattr(__main__, 'nova_window'):
#             def set_assistant_in_gui():
#                 __main__.nova_window.set_assistant(agent)
#                 print("✅ Assistant reference set in main window")
#             QTimer.singleShot(0, set_assistant_in_gui)
        
#         # Generate startup message
#         print("💬 Generating startup message...")
#         await session.generate_reply(instructions=SESSION_INSTRUCTION)
#         print("✅ Startup message sent")
        
#         print("🎉 Agent is now fully operational with camera!")
        
#         # Send a test frame immediately
#         if video_source:
#             def send_test_frame():
#                 try:
#                     # Create a colored test frame
#                     test_frame_data = np.zeros((480, 640, 4), dtype=np.uint8)
#                     test_frame_data[:, :, 0] = 255  # Blue channel
#                     test_frame_data[:, :, 3] = 255  # Alpha channel
                    
#                     test_frame = rtc.VideoFrame(
#                         width=640,
#                         height=480,
#                         type=VideoBufferType.RGBA,
#                         data=test_frame_data.tobytes()
#                     )
#                     video_source.capture_frame(test_frame)
#                     print("🎨 Test frame sent to LiveKit")
#                 except Exception as e:
#                     print(f"❌ Test frame failed: {e}")
            
#             QTimer.singleShot(1000, send_test_frame)
        
#         # Keep the agent running
#         while True:
#             await asyncio.sleep(1)
            
#     except Exception as e:
#         print(f"❌ Entrypoint error: {e}")
#         import traceback
#         traceback.print_exc()
#         raise

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))