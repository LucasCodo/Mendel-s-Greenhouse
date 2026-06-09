# Testing Strategy

## Purpose

Mendel's Greenhouse must use `pytest` as the primary automated testing framework.

The testing strategy should make the game safe to implement incrementally by validating:

- Genetic rules.
- Contract generation.
- Progression gates.
- Collection rules.
- Localization behavior.
- UI state transitions where possible.
- Future web/canvas behavior when a browser build exists.

## Research Summary

Current research did not identify a mature, Pyxel-specific pytest plugin. The practical approach is to keep gameplay logic independent from Pyxel rendering and test that logic directly with pytest.

Recommended tooling:

- `pytest` for the core test runner.
- `hypothesis` for property-based tests over genetics, probabilities, and generated contracts.
- `pytest-cov` for coverage reporting.
- `pytest-playwright` for future browser-level tests once the web build is available.

Optional tooling:

- `pytest-xdist` may be added later to parallelize tests if the suite becomes slow.
- `pytest-randomly` may be added later to detect hidden order dependencies.

Do not add a game-specific pytest plugin unless it is actively maintained, relevant to Pyxel, and solves a concrete testing problem.

## Poetry Dev Dependencies

When implementation starts, add the initial test dependencies as development dependencies:

```powershell
poetry add --group dev pytest pytest-cov hypothesis ruff poethepoet Babel
```

Future browser tests may add:

```powershell
poetry add --group dev pytest-playwright
poetry run playwright install
```

Do not add browser testing dependencies until there is a runnable web target to test.

## Test Directory Layout

Recommended structure:

```text
tests/
|-- conftest.py
|-- unit/
|   |-- core/
|   |   |-- test_genetics.py
|   |   |-- test_contracts.py
|   |   |-- test_greenhouse.py
|   |   |-- test_progression.py
|   |   `-- test_i18n.py
|   `-- content/
|       `-- test_content_bible.py
|-- property/
|   |-- test_genetic_invariants.py
|   `-- test_contract_generation_invariants.py
|-- integration/
|   |-- test_crossbreeding_contract_loop.py
|   `-- test_collection_progression_loop.py
`-- browser/
    `-- test_web_smoke.py
```

The `browser/` directory is future scope until the web build exists.

## Pytest Configuration

Use `pyproject.toml` for pytest configuration once the package exists.

Recommended baseline:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-ra --strict-markers --strict-config"
markers = [
  "unit: fast deterministic tests for isolated logic",
  "property: property-based tests using generated inputs",
  "integration: tests that combine multiple game systems",
  "browser: web/canvas tests for the future browser target",
  "slow: tests that are too slow for the default local loop",
]

[tool.coverage.run]
branch = true
source = ["mendels_greenhouse"]
omit = [
  "tests/*",
]

[tool.coverage.report]
show_missing = true
skip_covered = true
fail_under = 0
exclude_lines = [
  "pragma: no cover",
  "if TYPE_CHECKING:",
  "if __name__ == .__main__.:",
]
```

Coverage may be run with:

```powershell
poe test-cov
```

## Testability Rules

- Keep core gameplay rules free of direct Pyxel calls.
- Do not open a Pyxel window in unit tests.
- Inject randomness or pass a seed so crossbreeding tests can be deterministic.
- Keep rendering code thin; test state changes separately from pixel drawing.
- Prefer pure functions for genetics, probability, contract validation, and collection updates.
- Use fixtures for canonical plants, species, contracts, and analyzer levels.
- Use parametrized tests for known Punnett square examples.

## Required MVP Unit Tests

### Genetics

Test that:

- Alleles are inherited correctly from each parent.
- Genotypes are normalized consistently.
- Phenotypes are derived from genotypes according to the content bible.
- Crossbreeding distributions match expected Mendelian outcomes.
- Expected probabilities sum to 100%.
- A generated display batch uses the active cross's combination count when it
  fits the main screen.
- Larger combination counts are capped to a representative visual batch.
- Shuffling offspring order does not change the underlying distribution.

### Contracts

Test that:

- Phenotypic contracts validate matching offspring.
- Delivery contracts consume delivered plants.
- Statistical contracts validate batches without consuming plants.
- Contract generation never creates impossible contracts from undiscovered content.
- Contract rewards follow the balance rules.

### Greenhouse

Test that:

- Initial capacity is 4 slots.
- Maximum capacity is 20 slots.
- Starting plants are `AABB` and `aabb`.
- Storing fails cleanly when the greenhouse is full.
- Harvest sells excess specimens and awards the correct low-value reward.

### Progression

Test that:

- Analyzer level 1 reveals only phenotypes.
- Analyzer level 2 reveals genotypes.
- Analyzer level 3 reveals probabilities.
- Analyzer level 4 enables simulator/planning behavior.
- Contract types unlock only when the analyzer supports them.

### Localization

Test that:

- English and Brazilian Portuguese can be selected.
- Missing translations fall back to English.
- Contract text can be rendered through the localization layer.
- Gameplay state does not depend on display language.

## Property-Based Tests

Use Hypothesis for invariants that are easy to state but hard to exhaust manually.

Required invariants:

- Every generated offspring genotype is valid for its species.
- Every probability distribution sums to exactly 1.0 or 100%, depending on representation.
- No generated contract is impossible under its unlock conditions.
- Analyzer output never reveals information above its level.
- Reordering a generated batch does not change contract validation results unless the contract explicitly depends on order.

Hypothesis tests should use constrained strategies that generate valid species, genes, alleles, and contracts from the official content bible.

## Integration Tests

Integration tests should validate complete gameplay slices without requiring rendering:

1. Accept a phenotypic contract.
2. Select parent plants.
3. Generate a batch.
4. Validate offspring.
5. Store useful plants.
6. Complete the contract.
7. Award rewards.
8. Update collection/progression state.

These tests should run through public game-service APIs rather than internal helper functions once those APIs exist.

## Browser And Visual Tests

Future browser tests should use `pytest-playwright` only after a runnable web build exists.

Initial browser smoke tests should verify:

- The game page loads.
- The Pyxel canvas is visible.
- The canvas is not blank after startup.
- The game fills the browser page while preserving aspect ratio.
- The fullscreen control is present.
- English and Brazilian Portuguese settings can be selected.

Visual regression tests are optional and should not block early MVP work unless the UI becomes unstable.

## Manual Playtest Boundary

Automated tests do not replace manual playtesting.

Manual testing remains required for:

- Game feel.
- Readability of pixel art.
- Perceived pacing.
- Educational clarity.
- Visual feedback quality.

Automated tests should protect rules and regressions; manual tests should judge whether the game feels understandable and engaging.

## Tester Shortcuts

Manual testers may use the `MONEYTREE` tester code to set credits to `999999`
and advance quickly to later species, analyzer levels, and contract tiers.

Rules:

- The shortcut exists for QA speed only.
- It must not change genetics, contract validation, collection completion, or
  unlock rules other than making purchases affordable.
- It should be covered by an automated test so accidental changes are visible.
- It should be reviewed before any production-oriented build or public release.

## Acceptance Criteria

- `pytest` is the default test command.
- Core genetics and contract rules are covered before expanding content.
- Property-based tests exist for genetic invariants before Species 2 is implemented.
- Browser tests are added when a web build exists.
- Tests can run without launching a visible Pyxel window by default.
- Failing tests should identify the broken rule clearly.

## References

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest plugin list](https://docs.pytest.org/en/stable/reference/plugin_list.html)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [Playwright pytest plugin documentation](https://playwright.dev/python/docs/test-runners)
