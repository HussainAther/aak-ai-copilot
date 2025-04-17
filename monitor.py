import time
import os
import json
from datetime import datetime
import openai
from pynput import keyboard, mouse

openai.api_key = os.getenv("OPENAI_API_KEY")
LOG_FILE = "copilot_log.jsonl"

last_activity = time.time()

def log_event(event_type, prompt, ai_response, user_response):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "prompt": prompt,
        "ai_response": ai_response,
        "user_response": user_response
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def trigger_claude_prompt(task_name="unknown task"):
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

def on_activity(event=None):
    global last_activity
    last_activity = time.time()

def run_monitor():
    print("🚀 AI Copilot running... (live input and real tracking)")
    
    kb_listener = keyboard.Listener(on_press=on_activity)
    ms_listener = mouse.Listener(on_move=on_activity, on_click=on_activity, on_scroll=on_activity)

    kb_listener.start()
    ms_listener.start()

    while True:
        time.sleep(5)
        elapsed = time.time() - last_activity
        if elapsed > 20:  # change to 1200 in real scenario
            print("⚠️ User idle detected. Triggering Claude...")
            trigger_claude_prompt(task_name="Investor Dashboard Refactor")
            last_activity = time.time()

if __name__ == "__main__":
    run_monitor()

