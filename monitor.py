import time
import os
import json
from datetime import datetime
import openai
import requests
from pynput import keyboard, mouse

openai.api_key = os.getenv("OPENAI_API_KEY")
LOG_FILE = "copilot_log.jsonl"
SIGNAL_FILE = "live_metrics.json"
API_URL = "http://localhost:8000/score_session"  # or your deployed endpoint

def write_live_metrics():
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "keystrokes": keystroke_count,
        "mouse_movement" mouse_movement,
        "idle_seconds": int(time.time() - last_activity),
        "task_alignment_score": last_match_score,
        "task_name": current_task
    }

    # Save locally
    with open(SIGNAL_FILE, "w") as f:
        json.dump(metrics, f)

    # ALSO send to FastAPI
    try:
        res = requests.post(API_URL, json=metrics)
        if res.status_code == 200:
            print(f"✅ Metrics POSTed to API: {res.json()}")
        else:
            print(f"❌ Failed POST: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"⚠️ Error posting metrics: {e}")


last_activity = time.time()
keystroke_count = 0
mouse_movement = 0
current_task = "Investor Dashboard Refactor"
last_match_score = 100  # default to full match

def log_event(event_type, prompt, ai_response, user_response, match_score=None):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "prompt": prompt,
        "ai_response": ai_response,
        "user_response": user_response
    }
    if match_score is not None:
        log_entry["task_alignment_score"] = match_score
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def evaluate_task_alignment():
    global last_match_score
    prompt = f"""
The user is currently assigned to the task: '{current_task}'.

Session details:
- Keystrokes so far: {keystroke_count}
- Mouse movements: {mouse_movement}
- Idle time: {int(time.time() - last_activity)} seconds

Based on this behavior, how well does the user's activity match the assigned task? Give a score from 0 to 100 and a short explanation.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You evaluate session alignment with assigned tasks for productivity scoring."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        message = response["choices"][0]["message"]["content"]
        print(f"🎯 Task Alignment Check:\n{message}")

        # Extract score if present (primitive)
        import re
        score = re.findall(r"(\d{1,3})", message)
        if score:
            last_match_score = min(int(score[0]), 100)

        log_event("task_alignment", prompt, message, "N/A", last_match_score)

    except Exception as e:
        print(f"⚠️ Task alignment check failed: {e}")
        log_event("error", prompt, str(e), "N/A")

def trigger_claude_prompt(task_name=current_task):
    prompt = f"The user appears idle or distracted. Please generate a polite message asking if they are still working on '{task_name}'"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant monitoring productivity sessions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        message = response["choices"][0]["message"]["content"]
        print(f"🤖 Claude says: {message}")

        user_response = input("🧑 Your reply: ")
        log_event("intervention", prompt, message, user_response)

    except Exception as e:
        print(f"⚠️ Claude interaction failed: {e}")
        log_event("error", prompt, str(e), "N/A")

def write_live_metrics():
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "keystrokes": keystroke_count,
        "mouse_movement": mouse_movement,
        "idle_seconds": int(time.time() - last_activity),
        "task_alignment_score": last_match_score
    }
    with open(SIGNAL_FILE, "w") as f:
        json.dump(metrics, f)

def on_key_press(key):
    global keystroke_count, last_activity
    keystroke_count += 1
    last_activity = time.time()

def on_mouse_move(x, y):
    global mouse_movement, last_activity
    mouse_movement += 1
    last_activity = time.time()

def run_monitor():
    print("🚀 AI Copilot running... (task alignment + Claude)")

    kb_listener = keyboard.Listener(on_press=on_key_press)
    ms_listener = mouse.Listener(on_move=on_mouse_move)

    kb_listener.start()
    ms_listener.start()

    while True:
        time.sleep(10)
        evaluate_task_alignment()
        write_live_metrics()

        elapsed = time.time() - last_activity
        if elapsed > 20:
            print("⚠️ User idle detected. Triggering Claude...")
            trigger_claude_prompt(task_name=current_task)
            last_activity = time.time()

if __name__ == "__main__":
    run_monitor()

