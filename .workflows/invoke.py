#!/usr/bin/env python3
"""Orchestration: reads sub-skill .md, extracts agent profile + model, spawns fresh agent with handoff."""
import re, sys, json, subprocess, os

SKILL_DIR = ".agents/skills"
HANDOFF_DIR = ".workflows/state"

step_md = sys.argv[1]
agent_name = re.search(r"Agent profile:\s*(\w+)\.md", open(step_md).read()).group(1)
agent_path = f".agents/agents/{agent_name}.md"
agent_cfg = open(agent_path).read()
model = re.search(r"model:\s*(\S+)", agent_cfg).group(1)

# Write session-key handoff state; spawn fresh agent session with agent_cfg + step prompt + state file
print(f"Spawning fresh agent: agent={agent_name} model={model} step={step_md} state={HANDOFF_DIR}")
# Actual harness invocation: delegate_task or new session with agent_cfg injected
