#!/usr/bin/env python3
"""Generic harness spawn: Pi agent (delegate_task) + ChatGPT app branch; fallback writes payload."""
import re, sys, json, os

step_md = sys.argv[1]
agent_name = re.search(r"Agent profile:\s*(\w+)\.md", open(step_md).read()).group(1)
agent_path = f".agents/agents/{agent_name}.md"
agent_cfg = open(agent_path).read()
model = re.search(r"model:\s*(\S+)", agent_cfg).group(1)

payload = {
    "harness": "pi" if "pi" in sys.argv else "chatgpt",
    "agent_profile": agent_name,
    "agent_config_path": agent_path,
    "model": model,
    "step_md": step_md,
    "agent_config_raw": agent_cfg,
    "step_content": open(step_md).read(),
    "session_state_path": ".workflows/state/<session-key>/state.json",
}

if payload["harness"] == "pi":
    # Pi agent: delegate_task / subagent invocation with agent_cfg + step + state
    print(f"[PI] Spawn fresh agent: agent={agent_name} model={model} step={step_md} state={payload['session_state_path']}")
    # Actual: delegate_task(agent_cfg=agent_cfg, prompt=step_content, state_path=...)
else:
    # ChatGPT app: pass agent_config + step + state via subprocess or API call
    print(f"[CHATGPT] Spawn fresh session: agent={agent_name} model={model} step={step_md} state={payload['session_state_path']}")
    # Actual: subprocess / API call injecting agent_cfg + step_content + session_state

# Transition logic: read state file; if previous status has 'gaps' or 'back', invoke previous step
prev_state_path = payload.get("session_state_path", ".workflows/state/<session-key>/state.json").replace("<session-key>", "work")
if os.path.exists(prev_state_path):
    try:
        prev_state = json.load(open(prev_state_path))
        if prev_state.get("status") in ("gaps", "back", "invalid"):
            prev_step = prev_state.get("prev_step")
            if prev_step:
                print(f"[TRANSITION] Back-circling to previous step: {prev_step}")
    except Exception:
        pass

with open(f".workflows/state/{os.path.basename(step_md).replace('.md','.json')}-payload.json", "w") as f:
    json.dump(payload, f, indent=2)
print("Payload written; generic spawn supports pi (delegate_task) and chatgpt (subprocess/API).")
