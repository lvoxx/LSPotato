# 🥔 Potato-LSCherry

<p align="center">
  <a href="" rel="noopener">
 <img width="100%" src="assets/potatoes.jpg" alt="Project Banner"></a>
</p>

> A lightweight Blender add-on for potato-style automation 🍠 — simplify your workflow and focus on creativity.

<p align="center">
  <a href="#">
    <img alt="GitHub Repo Stars" src="https://img.shields.io/github/stars/lvoxx/Potato-LSCherry?style=for-the-badge"/>
  </a>&nbsp;&nbsp;
  <a href="#">
    <img alt="Total Downloads" src="https://img.shields.io/github/downloads/lvoxx/Potato-LSCherry/total.svg?style=for-the-badge"/>
  </a>&nbsp;&nbsp;
  <a href="https://www.blender.org/">
    <img alt="Build for Blender" src="https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white"/>
  </a>&nbsp;&nbsp;
  <a href="https://www.blender.org/">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
  </a>&nbsp;&nbsp;
  <a href="https://opensource.org/license/mit">
    <img alt="License: MIT" src="https://img.shields.io/github/license/lvoxx/Potato-LSCherry?style=for-the-badge"/>
  </a>&nbsp;&nbsp;
</p>

---

## 🚀 Prerequisites

Before getting started, ensure you have the following installed:

- 🖌️ **Blender** → `4.x` or above  
  👉 [Download](https://www.blender.org/download/releases/4-0/)  

- 🐍 **Python** → `3.x` or above (For developers)
  👉 [Download](https://www.python.org/downloads/)  

> [!TIP]  
> Using the latest stable version is recommended for the best compatibility.

---

## 😨 I dont want to read potato code

**Copy one of those to the terminal**

1. Build the addon, then checking \dist folder

```bash
potato package
```

2. Build and install/uninstall the addon based on your Blender version, default 4.3

```bash
potato install 4.x
```

```bash
potato uninstall 4.x
```

3. If you're a dev, "reload" is a combination of UnInstall + Clean + package + Install

```bash
potato reload
```

---

## 🚀 Features

- 🔄 **Automated mesh adjustments**
- 🎨 **Quick material setup**
- 🧩 **Custom utilities for Blender scripting**
- ⚡ **One-click run from Blender or terminal**
- 🛠 **Extensible Python codebase**

---

## 📦 Installation

### 1️⃣ Install as Blender Add-on

1. Download the latest release ZIP from [Releases](https://github.com/lvoxx/Potato-Blender/releases).
2. Open Blender → `Edit` → `Preferences` → `Add-ons` → `Install...`
3. Select the ZIP file → enable **Potato-Blender**.

### 2️⃣ Install via Source (Dev Mode)

```bash
git clone https://github.com/lvoxx/Potato-Blender.git
cd Potato-Blender
```

---

# Developer Section

## Quick Help

```bash
potato help
```

<img width="100%" src="assets/help.png" alt="Potato Help">

## Project Architecture

```mermaid
graph TD
    %% Main Entry Point
    A[Blender Startup] --> B{Addon Installed?}
    B -->|No| C[Install Potato-LSCherry Addon]
    B -->|Yes| D[Load Addon Components]
    C --> D
    
    %% Core Components Loading
    D --> E[Initialize LSCherry Toon Shader]
    D --> F[Load Potato Utilities]
    D --> G[Register UI Panels]
    
    %% LSCherry Toon Shader System
    E --> H[Load Material Libraries]
    H --> I[Game-specific Presets]
    I --> J[HI3 Materials]
    I --> K[Genshin Impact Materials]
    I --> L[Honkai Star Rail Materials]
    I --> M[Other Game Materials]
    
    %% Potato Automation System
    F --> N[Mesh Automation Tools]
    F --> O[Material Setup Utilities]
    F --> P[Custom Scripting Tools]
    
    %% User Interface
    G --> Q[Shader Editor Panel]
    G --> R[Properties Panel]
    G --> S[Tools Panel]
    
    %% Main Workflow
    T[User Selects Object] --> U{Material Exists?}
    U -->|No| V[Create New Material]
    U -->|Yes| W[Edit Existing Material]
    
    V --> X[Apply LSCherry Base Shader]
    W --> X
    X --> Y[Configure Toon Parameters]
    Y --> Z[Select Game-specific Preset]
    Z --> AA[Fine-tune Settings]
    AA --> BB[Preview Result]
    BB --> CC{Satisfied?}
    CC -->|No| Y
    CC -->|Yes| DD[Apply Final Material]
    
    %% Advanced Features
    DD --> EE[Optional: Batch Processing]
    DD --> FF[Optional: Export Settings]
    DD --> GG[Optional: Save as Preset]
    
    %% Error Handling
    BB --> HH{Errors Detected?}
    HH -->|Yes| II[Show Error Messages]
    HH -->|No| CC
    II --> JJ[Suggest Fixes]
    JJ --> Y
    
    %% Background Processes
    subgraph "Background Systems"
        KK[Auto-reload Libraries]
        LL[Mesh Fairing]
        MM[Planar UV Mapping]
        NN[Material Validation]
    end
    
    %% CLI Tools
    subgraph "CLI Tools"
        OO[potato package]
        PP[potato install]
        QQ[potato uninstall]
        RR[potato reload]
    end
    
    style A fill:#e1f5fe
    style DD fill:#c8e6c9
    style HH fill:#ffcdd2
    style EE fill:#fff3e0
    style FF fill:#fff3e0
    style GG fill:#fff3e0
```
