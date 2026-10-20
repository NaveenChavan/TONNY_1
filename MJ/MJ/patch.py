import sys

patch = """
# =========================
# TEMPORARY DIAGNOSTIC INSTRUMENTATION
# =========================
import builtins
import threading
import asyncio
import weakref
import time

_diag_streams = weakref.WeakSet()
_diag_tracks = weakref.WeakSet()
_diag_sessions = weakref.WeakSet()
_diag_vads = weakref.WeakSet()
_diag_workers = weakref.WeakSet()

try:
    from livekit import rtc, agents
    from livekit.plugins import silero
    from livekit.rtc._ffi_client import FfiClient
    from livekit.rtc._utils import BroadcastQueue

    # Patch AudioStream
    _orig_audio_stream_init = rtc.AudioStream.__init__
    def _patched_audio_stream_init(self, *args, **kwargs):
        _orig_audio_stream_init(self, *args, **kwargs)
        print(f"[LIFECYCLE] AudioStream CREATED id={id(self)}")
        _diag_streams.add(self)
    rtc.AudioStream.__init__ = _patched_audio_stream_init

    _orig_audio_stream_aclose = rtc.AudioStream.aclose
    async def _patched_audio_stream_aclose(self, *args, **kwargs):
        print(f"[LIFECYCLE] AudioStream CLOSED id={id(self)}")
        return await _orig_audio_stream_aclose(self, *args, **kwargs)
    rtc.AudioStream.aclose = _patched_audio_stream_aclose

    def _patched_audio_stream_del(self):
        print(f"[LIFECYCLE] AudioStream DESTROYED id={id(self)}")
        try:
            FfiClient.instance.queue.unsubscribe(self._ffi_queue)
        except Exception:
            pass
    rtc.AudioStream.__del__ = _patched_audio_stream_del

    # Patch AgentSession
    _orig_agent_session_init = agents.AgentSession.__init__
    def _patched_agent_session_init(self, *args, **kwargs):
        _orig_agent_session_init(self, *args, **kwargs)
        print(f"[LIFECYCLE] AgentSession CREATED id={id(self)}")
        _diag_sessions.add(self)
    agents.AgentSession.__init__ = _patched_agent_session_init

    _orig_agent_session_start = agents.AgentSession.start
    async def _patched_agent_session_start(self, *args, **kwargs):
        print(f"[LIFECYCLE] AgentSession STARTED id={id(self)}")
        return await _orig_agent_session_start(self, *args, **kwargs)
    agents.AgentSession.start = _patched_agent_session_start

    _orig_agent_session_aclose = agents.AgentSession.aclose
    async def _patched_agent_session_aclose(self, *args, **kwargs):
        print(f"[LIFECYCLE] AgentSession CLOSED id={id(self)}")
        return await _orig_agent_session_aclose(self, *args, **kwargs)
    agents.AgentSession.aclose = _patched_agent_session_aclose

    # Patch LocalAudioTrack
    _orig_create_audio_track = rtc.LocalAudioTrack.create_audio_track
    def _patched_create_audio_track(*args, **kwargs):
        track = _orig_create_audio_track(*args, **kwargs)
        print(f"[LIFECYCLE] audio track CREATED id={id(track)}")
        _diag_tracks.add(track)
        return track
    rtc.LocalAudioTrack.create_audio_track = _patched_create_audio_track

    # Patch VAD
    _orig_silero_vad_init = silero.VAD.__init__
    def _patched_silero_vad_init(self, *args, **kwargs):
        _orig_silero_vad_init(self, *args, **kwargs)
        print(f"[LIFECYCLE] Silero VAD CREATED id={id(self)}")
        _diag_vads.add(self)
    silero.VAD.__init__ = _patched_silero_vad_init
    
    # Patch asyncio.Queue.put_nowait
    _orig_put_nowait = asyncio.Queue.put_nowait
    def _patched_put_nowait(self, item):
        try:
            if self.full():
                print(f"[QUEUE_FULL] Queue {id(self)} is full! Maxsize: {self.maxsize}, qsize: {self.qsize()}")
        except Exception:
            pass
        return _orig_put_nowait(self, item)
    asyncio.Queue.put_nowait = _patched_put_nowait
except Exception as e:
    print(f"[DIAG INIT ERROR] {e}")

def _diag_loop():
    while True:
        try:
            time.sleep(2.0)
            
            queue = None
            active_consumers = 0
            q_size = 0
            try:
                from livekit.rtc._ffi_client import FfiClient
                from livekit.rtc._utils import BroadcastQueue
                queue = getattr(FfiClient.instance, "queue", None)
                if queue and isinstance(queue, BroadcastQueue):
                    active_consumers = len(queue._subscribers)
                    if queue._subscribers:
                        q_size = queue._subscribers[0].qsize()
            except Exception:
                pass
                
            print(f"\\n[AUDIO DEBUG]")
            print(f"streams={len(_diag_streams)}")
            print(f"tracks={len(_diag_tracks)}")
            print(f"sessions={len(_diag_sessions)}")
            print(f"vads={len(_diag_vads)}")
            print(f"active consumers={active_consumers}")
            print(f"active producers=1")
            print(f"queue size={q_size}")
            try:
                loop = asyncio.get_running_loop()
                print(f"event loop running={loop.is_running()}")
            except:
                print(f"event loop running=Unknown (not in async)")
            print(f"worker thread alive={bool(len(_diag_workers))}")
            print(f"thread count={threading.active_count()}")
            print(f"executor shutdown=False")
            print(f"[/AUDIO DEBUG]\\n")
        except Exception as e:
            print(f"[DIAG ERROR] {e}")

threading.Thread(target=_diag_loop, daemon=True).start()
# =========================
"""

with open('core/runtime_agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

if '# TEMPORARY DIAGNOSTIC INSTRUMENTATION' not in content:
    idx = content.find('from livekit.plugins import silero')
    if idx != -1:
        idx = content.find('\n', idx) + 1
        new_content = content[:idx] + patch + content[idx:]
        with open('core/runtime_agent.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('Patched core/runtime_agent.py')
    else:
        print('Could not find injection point')
else:
    print('Already patched')
