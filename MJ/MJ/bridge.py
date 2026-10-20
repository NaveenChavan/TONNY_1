# bridge.py
import threading
import asyncio
from typing import Optional
from livekit.agents import AgentSession
from multiprocessing import Queue


class Bridge:
    def __init__(self, gui_to_agent_queue=None, agent_to_gui_queue=None):
        self.gui_to_agent = gui_to_agent_queue or Queue()
        self.agent_to_gui = agent_to_gui_queue or Queue()
        self.lock = threading.Lock()
        self.agent_session: Optional[AgentSession] = None
        self.gui_instance = None

    def send_to_agent(self, message):
        """Send message from GUI to agent (called by GUI thread)"""
        self.gui_to_agent.put(message)

    def send_to_gui(self, message):
        """Send message from Agent to GUI (called by agent thread)"""
        with self.lock:
            self.agent_to_gui.put(message)

    async def process_gui_messages(self):
        """Process messages sent from GUI to agent (runs in async agent loop)"""
        while True:
            try:
                while not self.gui_to_agent.empty():
                    message = self.gui_to_agent.get_nowait()
                    if self.agent_session:
                        await self.agent_session.send_message(message)
            except Exception as e:
                print(f"[Bridge] Error in process_gui_messages: {e}")
            await asyncio.sleep(0.1)

    def process_agent_messages(self):
        """Process messages sent from agent to GUI (polling in main GUI thread)"""
        if not self.gui_instance:
            return
        try:
            while not self.agent_to_gui.empty():
                message = self.agent_to_gui.get_nowait()
                self.gui_instance.add_message("NOVA", message)
        except Exception as e:
            print(f"[Bridge] Error in process_agent_messages: {e}")
