import asyncio
import os
from dotenv import load_dotenv
from livekit import api, rtc

async def main():
    load_dotenv()
    url = os.getenv("LIVEKIT_URL")
    key = os.getenv("LIVEKIT_API_KEY")
    secret = os.getenv("LIVEKIT_API_SECRET")
    print(f"URL: {url}")
    print(f"KEY: {key}")
    try:
        token = api.AccessToken(key, secret).with_identity("test-client").with_grants(api.VideoGrants(room_join=True, room="test-room")).to_jwt()
        room = rtc.Room()
        print("Connecting to LiveKit...")
        await room.connect(url, token)
        print("Connected successfully!")
        await room.disconnect()
        print("Disconnected successfully!")
    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    asyncio.run(main())
