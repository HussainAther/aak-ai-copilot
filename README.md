### 📄 `README.md`

```markdown
# 🤖 AAK AI Copilot

An intelligent session monitor that runs in the background during tracked work sessions. Designed for AAK Telescience to provide real-time nudges, idle detection, and AI-powered feedback using Claude or GPT.

## 🧠 Features

- Background session monitoring
- Idle/inactivity detection
- Window mismatch alerts
- Claude/GPT-powered prompts for guidance
- User response logging for audit trails

## 📦 Stack

- Python
- OpenAI / Claude API
- Optional websocket/CLI integration

## 🚀 Usage

Start the monitor:

```bash
python monitor.py
```

Monitor runs in the background and triggers prompts based on session behavior.

## 🛠️ To-Do

- [ ] Idle detection engine
- [ ] Claude intervention prompt
- [ ] CLI/chat-style response logging
- [ ] Task alignment detection
```

---

### 🧠 `monitor.py`

```python
# monitor.py

import time

def run_monitor():
    print("🚀 AI Copilot running... (simulate idle monitor)")
    last_activity = time.time()

    while True:
        time.sleep(5)
        elapsed = time.time() - last_activity
        if elapsed > 1200:  # 20 minutes
            print("⚠️ User idle for 20+ minutes. Triggering prompt...")
            # TODO: Call Claude or display alert
            last_activity = time.time()  # Reset

if __name__ == "__main__":
    run_monitor()

