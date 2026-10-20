import asyncio
import time
from agent import route_command_directly, reset_timer, get_or_create_timer

class MockSession:
    def clear_user_turn(self):
        pass

async def test_all():
    session = MockSession()
    
    commands = [
        "open chrome",
        "open notepad",
        "increase volume",
        "set volume to 50",
        "take a screenshot",
        "open downloads",
        "open spotify",
        "close chrome",
        "scroll down",
        "open whatsapp"
    ]
    
    print("Starting local router latency benchmarks...")
    for cmd in commands:
        print(f"\nCommand: '{cmd}'")
        reset_timer()
        timer = get_or_create_timer()
        timer.command = cmd
        timer.t1 = time.time()  # Start turn timer
        timer.t3 = time.time()  # Transcript received
        timer.t4 = time.time()  # Router started
        
        start_time = time.time()
        handled = await route_command_directly(session, cmd)
        duration = time.time() - start_time
        print(f"Direct Match Handled: {handled}")
        
        # Give a small yield to let background tasks run
        await asyncio.sleep(0.2)

if __name__ == "__main__":
    asyncio.run(test_all())
