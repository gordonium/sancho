---
name: quarantine-paths
type: registry
lobe: both
description: The legacy folders the quarantine guard fences off (gordon-os-v2, jarvis-v3), and how the guard tells a dispatched subagent from a main thread. Read by _setup/quarantine-guard.py on every tool call; Gordon edits.
sources: ["[gordon 2026-10-01]"]
---
# Quarantine paths

Gordon, 2026-10-01: "You can never read the gordon-os-v2 folder directly, it will infect your brain. It must always be read with a dispatched subagent." [gordon 2026-10-01]

The guard reads the two lists below. One entry per line, in backticks. A folder is fenced at these paths and also wherever a folder of the same name is mounted (a Cowork mount shows the same folder under a different path), so the last part of each path counts as a name on its own.

## Paths
- `~/Sync/Gordonium Enterprises Sync/gordon-os-v2`
- `~/Sync/Gordonium Enterprises Sync/jarvis-v3`
- `~/PhpstormProjects/gordon-os-v2`
- `~/PhpstormProjects/jarvis-v3`

## Discriminator
How the guard recognises a dispatched subagent. One of:
- `agent_id`: the hook input carries an `agent_id` field inside a subagent and not in a main thread. Subagents may use Read, Grep and Glob; Bash is refused for everyone.
- `env`: the fallback when no field tells the two apart. Read, Grep and Glob are refused for everyone; the only way in is a Bash command that starts with `SANCHO_QUARANTINE_READER=1 `, which the `v2-read` skill's subagent prompt sets. Every such read is logged with the first 80 characters of the command.

discriminator: `agent_id`

Status of that setting: taken from Claude Code's documented hook input, not yet confirmed by a capture on this Mac. The first real calls are recorded in `_queue/log/quarantine-probe.log`; see `_design/STATUS.md` (Nerd's replies, 2026-10-01 quarantine guard).

## Refused for everyone, subagents included
Under any fenced folder: anything under `tools/` or `_dmz/`, every `.env*` file, and names that look like credentials (key, secret, token, password, credential, `.pem`, `.age`, `id_rsa` and the like). Also every instruction file by nature [gordon 2026-10-01]: any file or folder with `CLAUDE` in its name in any case (so the renamed `CLAUDE-SAFE-DO-NOT-USE.md` and a `.claude/` folder count), `SKILL.md`, `*.skill`, anything under `hooks/` or `skills/`, `settings*.json`, `*.prompt.md`. This list lives in the guard, not here, so that editing this file cannot open it.
