# Poster Generator

Convert structured Markdown files to professional HTML and PDF posters with live development workflow.

## Features

✨ **Markdown to Poster**: Write posters in simple markdown with YAML front matter  
🎨 **Customizable Design**: Easy-to-modify constants for fonts, colors, and spacing  
📱 **Live Development**: Auto-regeneration and browser refresh on file save  
📝 **Rich Formatting**: Multi-line titles, nested bullet points, bold/italic text  
🔧 **Organized Structure**: Clean directory organization for maintainability

## Quick Start

### 1. Development Mode (Recommended)
```bash
./serve.sh
```
This starts a development server with:
- Auto-regeneration when you save `poster.md`
- Live browser refresh
- Instant preview at `http://localhost:3000`

### 2. One-time Generation
```bash
./generate_poster.sh poster.md
```
You need to run this to get the final PDF. The PDF will probably look somewhat different from the HTML page that appears in your browser, so make sure to check how it looks.

### 3. Setup for PDF Generation
```bash
pip install playwright
playwright install chromium
# For file watching (auto-regeneration):
sudo apt-get install inotify-tools
```

## Markdown Structure

Your markdown file should follow this structure:

```markdown
---
title: Your Poster Title:
It Can Be Multi-line
authors: Author1, Author2, Author3
logo: logo-filename.png
---

## Left Column

**Bold introduction text.** Regular paragraph content here...

### Section Title
Section content with *italic* and **bold** formatting.

**Key Point:** Important information here.

## Middle Column

### Another Section
More content with automatic image handling...

![Graph Description](graph-image.png)

### Research Results
Additional findings and analysis...

## Right Column

### Conclusions
- Top level bullet point
  - Nested sub-point
  - Another sub-point
- Second main point
  - With nested content

Final paragraph content here.
```

### Key Features:

1. **Multi-line Titles**: Line breaks in titles are preserved exactly as written
2. **Smart Image Paths**: `image.png` automatically becomes `../assets/image.png`
3. **Nested Lists**: Support for multi-level bullet points with proper indentation
4. **Equal Heights**: All columns automatically stretch to match the tallest
5. **Flexible Content**: Sections can contain any mix of text, images, and lists

## Directory Structure

```
poster/
├── assets/                     # Images and logos
│   ├── example-graph.png
│   ├── mats-logo-small.png
│   └── mats-logo.png
├── output/                     # Generated files
│   ├── poster.html
│   └── poster.pdf
├── scripts/                    # Core conversion scripts
│   ├── html_to_pdf.py         # HTML → PDF conversion
│   └── md_to_poster.py        # Markdown → HTML conversion
├── generate_poster.sh          # One-time generation
├── serve.sh                    # Development server + file watching
├── poster.md                   # Your poster content
└── README.md
```

## Customization

### Design Constants
Edit `scripts/md_to_poster.py` to customize the poster design:

```python
# Dimensions
POSTER_WIDTH = "36in"
POSTER_HEIGHT = "24in"

# Typography  
TITLE_FONT_SIZE = "2in"
SECTION_TITLE_FONT_SIZE = "0.5in"
SECTION_CONTENT_FONT_SIZE = "0.35in"

# Colors
PRIMARY_COLOR = "#801323"
SECTION_BACKGROUND = "#f9f9f9"

# Spacing
CONTENT_PADDING = "0.75in"
CONTENT_GAP = "0.6in"
# ... and many more
```

### Individual Commands
```bash
# Generate HTML only
python3 scripts/md_to_poster.py poster.md

# Convert HTML to PDF
python3 scripts/html_to_pdf.py output/poster.html output/poster.pdf

# Watch specific file
./serve.sh my-other-poster.md
```

## PDF Output

- **Dimensions**: Exactly 36" × 24" (landscape)
- **Quality**: High-resolution, perfect for professional printing
- **Format**: Single page with equal-height columns
- **Assets**: All images properly embedded with relative paths