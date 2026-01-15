# How to Add Safari Extension Icons

## Generated Icons for TokenExplanation

Source SVG: `05_TokenExplained.svg`

## Generated Files

- `icon-16.png` - 16x16px
- `icon-19.png` - 19x19px
- `icon-32.png` - 32x32px
- `icon-38.png` - 38x38px
- `icon-48.png` - 48x48px
- `icon-64.png` - 64x64px
- `icon-96.png` - 96x96px
- `icon-128.png` - 128x128px
- `icon-256.png` - 256x256px
- `icon-384.png` - 384x384px
- `icon-512.png` - 512x512px

## Usage in Safari Extension

### For Extension Resources/images/

These icons are used in the Safari Extension's UI (toolbar, menu, popup):

1. Copy the required sizes to your extension's `Resources/images/` directory
2. Reference them in your extension's manifest or code

Common sizes:
- **icon-16.png** - Toolbar icon (normal displays)
- **icon-32.png** - Toolbar icon (retina displays)
- **icon-48.png** - Extension management UI
- **icon-128.png** - Extension gallery and settings

### For App Resources/Icon.png

The **Icon.png** file (384x384) is ready to copy to:
- Main app `Resources/Icon.png`
- Extension preferences/settings display
- Note: This is a copy of icon-384.png for convenience

### Integration Steps

1. **Copy icons to your project:**
   ```
   SafarAI Extension/Resources/images/
   ├── icon-16.png
   ├── icon-19.png
   ├── icon-32.png
   ├── icon-38.png
   ├── icon-48.png
   ├── icon-64.png
   ├── icon-96.png
   ├── icon-128.png
   ├── icon-256.png
   └── icon-512.png

   SafarAI/Resources/
   └── Icon.png (ready to copy - 384x384)
   ```

2. **Update your manifest (if applicable):**
   See `manifest-reference.json` for icon path structure

3. **Reference in code:**
   ```swift
   let icon = NSImage(named: "icon-48")
   ```

### Toolbar Icon SVG

The **toolbar-icon.svg** file is a copy of your source SVG. Depending on your design:
- If your icon works well in Safari's toolbar as-is, use it directly
- If you need a monochrome/outline version for the toolbar, edit this SVG to be black & white
- Safari toolbar typically uses template icons (single color that adapts to light/dark mode)

### Notes

- Safari Extension icons use web naming convention (icon-{size}.png)
- No @2x retina variants needed (size handles both standard and retina)
- All sizes (48-512) are included for different contexts and future compatibility
- These are separate from the AppIcon and LargeIcon in Assets.xcassets
