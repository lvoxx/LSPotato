# LSCherry — XTR (External)

**Menu path:** `Add Shader > LSCherry > External`

> 2 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

XTR parallax mapping pair: `Parallax UV` offsets UVs by view direction to fake depth, and `Parallax Combiner` layers the result. Appear under the **External** submenu.

## When to use it

- Fake interior/relief depth (eyes, panels, engravings) without extra geometry.

## How to use it

1. Generate offset UVs with `Parallax UV`, sample your textures with them, then combine.

## Node reference

### XTR: Parallax Combiner

Combines parallax-mapped layers produced from `Parallax UV`.

**Menu:** `Add Shader > LSCherry > External > XTR: Parallax Combiner`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Layer A` | Float | 1 | -10000 – 10000 | Scalar value. |
| `Layer B` | Float | 0.85 | -10000 – 10000 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Parallax` | Float | Scalar value. |

---

### XTR: Parallax UV

Offsets UVs along the view direction to fake surface depth.

**Menu:** `Add Shader > LSCherry > External > XTR: Parallax UV`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `UV Map` | Vector | (0, 0, 0) | -10000 – 10000 | UV coordinates. |
| `Tangent UV` | Vector | (0, 0, 0) | -10000 – 10000 | UV coordinates. |
| `Distance` | Float | 0 | 0 – 100 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Parallax UV` | Vector | UV coordinates. |
