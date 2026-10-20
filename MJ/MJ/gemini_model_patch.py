# Monkey patch for RealtimeModel to use a model that supports bidiGenerateContent
# and fix protobuf compatibility issues



# Then apply the Gemini model patch
from livekit.plugins.google.beta.realtime import RealtimeModel
import inspect

# Store the original __init__ method
original_init = RealtimeModel.__init__

# Define a new __init__ method that overrides the model name
def patched_init(self, *args, **kwargs):
    # Force the model to use a model that supports bidiGenerateContent
    # Using gemini-2.0-flash-exp which is a valid Live API model for free tier
    kwargs['model'] = 'gemini-2.5-flash-native-audio-preview-12-2025'  # Latest Live API model
    
    # Call the original __init__ method with the modified kwargs
    original_init(self, *args, **kwargs)

# Apply the monkey patch
RealtimeModel.__init__ = patched_init

print("[OK] Monkey patch applied: RealtimeModel now uses 'gemini-2.5-flash-native-audio-preview-12-2025'")