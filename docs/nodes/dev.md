# LSCherry — Dev (Experimental / Deprecated)

**Menu path:** `Add Shader > LSCherry > Dev`

> 2 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

Work-in-progress and retired nodes. **Not for production** — experimental nodes may change or break, and deprecated nodes are kept only for opening older files.

## When to use it

- Testing new ideas; loading legacy materials that still reference these groups.

## How to use it

1. Avoid in new materials. Migrate deprecated nodes to their current equivalents.

## Node reference

### Deprecated

Retired node retained only so older files keep opening. Do not use in new work.

**Menu:** `Add Shader > LSCherry > Dev > Deprecated`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Deprecated` | Shader | — | — | Shader stream. |
| `USE NEW NODE BELOW INSTEAD` | Shader | — | — | Shader stream. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Deprecated` | Shader | Shader stream. |
| `USE NEW NODE BELOW INSTEAD` | Shader | Shader stream. |

---

### Experimental

Unstable work-in-progress node; behavior and sockets may change.

**Menu:** `Add Shader > LSCherry > Dev > Experimental`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Unstable` | Shader | — | — | Shader stream. |
| `DO NOT USE FOR PRODUCTION` | Shader | — | — | Shader stream. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Unstable` | Shader | Shader stream. |
| `DO NOT USE FOR PRODUCTION` | Shader | Shader stream. |
