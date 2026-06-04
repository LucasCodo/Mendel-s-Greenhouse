# Implementation Plan - Finalizing the MVP

We analyzed the current project state and determined the requirements needed to achieve a fully featured gameplay MVP. We will implement these systems today.

## Proposed Changes

### 1. Variable Germination Bed Layout (Replaces Conveyor)

We will replace the industrial conveyor belt with a variable soil grid representing the active cross.

- **Visual Grid**: A framed brown soil panel inside the central-lower main screen. Its cell count follows the number of genetic outcome combinations when that count fits on screen.
- **Representative Cap**: If a future cross has more combinations than can fit cleanly, the bed uses a capped representative size instead of overflowing the canvas.
- **Growth Animation**: Unrevealed offspring appear as seeds/dirt. Revealed offspring grow over 30 frames:
  - Age < 15: Seed stage.
  - 15 <= Age < 30: Seedling stage.
  - Age >= 30: Mature plant (pea pod sprite).
- **Selection**: The player can click any cell in the 5x4 grid. The selected cell is highlighted with an accent border, and its details are shown in the bottom "Selected specimen" panel.
- **Contract Highlighting**: Cells matching the current active contract will display a small checkmark icon/indicator and a special green/accent border.
- **Specimen Actions**: The selected specimen details panel will offer:
  - **STORE**: Moves the plant to the greenhouse (if space is available) and removes it from the bed (marking it as empty/harvested).
  - **SELL**: Sells the plant for 2 credits (roughly 10% of contract value per specimen) and removes it from the bed.

### 2. Information Visibility by Analyzer Level

We will restrict genotype, allele, and probability forecasts based on the `analyzer_level`:

- **Level 1**:
  - Hides genotypes (displays `????`) on parent cards, details panels, and the Garden slot viewer.
  - Displays a lock message on the left Analyzer panel: `"ANALYSER L3 REQUIRED"`.
- **Level 2**:
  - Reveals genotypes (e.g. `AaBb`) on parent cards, details panels, and the Garden slot viewer.
  - Keeps the left Analyzer panel locked.
- **Level 3**:
  - Unlocks expected probabilities list and a compact read-only Punnett summary on the left Analyzer panel.
- **Level 4**:
  - Unlocks simulated crosses preview.

### 3. Knowledge Progression Screen

We will add a new "Knowledge" tab in the top navigation bar to display learned genetics concepts.

The best MVP approach is a scoped knowledge progression map rather than a broad skill tree. The screen should look like a tree/map, but its structure should follow the official learning progression:

```text
Phenotype -> Genotype -> Probability -> Genetic Planning
```

This keeps the feature educational instead of turning it into an unrelated upgrade system.

- **Navigation**: Insert a new `Knowledge` navigation item to the top menu (using the `guide` icon at `(0, 64)`, while moving `Collection` to the `seed` icon at `(64, 128)`).
- **Concept Groups**: Display the 12 initial concepts grouped by progression stage:
  - Phenotype: Phenotype, Dominant allele, Recessive allele.
  - Genotype: Allele pair, Genotype, Homozygous, Heterozygous, Allele segregation.
  - Probability: Independent assortment, 9:3:3:1 dihybrid ratio, Genetic probability.
  - Genetic Planning: Genetic planning.
- **Content Detail**: Selecting an unlocked concept displays its detailed Mendelian genetics explanation on the right panel. Concept locks are gated by the current `analyzer_level`.
- **Unlock Sources**: Each concept should record why it unlocked, such as analyzer level, discovery, or contract milestone.
- **No Early Leakage**: Locked concepts must not reveal genotype, allele, or probability details before the relevant analyzer level.

### 4. Profile-Scoped Local Autosave System

We will implement a JSON-based serialization and save service to persist the player's progress.

- **Save Location**: Save files must live under Pyxel's user data directory, not a hardcoded home-directory path.
- **Save Identity**: The save service must address saves by `profile_id` and `slot_id`, even while the MVP exposes only one local autosave slot.
- **Default Local Profile**: Standalone Pyxel runs use a default local profile such as `local`.
- **Future User Isolation**: Future NiceGUI/account integration must pass the authenticated user/profile identity into the save service or backend. A save belonging to one user must never overwrite, load, or expose another user's save.
- **Suggested Local Path Shape**:
  ```text
  pyxel.user_data_dir("LucasCodo", "MendelsGreenhouse")/
  `-- saves/
      `-- local/
          `-- slot-1.json
  ```
- **Auto-Save**: The game state is written after durable gameplay events such as claims, purchases, plant storing, selling, discoveries, and settings changes.
- **Auto-Load**: The launcher asks the save service for the current `profile_id` and `slot_id` and recovers only that scoped save.
- **Schema**: Every save includes `schema_version`, timestamps, profile metadata, greenhouse, collection, progression, contracts, and settings.
- **Atomic Writes**: Write to a temporary file and replace the target save file so a crash cannot leave a partially written save.
- **Tests**: Save/load tests must include profile isolation: loading `profile_a/slot-1.json` must not read or mutate `profile_b/slot-1.json`.

### 5. Verification & Automated Tests

 we will write additional automated tests to verify the correctness of the genetics and game loop:

- **Property-based tests** using `hypothesis` to check Mendelian inheritance invariants.
- **Integration tests** covering the entire loop: selecting parents, crossbreeding, revealing, storing, selling, claiming, and upgrading.
- **Save/Load tests** to confirm state is serialized and restored properly.

---

## Verification Plan

### Automated Tests
- Run `poetry run pytest` to ensure all existing and new unit, integration, and property tests pass.
- Run `poetry run poe check` to confirm formatting, linting, and tests are passing.

### Manual Verification
- Launch the Pyxel game locally via `poetry run poe start`.
- Select parents, perform a cross, observe the Germination Bed growth animation.
- Select different offspring cells, click store, click sell, and claim the contract reward.
- Buy analyzer upgrades and verify that information (genotypes, probabilities) is revealed step-by-step.
- Open the new Knowledge Tree screen and inspect the explanations.
- Relaunch the game and verify that credits and greenhouse slots are successfully loaded.
