---
trigger: always_on
description: "Compact index of all rules, workflows, and memory files. Read this INSTEAD of loading individual files."
---
# Rules Manifest (auto-generated 2026-06-28 17:04)

Total files indexed: 0  
Full-load token estimate: ~0 tokens  
Progressive load: read this manifest (~800 tokens), then load individual files on-demand.

## Rules (0 files)

| File | Trigger | Summary |
|------|---------|---------|

## Workflows (0 files)

| File | Trigger | Summary |
|------|---------|---------|

## Skills (0 files)

| File | Trigger | Summary |
|------|---------|---------|

## Agents (0 files)

| File | Trigger | Summary |
|------|---------|---------|

## Memory Files (0 files)

| File | Type | Size |
|------|------|------|

## Loading Protocol

1. At session start: read `session-state.md` + this manifest ONLY.
2. When task arrives, match task keywords against entries above.
3. Load ONLY matching rules/workflows. Never bulk-read all files.
4. If user explicitly says "full load" or "--full", then read all files.
