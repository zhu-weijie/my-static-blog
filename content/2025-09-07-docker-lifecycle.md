```mermaid
stateDiagram-v2
    [*] --> Created: Create
    [*] --> Running: Run
    Created --> Running: Start
    Running --> Paused: Pause
    Paused --> Running: Unpause
    Running --> Stopped: Stop
    Stopped --> Running: Restart
    Stopped --> Deleted: rm
    Created --> Deleted: rm
```
