---
title: Commands
tags:
  - agent-memory/command
type: command
project: mendels-greenhouse
status: active
updated: 2026-05-30
---

# Commands

No build, run, test, or lint commands have been validated yet. The project is currently documentation-first.

Validated documentation checks:

- `git status --short` checks the worktree before staging or commits.
- `rg -n "<term>" README.md AGENTS.md DESIGN.md CONTRIBUTING.md specs` searches for stale references across documentation.
- `Get-ChildItem specs -File | Sort-Object Name | Select-Object -ExpandProperty Name` verifies the specs directory contents on Windows PowerShell.
- A PowerShell Markdown-link scan can validate relative links after moving docs by scanning Markdown link syntax and checking local targets with `Test-Path`.
- `git diff --check` validates staged or unstaged documentation edits for whitespace errors.
- `python --version` confirmed the local Python baseline as Python 3.11.1.
- GitHub CLI was used successfully to make the repository public, add branch protection, and verify final settings.
