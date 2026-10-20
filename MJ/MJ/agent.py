# =========================
# ENV + CORE IMPORTS
# =========================
from dotenv import load_dotenv
import asyncio
import os
import sys
import time
import json
import socket
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

load_dotenv()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# =========================
# LIVEKIT IMPORTS
# =========================
from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import noise_cancellation

# Gemini realtime (network-safe)
network_available = False
try:
    socket.create_connection(("8.8.8.8", 53), timeout=3)
    from livekit.plugins.google.beta.realtime import RealtimeModel
    network_available = True
except Exception:
    print("[!] Network issue -> Offline fallback mode")

# =========================
# PROMPTS
# =========================
from prompts_mj import (
    AGENT_INSTRUCTION,
    SESSION_INSTRUCTION,
    AGENT_INSTRUCTION_FOR_TOOLS,
)

# =========================
# TOOLS (ALL)
# =========================
from Tools.manage_windows import manage_window, list_windows
from Tools.search_web import search_web
from Tools.send_whatsapp_message import send_whatsapp_message
from Tools.system_power_action import system_power_action
from Tools.type_user_message_auto import type_user_message_auto
from Tools.write_in_notepad import write_in_notepad
from Tools.desktop_control import desktop_control
from Tools.scroll_content import scroll_content
from Tools.code_handler import fix_code_error
from Tools.file_searching import universal_file_opener
from Tools.press_key import press_key, use_smart_clipboard
from Tools.open_app import open_app
from Tools.scan_system_for_viruses import scan_system_for_viruses
from Tools.time_volume_bright import (
    control_screen_brightness,
    control_system_volume,
    get_time_info,
    get_weather,
    get_system_info_deep,
)
from Tools.multi_task import execute_multi_task
from Tools.generate_ai_image import generate_ai_image
from Tools.code_generator import generate_and_type_code, run_file_in_vscode
from Tools.news_provider import get_top_news
from Tools.youtube_videos import play_media
from Tools.reminder import set_reminder, view_reminders, cancel_reminder
from Tools.screen_short import screen_short
from Tools.pdf_reader import process_document_query
from Tools.send_media_whatsapp import send_media_to_whatsapp
from Tools.excel_data_entery  import create_excel_file,save_excel_changes,delete_all_data,move_left,move_up,enter_data_quick,enter_multiple_data_quick,move_down,move_right,delete_current_cell,go_to_cell,toggle_text_bold,select_row_or_column,sort_excel_data,excel_clipboard_action,calculate_sum
from Tools.word_to_pdf  import word_to_pdf,image_to_pdf,excel_to_pdf,ppt_to_pdf,convert_image_format,test_converters
from Tools.create_folder  import create_here
from Tools.create_folder import create_here
from Tools.read_screen_text import read_screen_text
from Tools.camera_analysis import camera_analysis
from Tools.screen_analyzer import analyze_screen
from Tools.image_analysis import analyze_local_image
from Tools.spotify import open_spotify,spotify_next,spotify_previous,spotify_play_song,spotify_play_liked,spotify_pause

# =========================
# MAIN AGENT
# =========================
class UltimateAdvancedNova(Agent):
    def __init__(self):
        self._reminders: Dict[str, Dict[str, Any]] = {}
        self._reminder_task: Optional[asyncio.Task] = None
        self._session: Optional[AgentSession] = None
        self._reminder_counter = 0

        tools = [
            search_web,
            get_time_info,
            open_app,
            get_system_info_deep,
            get_weather,
            manage_window,
            list_windows,
            play_media,
            press_key,
            write_in_notepad,
            desktop_control,
            scroll_content,
            send_whatsapp_message,
            use_smart_clipboard,
            universal_file_opener,
            system_power_action,
            get_top_news,
            execute_multi_task,
            generate_and_type_code,
            run_file_in_vscode,
            screen_short,
            type_user_message_auto,
            scan_system_for_viruses,
            control_system_volume,
            control_screen_brightness,
            generate_ai_image,
            fix_code_error,
            set_reminder,
            view_reminders,
            cancel_reminder,
            process_document_query,
            send_media_to_whatsapp,
            create_excel_file,
                save_excel_changes,
                delete_all_data,
                move_left,
                move_up,
                enter_data_quick,
                enter_multiple_data_quick,
                move_down,
                move_right,
                delete_current_cell,
                go_to_cell,
                toggle_text_bold,
                select_row_or_column,
                sort_excel_data,
                excel_clipboard_action,
                calculate_sum,
                word_to_pdf,
                image_to_pdf,
                excel_to_pdf,
                ppt_to_pdf,
                convert_image_format,
                test_converters,
                create_here,
                read_screen_text,
                camera_analysis,
                analyze_screen,
                analyze_local_image,
                open_spotify,
                spotify_next,
                spotify_previous,
                spotify_play_song,
                spotify_play_liked,
                spotify_pause,
                
        ]

        super().__init__(
            instructions=self._build_instructions(),
            tools=tools,
            llm=self._init_llm(),
        )

        print(f"✅ Nova initialized with {len(tools)} tools")

    def _init_llm(self):
        if network_available:
            return RealtimeModel(
                model="gemini-2.5-flash-native-audio-preview-12-2025",
                voice="Kore",
                temperature=0.9,
                max_output_tokens=1024,
            )
        return None

    def _build_instructions(self):
        return "\n".join([
            AGENT_INSTRUCTION,
            AGENT_INSTRUCTION_FOR_TOOLS,
            "You have access to ALL system, voice, automation and reminder tools.",
            "Use tools aggressively when required.",
        ])

    # =========================
    # REMINDER SYSTEM
    # =========================
    def set_session(self, session: AgentSession):
        self._session = session
        print("🔔 Session linked for reminders")

    def add_reminder(self, text: str, time_: datetime):
        rid = f"rem_{self._reminder_counter}"
        self._reminder_counter += 1

        self._reminders[rid] = {
            "text": text,
            "time": time_,
        }

        if not self._reminder_task or self._reminder_task.done():
            self._reminder_task = asyncio.create_task(self._monitor_reminders())

        return rid

    async def _monitor_reminders(self):
        print("⏰ Reminder monitor running")
        while self._reminders:
            now = datetime.now()
            triggered = []

            for rid, data in self._reminders.items():
                if now >= data["time"]:
                    await self._trigger_reminder(data["text"])
                    triggered.append(rid)

            for rid in triggered:
                self._reminders.pop(rid, None)

            await asyncio.sleep(5)

    async def _trigger_reminder(self, text: str):
        if self._session:
            # removed generate_reply
            print(f"🔔 Reminder sent → {text}")

# =========================
# ENTRYPOINT
# =========================
async def entrypoint(ctx: agents.JobContext):
    print("🚀 Starting Nova...")

    agent = UltimateAdvancedNova()
    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            video_enabled=False,
            # removed bvc
        ),
    )

    agent.set_session(session)

    await ctx.connect()
    # removed generate_reply

    print("🔥 Nova is LIVE & READY")

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("🛑 Nova stopped")

# =========================
# RUNNER
# =========================
if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
