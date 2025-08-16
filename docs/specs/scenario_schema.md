# Scenario YAML Schema (v1)

Scenarios declare tweaks to **scalars**, **parameters**, **sets**, and **equation includes**.
YAML is human-readable and git-friendly.

```yaml
id: BaselineA
description: Raise cap for node A; add new set element B2
edits:
  scalars:
    - name: capA
      value: 3.0
  parameters:
    - name: demand
      keys: [region, year]        # documentation of dimension ordering (optional)
      updates:
        - key: [A, 2025]
          value: 120.0
        - key: [B, 2025]
          value: 95.0
  sets:
    - name: Tech
      add: [B2]
      remove: []
  equations:
    includes:
      - equation_patches/new_constraint.inc
meta:
  author: Rapha
  tags: [paper1, sensitivity]
