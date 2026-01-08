# Generate fr MacOS APP

This is the workflow i want to support:

- Create a logo in SVG format for a specific project of mine
- The typical path of the different SVG files (including the final version we want to use) is <Project root>/logos/<Project name>/nn_something.svg
- I want to be able call the generation tool from anywhere within my project: from the project root, from /logos/SafarAI, from /tools...
- When calling it from within logos/SafarAI I don't need to pass a project name - it sees where I am
- When calling it from outside that directory i need to pass the project name, i.e. SafarAI
- I might also pass the SVG file that should be used as the starting point. If I don't pass a SVG file name it takes the SVG file with the highhest number in the file name
- The tool creates a sub dir under logos/SafarAI/generated
- Within the generated dir it creates / copies:
  - The SVG file that it uses as a base (copied over with it's original name)
  - a dir "macOS" in which it will place all the generated image files for a macOS Xcode project

---

## Architecture

**Python CLI Tool** - Chosen for excellent SVG/image libraries and maintainability.

---

## Libraries

- **cairosvg** - SVG to PNG conversion with good quality
- **Pillow (PIL)** - PNG manipulation if needed (fallback/resizing)
- **argparse** - CLI argument parsing
- **pathlib** - Cross-platform path handling
- **shutil** - File operations

Install: `pip install cairosvg pillow`

---

## Decisions

1. **Output format**: PNG files with proper naming for drag-and-drop into Xcode + HOWTO.md guide
2. **SVG preprocessing**: Source SVG remains untouched, no automatic adjustments
3. **Duplicate SVG numbers**: Prompt user to select which file (e.g., `18_v1.svg` vs `18_v2.svg`)
4. **Error handling**: Clear error messages with actionable guidance, then exit
5. **No .icns or AppIcon.appiconset generation**: User adds PNGs to Xcode manually via guide

---

## Implementation Approach

### 1. CLI Interface

```bash
# From logos/SafarAI/ (auto-detect project)
generate-macos-icons

# From anywhere (specify project)
generate-macos-icons --project SafarAI

# Specify SVG file
generate-macos-icons --project SafarAI --svg 18_atomic_orbit.svg
```

### 2. Core Logic Flow

**Step 1: Path Resolution**

- Get current working directory
- Walk up directory tree to find project root (contains `logos/` dir)
- If in `logos/<ProjectName>/`, extract project name
- Otherwise require `--project` argument
- Exit with clear error if project not found

**Step 2: SVG Selection**

- If `--svg` provided, use that file
- Otherwise: scan directory for `NN_*.svg` pattern, find highest NN
- If multiple files with same NN (e.g., `18_v1.svg`, `18_v2.svg`), prompt user to select
- Exit with clear error if no SVG files exist

**Step 3: Directory Setup**

- Create `logos/<ProjectName>/generated/` if not exists
- Create `logos/<ProjectName>/generated/macOS/`
- Copy source SVG to `generated/` directory (preserve original filename)

**Step 4: Icon Generation**

- Generate PNG files at required sizes:
  - `icon_16x16.png`, `icon_16x16@2x.png` (32px)
  - `icon_32x32.png`, `icon_32x32@2x.png` (64px)
  - `icon_128x128.png`, `icon_128x128@2x.png` (256px)
  - `icon_256x256.png`, `icon_256x256@2x.png` (512px)
  - `icon_512x512.png`, `icon_512x512@2x.png` (1024px)
- Use cairosvg for SVG→PNG conversion at each size

**Step 5: Generate HOWTO.md**

- Create `HOWTO.md` in `generated/macOS/` directory
- Include instructions for adding icons to Xcode project
- List all generated PNG files with their purposes

### 3. Key Implementation Details

**Finding highest numbered SVG with duplicate handling:**

```python
import re
from pathlib import Path

def find_latest_svg(directory):
    pattern = re.compile(r'^(\d+)_.*\.svg$')
    svg_files = []
    for f in Path(directory).glob('*.svg'):
        match = pattern.match(f.name)
        if match:
            svg_files.append((int(match.group(1)), f))

    if not svg_files:
        return None

    # Find highest number
    max_num = max(svg_files, key=lambda x: x[0])[0]
    candidates = [f for num, f in svg_files if num == max_num]

    # If multiple files with same number, prompt user
    if len(candidates) > 1:
        print(f"Multiple SVG files found with number {max_num}:")
        for i, f in enumerate(candidates, 1):
            print(f"  {i}. {f.name}")
        choice = int(input("Select file (enter number): ")) - 1
        return candidates[choice]

    return candidates[0]
```

**Project detection:**

```python
def find_project_root_and_name(start_path):
    current = Path(start_path).resolve()
    # Check if in logos/<ProjectName>/
    if current.parent.name == 'logos':
        return current.parent.parent, current.name
    # Walk up to find logos/ dir
    while current != current.parent:
        if (current / 'logos').exists():
            return current, None
        current = current.parent
    raise ValueError("Not in a project with logos/ directory")
```

### 4. Configuration

Optional `config.json` in `tools/` directory:

```json
{
  "icon_sizes": [16, 32, 128, 256, 512],
  "generate_retina": true
}
```
