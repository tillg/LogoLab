# LogoLab

My lab for creating logos for different projects.

## Workflow

1. **Design** - Iteratively create logos in SVG format (with AI help 😜)
   - Save iterations as `01_initial.svg`, `02_updated.svg`, etc. in `logos/<ProjectName>/`

2. **Generate** - Transform SVG logos into platform-specific assets
   - macOS app icons (PNG files at multiple sizes)
   - Web assets (coming soon)

## Tools

See **[tools/TOOLS.md](tools/TOOLS.md)** for setup instructions and available tools.

## Project Structure

```text
LogoLab/
├── logos/<ProjectName>/     # Your SVG iterations
│   └── generated/           # Auto-generated assets (gitignored)
├── tools/                   # Asset generation tools
└── requirements.txt         # Python dependencies
```
