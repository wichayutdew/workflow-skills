#!/usr/bin/env python3
"""Spawn fresh agent session with embedded sub-skill content + session state handoff."""
import sys, json, os, datetime

def get_session_id():
    return os.environ.get("WORKFLOW_SESSION", "work-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

step_md = sys.argv[1]
content = open(step_md).read()
session_id = get_session_id()
state_path = f".workflows/state/{session_id}/state.json"

# Transition logic: read previous state for back-circling
prev_state_path = state_path
if os.path.exists(prev_state_path):
    try:
        prev_state = json.load(open(prev_state_path))
        if prev_state.get("status") in ("gaps", "back", "invalid"):
            prev_step = prev_state.get("prev_step")
            if prev_step:
                print(f"[TRANSITION] Back-circling to previous step: {prev_step}")
    except Exception:
        pass

payload = {
    "harness": "pi" if "pi" in sys.argv else "chatgpt",
    "step_md": step_md,
    "step_content": content,
    "session_id": session_id,
    "session_state_path": state_path,
}

if payload["harness"] == "pi":
    print(f"[PI] Spawn fresh agent session: step={step_md} session={session_id}")
else:
    print(f"[CHATGPT] Spawn fresh session: step={step_md} session={session_id}")

os.makedirs(os.path.dirname(state_path) if "/" in state_path else ".workflows/state", exist_ok=True)
with open(f".workflows/state/{session_id}-payload.json", "w") as f:
    json.dump(payload, f, indent=2)
print(f"Payload written; session={session_id}; state_path={state_path}")
