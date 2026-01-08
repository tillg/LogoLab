# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a logo design repository for **SafarAI** - a Safari Web Extension that makes the browser AI-intelligent. The repository contains iterative SVG logo designs.

## Repository Structure

- **Numbered SVG files** (`01_*.svg`, `03_*.svg`, etc.) - Logo design iterations for SafarAI
- **Summarum/logo.svg** - Reference logo with the brand color palette to reuse
- **Safari.svg** - Original Safari browser compass logo (source reference)
- **React-icon.svg** - React atom logo (source reference for atomic orbit patterns)

## Brand Color Palette

All SafarAI logos should use the Summarum color scheme:
- **#FB923C** - Orange (lighter)
- **#F59E0B** - Amber (middle)
- **#EF4444** - Red-orange (darker)
- **#2A2A2A** - Dark background

## Design Evolution Pattern

The logo designs follow an iterative numbering system where each new variation explores different concepts:
- Early iterations (01-02): Initial Safari compass concepts with AI elements
- 03: Base Safari compass in Summarum colors (canonical reference)
- 04-06: Robot/tech aesthetics (circuits, hexagons, LEDs)
- 07-08: Robot face/eyes variations
- 14-18: Atomic orbit variations (React-inspired electron orbits around compass)

## Working with SVG Files

When creating new logo variations:
1. Read the base reference file (e.g., `03_safari_summarum_colors.svg` or `Summarum/logo.svg`)
2. Create new iterations with the next sequential number (e.g., `19_description.svg`)
3. Use descriptive filenames that indicate the design concept
4. Maintain the Summarum color palette
5. Keep the Safari compass as the core element (represents navigation/direction)

## Key Design Principles

- The Safari compass represents **navigation** as the core concept
- Surrounding elements (orbits, circuits, etc.) represent **AI intelligence**
- All orbit ellipses should be fully visible within the canvas bounds
- Canvas should be square for consistency (e.g., viewBox with equal width/height)
- When using atomic orbits, center them on the compass at coordinates (33.08, 31.90)
