# LSCherry — General

**Menu path:** `Add Shader > LSCherry > General`

> 1 node(s) in this category. Socket types, defaults and ranges below are extracted directly from the compiled node source — they are the ground truth.

General-purpose helpers that don't belong to a specific shading stage.

## When to use it

- Feeding scene world/ambient color into a material.

## How to use it

1. Add the node and route its output where a world/ambient color is expected.

## Node reference

### WorldColor Provider

Exposes the scene world/ambient color as a shader input.

**Menu:** `Add Shader > LSCherry > General > WorldColor Provider`

**Inputs**

| Input | Type | Default | Range | Description |
|---|---|---|---|---|
| `Saturation` | Float | 1.2 | 0 – 2 | Scalar value. |
| `Value` | Float | 1.5 | 0 – 2 | Scalar value. |


**Outputs**

| Output | Type | Description |
|---|---|---|
| `Enable WorldColor` | Integer | Color value for this slot. |
| `WorldColor` | Color (RGBA) | Color value for this slot. |
