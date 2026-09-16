---
trigger: always_on
description: "Load when: scanning changes for exposed keys, credentials, tokens, or personal data prior to committing or deploying."
---
# Workflow: Privacy Check (Vault Guard) v2.0

**Description**: The last line of defense before AI outputs to public files (README, git commit, public logs). Integrated with Privacy Vault (`scripts/privacy_vault.py`).

## Process

### 1. Pre-flight Scan
Gather all text being prepared for output (commit messages, README, public docs, logs).

### 2. Vault Match (3 layers)

**Layer A — Static Index Check:**
Cross-reference against `~/.gemini/memory/vault/secrets-index.yaml`.

**Layer B — Pattern-Based Detection:** *(NEW in v2.0)*
Run regex patterns equivalent to `privacy_vault.py scan`:
- API keys: `api_key|apikey|secret|token|password|private_key`
- Known formats: `sk-*`, `AIza*`, `ghp_*`
- `.env` variable patterns: `KEY=value`

**Layer C — Contextual Check:**
Scan Personal Context marked "NEVER_SHARE" in secrets-index.

### 3. Action Matrix

| Detection | Action |
|-----------|--------|
| API Key / Token | Replace with `<REDACTED_API_KEY>` |
| Password / Secret | Replace with `<REDACTED_SECRET>` |
| Personal Context marked no-share | Rewrite to generic phrasing |
| .env variable value | Replace with `<ENV_VALUE_REDACTED>` |
| Known vendor key format | Replace with `<VENDOR_KEY_REDACTED>` |

### 4. Output
Write safe file. Log action to `logs/privacy-audit.log`.

### 5. Integration *(NEW in v2.0)*
- **Tool**: `python scripts/privacy_vault.py scan <path>` — Scan entire directory before commit
- **Pre-commit hook** (optional): Add to `.git/hooks/pre-commit` for automatic blocking of commits containing secrets
- **Agent rule**: Before any `git add/commit/push` operation, Agent MUST run Privacy Check

