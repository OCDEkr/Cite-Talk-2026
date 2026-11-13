#!/usr/bin/env bash
# Offline discovery/Python floor only. Does not execute agents or read their configuration.
# Run with: bash preflight.sh
set -u

if [[ "$(uname -s)" != Linux ]]; then
  printf '%s\n' 'SKIP: Linux/WSL2 preflight requires Linux. Use the platform appendix or offline workbook.'
  exit 2
fi

printf '%s\n' 'Offline Linux discovery; no network, installs, config reads, or agent launches.'
if [[ "$(id -u)" == 0 ]]; then
  printf '%s\n' 'STOP: use a normal lab user rather than root.'
  exit 1
fi

missing=0
for tool in bash python3; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'FOUND: %s\n' "$tool"
  else
    printf 'MISSING: %s\n' "$tool"
    missing=1
  fi
done

if command -v python3 >/dev/null 2>&1; then
  if python3 -I -S -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
    printf '%s\n' 'PASS: Python satisfies workshop floor 3.11+.'
  else
    printf '%s\n' 'MISSING: supported Python 3.11+ runtime; use the text route.'
    missing=1
  fi
fi

for tool in claude codex hermes; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf 'PRESENT ONLY: %s (version, identity, permissions, and inference still unchecked)\n' "$tool"
  else
    printf 'OPTIONAL ABSENT: %s\n' "$tool"
  fi
done

if (( missing )); then
  printf '%s\n' 'USE TEXT ROUTE: script prerequisites incomplete. No repairs were attempted.'
  exit 1
fi
printf '%s\n' 'DISCOVERY COMPLETE: verify fixture and approved disposable environment before script lab.'
printf '%s\n' 'This does not establish WSL2, OS support, sandbox enforcement, provider access, or lab success.'
exit 0
