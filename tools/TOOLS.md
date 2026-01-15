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

Generate macOS app icons and Safari Extension icons from SVG logos. Single command creates all required PNG files for both macOS applications and Safari Web Extensions.

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
- **macOS icons**: Generates standard and @2x retina PNG variants (16-512px)
- **Safari Extension icons**: Generates web-standard icons (16-384px) for toolbar, menu, and resources
- Creates comprehensive HOWTO.md files for both platforms
- Generates manifest-reference.json for Safari Extension integration
- Configurable via `tools/config.json` (optional)

**Output:**
- `logos/<ProjectName>/generated/macOS/` - macOS app icons
- `logos/<ProjectName>/generated/SafariExtension/` - Safari Extension icons

**Details:** See spec documents:
- [macOS icons spec](Specs/01_GENERATE_FOR_MACOS.md)
- [Safari Extension icons spec](Specs/02_ICON_FOR_WEB_VIEW/02_ICON_FOR_WEB_VIEW.md)

---

### SVG to SwiftUI Assets

Convert SVG files to formats compatible with SwiftUI (PNG @1x/@2x/@3x or PDF).

**Prerequisites:**
```bash
# Install rsvg-convert (part of librsvg)
brew install librsvg
```

**Generate PNG at @1x, @2x, @3x scales:**

```bash
# From the SVG's directory, e.g. logos/TokenExplanation/
SVG_FILE="05_TokenExplained.svg"
BASE_NAME="${SVG_FILE%.svg}"

# @1x (base size - adjust width as needed)
rsvg-convert -w 500 "$SVG_FILE" -o "${BASE_NAME}.png"

# @2x
rsvg-convert -w 1000 "$SVG_FILE" -o "${BASE_NAME}@2x.png"

# @3x
rsvg-convert -w 1500 "$SVG_FILE" -o "${BASE_NAME}@3x.png"
```

**Generate PDF (vector, recommended for SwiftUI):**

```bash
rsvg-convert -f pdf "$SVG_FILE" -o "${BASE_NAME}.pdf"
```

**Using in SwiftUI:**
1. Drag the PNG files (all 3 scales) or PDF into your Xcode Asset Catalog
2. For PNGs: Xcode auto-detects @2x/@3x suffixes
3. For PDF: Set "Preserve Vector Data" in the asset inspector for crisp scaling
4. Reference in SwiftUI: `Image("TokenExplained")`

---

## Future Tools (TODO)

- Web assets: optimized PNGs, favicons, different sizes
