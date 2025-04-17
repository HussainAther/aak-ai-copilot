### 📄 `aak-ai-copilot/README.md`

```markdown
# 🤖 AAK AI Copilot

The **AAK AI Copilot** is a real-time productivity assistant designed for tracked sessions at AAK Telescience. It silently monitors keyboard and mouse activity, tracks session behavior, and uses Claude (or OpenAI GPT) to:

- Detect idle periods and prompt users
- Score how well a user is sticking to their assigned task
- Log all interactions for auditing, review, or reporting

---

## 📦 Features

### 🧠 Intelligent Session Monitoring
- Keystroke and mouse tracking via `pynput`
- Idle time detection (triggered after 20+ seconds by default)

### 💬 Claude-Powered Guidance
- Sends session data to Claude to get alignment feedback
- Evaluates whether user behavior matches their assigned task

### 🧾 Logging + Integration
- Real-time logs written to `copilot_log.jsonl`
- Broadcasts live session signals to `live_metrics.json`
- Easily consumed by `aak-ui-overlay` HUD

---

## 🚀 Usage

### 1. Clone and install dependencies

```bash
git clone https://github.com/YOURORG/aak-ai-copilot.git
cd aak-ai-copilot
pip install -r requirements.txt
```

### 2. Add your OpenAI API key

Create a `.env` file or export it in terminal:

```bash
export OPENAI_API_KEY=your-key-here
```

### 3. Run the copilot monitor

```bash
python monitor.py
```

You’ll see terminal updates with:
- Claude prompts
- Idle detection
- Task alignment scores

---

## 🧪 File Outputs

| File | Description |
|------|-------------|
| `live_metrics.json` | JSON file with live metrics (used by HUD) |
| `copilot_log.jsonl` | Line-by-line session logs with Claude responses |

---

## 🛠 Planned Features

- Websocket broadcast for real-time dashboards
- GUI input or Streamlit-based user replies
- Smart tag generation from session behavior
- Grant/project linking based on activity

---

Built by the AI team at **AAK Telescience**  
> Bridging researchers, investors, and the future of human-computer interaction.
