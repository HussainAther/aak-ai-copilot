from datetime import datetime, timedelta
from collections import defaultdict

def parse_timestamp(ts):
    return datetime.fromisoformat(ts)

def compute_event_density(events, start_time, end_time):
    duration = (end_time - start_time).total_seconds() / 60  # in minutes
    return round(len(events) / duration, 2) if duration > 0 else 0

def score_session(mouse_clicks, keyboard_data, screenshots, task_blocks):
    all_timestamps = []

    for e in (mouse_clicks or []):
        all_timestamps.append(parse_timestamp(e["timestamp"]))
    for e in (keyboard_data or []):
        all_timestamps.append(parse_timestamp(e["timestamp"]))
    for e in (screenshots or []):
        all_timestamps.append(parse_timestamp(e["timestamp"]))

    if not all_timestamps:
        return {
            "score": 0,
            "reason": "No recorded activity.",
            "density": 0,
            "duration_minutes": 0
        }

    session_start = min(all_timestamps)
    session_end = max(all_timestamps)
    duration = (session_end - session_start).total_seconds() / 60

    density = compute_event_density(mouse_clicks + keyboard_data, session_start, session_end)

    # Basic scoring formula
    score = 50
    if density > 5:
        score += 20
    if len(screenshots) > 3:
        score += 10
    if task_blocks:
        score += 20

    abnormalities = []
    if density > 20:
        abnormalities.append("Unusually high input rate")
    if not task_blocks:
        abnormalities.append("No task assigned during session")

    return {
        "score": min(score, 100),
        "density": density,
        "duration_minutes": round(duration, 2),
        "abnormalities": abnormalities,
        "start_time": session_start.isoformat(),
        "end_time": session_end.isoformat()
    }
