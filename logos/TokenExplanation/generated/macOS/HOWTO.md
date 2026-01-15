# How to Add Icons to Xcode Project

## Generated Icons for TokenExplanation

Source SVG: `05_TokenExplained.svg`

## Generated Files

### 16x16
- `icon_16x16.png` - 16x16px
- `icon_16x16@2x.png` - 32x32px (Retina @2x)

### 32x32
- `icon_32x32.png` - 32x32px
- `icon_32x32@2x.png` - 64x64px (Retina @2x)

### 128x128
- `icon_128x128.png` - 128x128px
- `icon_128x128@2x.png` - 256x256px (Retina @2x)

### 256x256
- `icon_256x256.png` - 256x256px
- `icon_256x256@2x.png` - 512x512px (Retina @2x)

### 512x512
- `icon_512x512.png` - 512x512px
- `icon_512x512@2x.png` - 1024x1024px (Retina @2x)

## Adding Icons to Xcode

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
