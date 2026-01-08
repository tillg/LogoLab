#!/usr/bin/env python3
"""
Generate macOS app icons from SVG logos.

This tool converts SVG files to PNG icons at various sizes required for macOS applications.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Optional, Tuple

try:
    import cairosvg
except ImportError:
    print("Error: cairosvg is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)


# Default configuration
DEFAULT_CONFIG = {
    "icon_sizes": [16, 32, 128, 256, 512],
    "generate_retina": True
}


def load_config(tools_dir: Path) -> dict:
    """Load configuration from tools/config.json or use defaults."""
    config_file = tools_dir / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {config_file}, using defaults")
    return DEFAULT_CONFIG


def find_project_root_and_name(start_path: Path) -> Tuple[Path, Optional[str]]:
    """
    Find project root and optionally determine project name.

    Returns:
        Tuple of (project_root, project_name)
        project_name is None if not in logos/<ProjectName>/ directory
    """
    current = start_path.resolve()

    # Check if in logos/<ProjectName>/
    if current.parent.name == 'logos' and current.parent.parent.exists():
        return current.parent.parent, current.name

    # Walk up to find logos/ dir
    while current != current.parent:
        if (current / 'logos').exists():
            return current, None
        current = current.parent

    raise ValueError(
        "Error: Not in a project with logos/ directory.\n"
        "Please run this tool from within your project or specify --project."
    )


def find_latest_svg(directory: Path, specified_svg: Optional[str] = None) -> Path:
    """
    Find the SVG file to use.

    If specified_svg is provided, use that file.
    Otherwise, find the highest numbered NN_*.svg file.
    If multiple files have the same highest number, prompt user to select.
    """
    if specified_svg:
        svg_path = directory / specified_svg
        if not svg_path.exists():
            raise FileNotFoundError(
                f"Error: Specified SVG file not found: {svg_path}\n"
                f"Please check the filename and try again."
            )
        return svg_path

    # Find all numbered SVG files
    pattern = re.compile(r'^(\d+)_.*\.svg$')
    svg_files = []

    for f in directory.glob('*.svg'):
        match = pattern.match(f.name)
        if match:
            svg_files.append((int(match.group(1)), f))

    if not svg_files:
        raise FileNotFoundError(
            f"Error: No numbered SVG files found in {directory}\n"
            f"Expected files matching pattern: NN_*.svg (e.g., 01_logo.svg)"
        )

    # Find highest number
    max_num = max(svg_files, key=lambda x: x[0])[0]
    candidates = [f for num, f in svg_files if num == max_num]

    # If multiple files with same number, prompt user
    if len(candidates) > 1:
        print(f"\nMultiple SVG files found with number {max_num:02d}:")
        for i, f in enumerate(candidates, 1):
            print(f"  {i}. {f.name}")

        while True:
            try:
                choice = input("\nSelect file (enter number): ").strip()
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(candidates):
                    return candidates[choice_idx]
                else:
                    print(f"Please enter a number between 1 and {len(candidates)}")
            except (ValueError, KeyboardInterrupt):
                print("\nOperation cancelled.")
                sys.exit(0)

    return candidates[0]


def generate_png(svg_path: Path, output_path: Path, size: int):
    """Generate PNG from SVG at specified size."""
    try:
        cairosvg.svg2png(
            url=str(svg_path),
            write_to=str(output_path),
            output_width=size,
            output_height=size
        )
    except Exception as e:
        raise RuntimeError(f"Error generating {output_path.name}: {e}")


def generate_icons(svg_path: Path, output_dir: Path, config: dict):
    """
    Generate all required icon sizes from the SVG.

    Creates standard and @2x retina variants.
    """
    icon_sizes = config.get("icon_sizes", DEFAULT_CONFIG["icon_sizes"])
    generate_retina = config.get("generate_retina", DEFAULT_CONFIG["generate_retina"])

    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for size in icon_sizes:
        # Standard size
        filename = f"icon_{size}x{size}.png"
        output_path = output_dir / filename
        print(f"  Generating {filename}...")
        generate_png(svg_path, output_path, size)
        generated_files.append((filename, size, False))

        # Retina @2x size
        if generate_retina:
            retina_size = size * 2
            retina_filename = f"icon_{size}x{size}@2x.png"
            retina_output_path = output_dir / retina_filename
            print(f"  Generating {retina_filename}...")
            generate_png(svg_path, retina_output_path, retina_size)
            generated_files.append((retina_filename, retina_size, True))

    return generated_files


def create_howto(output_dir: Path, generated_files: list, project_name: str, svg_filename: str):
    """Create HOWTO.md with instructions for adding icons to Xcode."""
    howto_content = f"""# How to Add Icons to Xcode Project

## Generated Icons for {project_name}

Source SVG: `{svg_filename}`

## Generated Files

"""

    # Group by base size
    size_groups = {}
    for filename, actual_size, is_retina in generated_files:
        base_size = actual_size // 2 if is_retina else actual_size
        if base_size not in size_groups:
            size_groups[base_size] = []
        size_groups[base_size].append((filename, actual_size, is_retina))

    for base_size in sorted(size_groups.keys()):
        files = size_groups[base_size]
        howto_content += f"### {base_size}x{base_size}\n"
        for filename, actual_size, is_retina in files:
            if is_retina:
                howto_content += f"- `{filename}` - {actual_size}x{actual_size}px (Retina @2x)\n"
            else:
                howto_content += f"- `{filename}` - {actual_size}x{actual_size}px\n"
        howto_content += "\n"

    howto_content += """## Adding Icons to Xcode

### AppIcon (Main App Icon)

1. Open your Xcode project
2. In the Project Navigator, select `Assets.xcassets`
3. Select `AppIcon` in the asset catalog
4. Drag and drop the PNG files into the appropriate slots:
   - 16x16: Use `icon_16x16.png` and `icon_16x16@2x.png`
   - 32x32: Use `icon_32x32.png` and `icon_32x32@2x.png`
   - 128x128: Use `icon_128x128.png` and `icon_128x128@2x.png`
   - 256x256: Use `icon_256x256.png` and `icon_256x256@2x.png`
   - 512x512: Use `icon_512x512.png` and `icon_512x512@2x.png`

### LargeIcon (Safari Web Extension)

For Safari Web Extensions, you also need to fill the **LargeIcon** asset (shown in Safari's Preferences/Extensions panel):

1. In `Assets.xcassets`, select `LargeIcon`
2. Drag and drop:
   - **1x slot**: Use `icon_512x512.png` (or `icon_256x256.png`)
   - **2x slot**: Use `icon_512x512@2x.png` (1024px)
   - **3x slot**: Optional (less common on macOS)

### Troubleshooting

- **Icon not updating**: Clean build folder (Cmd+Shift+K) and rebuild
- **Wrong size displayed**: Verify you're using the correct @2x variants for retina displays
- **Blurry icons**: Make sure you're using both standard and @2x variants

## Notes

- These icons are optimized for macOS applications
- The @2x variants provide sharp display on Retina screens
- Always test your icons at different sizes to ensure they remain clear and recognizable
"""

    howto_path = output_dir / "HOWTO.md"
    with open(howto_path, 'w') as f:
        f.write(howto_content)

    print(f"\n✓ Created {howto_path.name}")


def main():
    """Main entry point for the icon generator."""
    parser = argparse.ArgumentParser(
        description="Generate macOS app icons from SVG logos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect project from current directory (in logos/SafarAI/)
  generate-macos-icons

  # Specify project name
  generate-macos-icons --project SafarAI

  # Specify project and SVG file
  generate-macos-icons --project SafarAI --svg 18_atomic_orbit.svg
        """
    )
    parser.add_argument(
        '--project',
        help='Project name (auto-detected if in logos/<ProjectName>/ directory)'
    )
    parser.add_argument(
        '--svg',
        help='Specific SVG file to use (defaults to highest numbered file)'
    )

    args = parser.parse_args()

    try:
        # Step 1: Find project root and name
        print("🔍 Resolving project...")
        project_root, auto_project_name = find_project_root_and_name(Path.cwd())

        project_name = args.project or auto_project_name
        if not project_name:
            print(
                "Error: Could not auto-detect project name.\n"
                "Please specify project name with --project option."
            )
            sys.exit(1)

        print(f"✓ Project: {project_name}")
        print(f"✓ Project root: {project_root}")

        # Verify project directory exists
        project_dir = project_root / 'logos' / project_name
        if not project_dir.exists():
            print(
                f"Error: Project directory not found: {project_dir}\n"
                f"Please check the project name and try again."
            )
            sys.exit(1)

        # Step 2: Find SVG file
        print("\n🔍 Finding SVG file...")
        svg_path = find_latest_svg(project_dir, args.svg)
        print(f"✓ Using: {svg_path.name}")

        # Step 3: Setup output directories
        print("\n📁 Setting up output directories...")
        generated_dir = project_dir / 'generated'
        macos_dir = generated_dir / 'macOS'
        generated_dir.mkdir(exist_ok=True)
        macos_dir.mkdir(exist_ok=True)

        # Copy source SVG
        dest_svg = generated_dir / svg_path.name
        shutil.copy2(svg_path, dest_svg)
        print(f"✓ Copied {svg_path.name} to generated/")
        print(f"✓ Output directory: {macos_dir}")

        # Step 4: Load configuration
        tools_dir = project_root / 'tools'
        config = load_config(tools_dir)

        # Step 5: Generate icons
        print("\n🎨 Generating PNG icons...")
        generated_files = generate_icons(svg_path, macos_dir, config)
        print(f"✓ Generated {len(generated_files)} icon files")

        # Step 6: Create HOWTO
        print("\n📝 Creating guide...")
        create_howto(macos_dir, generated_files, project_name, svg_path.name)

        print(f"\n✅ Success! Icons generated in:")
        print(f"   {macos_dir}")
        print(f"\nSee {macos_dir / 'HOWTO.md'} for instructions on adding icons to Xcode.")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except (ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
