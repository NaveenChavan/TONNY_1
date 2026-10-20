# Tony Architecture

The desktop application has one startup path:

```text
main.py
  -> tony.py
      -> core.runtime_agent.entrypoint
          -> LiveKit session
          -> core.prompts
          -> Tools/* action modules
```

`tony.py` owns the existing PyQt presentation, signal bridge, window lifecycle, and UI callbacks. `core/runtime_agent.py` owns the LiveKit worker, session lifecycle, direct command router, model setup, and tool registration. `core/prompts.py` is the single prompt source and reads persona configuration from environment variables. `Tools/` contains the action implementations and is imported by the runtime agent.

External credentials are supplied through environment variables. Runtime databases, logs, caches, and bytecode are excluded from source control. The LiveKit subdomain in `livekit.toml` is deployment configuration and must match the provisioned LiveKit project.
