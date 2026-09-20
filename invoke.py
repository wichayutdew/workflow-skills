#!/usr/bin/env python3
"""Generic harness spawn: Pi agent (delegate_task) + ChatGPT app branch; uses explicit session id."""
import re, sys, json, os, datetime

def get_session_id():
    # Use named session from env or generate timestamp-based id
    return os.environ.get("WORKFLOW_SESSION", "work-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

step_md = sys.argv[1]
agent_name = re.search(r"Agent profile:\s*(\w+)\.md", open(step_md).read()).group(1)
agent_path = f".agents/agents/{agent_name}.md"
agent_cfg = open(agent_path).read()
model = re.search(r"model:\s*(\S+)", agent_cfg).group(1)

session_id = get_session_id()
state_path = f".workflows/state/{session_id}/state.json"

payload = {
    "harness": "pi" if "pi" in sys.argv else "chatgpt",
    "agent_profile": agent_name,
    "agent_config_path": agent_path,
    "model": model,
    "step_md": step_md,
    "agent_config_raw": agent_cfg,
    "step_content": open(step_md).read(),
    "session_id": session_id,
    "session_state_path": state_path,
}

if payload["harness"] == "pi":
    print(f"[PI] Spawn fresh agent: agent={agent_name} model={model} step={step_md} session={session_id}")
else:
    print(f"[CHATGPT] Spawn fresh session: agent={agent_name} model={model} step={step_md} session={session_id}")

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

os.makedirs(os.path.dirname(state_path) if "/" in state_path else ".workflows/state", exist_ok=True)
with open(f".workflows/state/{session_id}-payload.json", "w") as f:
    json.dump(payload, f, indent=2)
print(f"Payload written; session={session_id}; path={state_path}")
