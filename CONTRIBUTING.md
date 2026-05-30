# Contributing

Thank you for your interest in Mendel's Greenhouse.

This project is currently in design phase. Contributions should help clarify the game, reduce ambiguity, or improve future implementation guidance.

## Contribution Process

1. Read [README.md](README.md) for the project overview.
2. Read [AGENTS.md](AGENTS.md) for repository rules.
3. Check the relevant documents in [`specs/`](specs/).
4. Propose changes with clear rationale.
5. Update every affected spec when changing a gameplay rule.

## Gameplay Changes

Gameplay proposals should explain:

- The player problem or design goal.
- The affected system.
- The expected player behavior.
- The educational value.
- Any balance or progression impact.

Do not introduce new species, genes, contracts, rewards, progression gates, or mechanics without updating the appropriate spec.

## Updating Specs

Use this mapping:

- Core rules: `specs/mechanics/gameplay.md`
- Species and genetic content: `specs/content/content-bible.md`
- Contracts: `specs/mechanics/contracts.md`
- Progression and unlocks: `specs/mechanics/progression.md`
- Balance values: `specs/GBD.md`
- Screens and flows: `specs/UI_FLOW.md` and `specs/SCREEN_SPEC.md`
- Collection rules: `specs/mechanics/collection.md`
- Educational goals: `specs/education/learning-objectives.md`
- Conceptual entities: `specs/mechanics/data-model.md`

## Avoiding Inconsistencies

- Keep `specs/` as the source of truth.
- Do not duplicate detailed rules in the root README.
- Search for related terms before changing a rule.
- Keep planned systems distinct from implemented systems.
- Use Pyxel and pixel art as approved direction.
- Treat the current scope as the game only.
- Treat NiceGUI accounts and save management as future scope.
- Do not assume database schema, persistence format, authentication flow, hosting, packaging, or architecture.

## AI-Assisted Contributions

AI tools may be used as engineering assistants, but the human contributor is responsible for the entire contribution.

Requirements:

- Review and understand all AI-assisted changes before submission.
- Disclose meaningful AI assistance with an `Assisted-by:` trailer or PR metadata.
- Do not list AI tools as authors, signers, reviewers, or approvers.
- Do not use AI to bypass required tests, security review, licensing review, or human approval.
- Include prompt summaries or tool summaries when a substantial portion of the contribution was generated.
- Expect additional review for large generated patches, security-sensitive changes, dependency changes, and architecture changes.

Suggested trailer:

```text
Assisted-by: Codex:GPT-5.5
```

## Documentation Style

- Use clear Markdown.
- Prefer concise headings and tables when they improve scanning.
- Write public project documentation in English unless a task explicitly asks otherwise.
- Use the project name **Mendel's Greenhouse** consistently.
