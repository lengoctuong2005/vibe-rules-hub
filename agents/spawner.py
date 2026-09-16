#!/usr/bin/env python3
"""
Subagent Spawner Framework
Spawns isolated subagents to handle heavy reading/review tasks without polluting the main context.
Enforces JSON-only structured output.
"""

import argparse
import json
import os
import sys
import yaml
import urllib.request
import urllib.error
from pathlib import Path

AGENTS_DIR = Path(__file__).parent
CONFIG_PATH = AGENTS_DIR / "subagent_config.yaml"

def load_config():
    if not CONFIG_PATH.exists():
        print(f"[ERROR] Config not found at {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_template(template_rel_path: str) -> str:
    template_path = AGENTS_DIR / template_rel_path
    if not template_path.exists():
        print(f"[ERROR] Template not found at {template_path}")
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")

def gather_files_context(files: list) -> str:
    context = ""
    for file_path in files:
        p = Path(file_path)
        if p.exists() and p.is_file():
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                context += f"\n--- FILE: {file_path} ---\n{content}\n"
            except Exception as e:
                context += f"\n--- FILE: {file_path} (ERROR READING: {e}) ---\n"
        else:
            context += f"\n--- FILE: {file_path} (NOT FOUND) ---\n"
    return context

def call_llm_api(system_prompt: str, user_prompt: str, model: str) -> dict:
    """
    Lightweight fallback caller using REST API if SDK isn't installed.
    Requires GEMINI_API_KEY in environment.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    # Simple mapping for Gemini API
    gemini_model = "gemini-2.5-flash" if "flash" in model.lower() else "gemini-2.5-pro"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}"
    
    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [{
            "parts": [{"text": user_prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text_response)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise ValueError(f"API Error {e.code}: {err_msg}")
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON.")
    except Exception as e:
        raise ValueError(f"Unknown API error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Spawn a subagent for an isolated task.")
    parser.add_argument("--agent", required=True, help="Agent type (e.g., code_reviewer)")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--files", nargs="*", default=[], help="Files to include in context")
    parser.add_argument("--out", help="Output JSON file path")
    args = parser.parse_args()

    config = load_config()
    agent_types = config.get("agents", {})
    
    if args.agent not in agent_types:
        print(f"[ERROR] Unknown agent type '{args.agent}'. Available: {list(agent_types.keys())}")
        sys.exit(1)
        
    agent_config = agent_types[args.agent]
    system_prompt = load_template(agent_config["template"])
    
    # Build user prompt
    user_prompt = f"TASK:\n{args.task}\n\n"
    if args.files:
        user_prompt += "FILES CONTEXT:\n"
        user_prompt += gather_files_context(args.files)
        
    # Attempt to call API
    print(f"[INFO] Spawning subagent: {args.agent} (Model: {agent_config['model']})")
    try:
        result_json = call_llm_api(system_prompt, user_prompt, agent_config["model"])
        
        out_path = args.out if args.out else f"subagent_{args.agent}_result.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result_json, f, indent=2)
            
        print(f"[SUCCESS] Subagent completed task. Result saved to {out_path}")
        # Print a short summary to stdout for the main agent
        print("\n--- Subagent Summary ---")
        print(f"Status: {result_json.get('status', 'unknown')}")
        print(f"Summary: {result_json.get('summary', 'none')}")
        findings = result_json.get("findings", [])
        print(f"Findings: {len(findings)} items")
        sys.exit(0)
        
    except ValueError as e:
        print(f"[WARN] {e}")
        # Dump payload for manual execution or external MCP pickup
        payload_path = AGENTS_DIR / f"payload_{args.agent}.json"
        dump = {
            "agent": args.agent,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "expected_output": "json"
        }
        payload_path.write_text(json.dumps(dump, indent=2), encoding="utf-8")
        print(f"[INFO] Payload dumped to {payload_path}. Please execute externally and provide the JSON result.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Subagent execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
