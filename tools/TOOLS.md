# Tools

A collection of tools to create different image files based on SVG logos.

## Setup

### 1. Install System Dependencies

**macOS:**
```bash
brew install cairo
```

### 2. Setup Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Available Tools

### generate-macos-icons

Generate macOS app icons from SVG logos. Creates PNG files at all required sizes (16-512px) with @2x retina variants.

**Usage:**

```bash
# From within logos/<ProjectName>/ directory (auto-detects project)
./tools/generate-macos-icons

# From anywhere, specify project name
./tools/generate-macos-icons --project SafarAI

# Specify a particular SVG file
./tools/generate-macos-icons --project SafarAI --svg 18_atomic_orbit.svg
```

**Features:**

- Auto-detects project when run from `logos/<ProjectName>/` directory
- Automatically selects highest numbered SVG file (e.g., `18_*.svg` over `17_*.svg`)
- Prompts for selection when multiple SVGs have the same number
- Generates standard and @2x retina PNG variants
- Creates comprehensive HOWTO.md with Xcode integration instructions
- Configurable via `tools/config.json` (optional)

**Output:** `logos/<ProjectName>/generated/macOS/`

**Details:** See [spec document](Specs/01_GENERATE_FOR_MACOS.md) for implementation details.

---

## Future Tools (TODO)

- Web assets: optimized PNGs, favicons, different sizes
