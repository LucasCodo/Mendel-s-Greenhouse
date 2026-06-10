---
title: Knowledge Component Map
tags:
  - ui/scenes/knowledge
  - ui/components
type: component-map
project: mendels-greenhouse
status: draft
---

# Knowledge Component Map

## Hierarchy

```text
KnowledgeScene
|- SceneShell
|- KnowledgeProgressSummary
|- KnowledgeNodePanel
|  |- KnowledgeStageHeader[]
|  `- KnowledgeConceptNode[]
|- KnowledgeDetailPanel
`- RightNavigationRail
```

## Implementation Notes

- Concept node visibility is gated by analyzer level.
- Locked nodes may show only `Locked` and the required analyzer level.
- Details use localizable educational text from the runtime concept catalog.
- Scene components receive already selected concept data from the scene; they do
  not unlock concepts or modify progression.
