# Sensitive File Read Guard Design

## Goal

Prevent the coding agent from reading common local credential files through the `read_file` tool.

## Scope

- Restrict `read_file` only; ordinary file writing and command checks keep their current behavior.
- Block files named `.env`, files whose names start with `.env.`, and files named `credentials` or `secrets`, case-insensitively.
- Apply the rule after resolving the path, so nested sensitive files are also covered.
- Return a clear guardrail error without opening the file.
- Keep ordinary files such as `config.json` readable.

## Test-first behavior

1. A request to read `.env` is rejected.
2. A request to read a nested `config/.env.production` is rejected.
3. A request to read `config.json` remains allowed.

The existing path-boundary and dangerous-command tests must continue to pass.

## Non-goals

This change does not scan arbitrary file contents for secrets, redact values, or implement an approval UI. Those would require broader policy decisions.
