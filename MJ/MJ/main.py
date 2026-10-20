import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# CRITICAL FIX: livekit (via agent) MUST be imported BEFORE PyQt5 on Windows
try:
    import agent
    from agent import entrypoint
except Exception as e:
    pass

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

from tony import main

if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        import traceback
        with open("crash.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
