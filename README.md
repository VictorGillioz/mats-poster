# Poster Generator

Convert structured Markdown files to HTML posters automatically.

## Usage

### Quick Start (HTML + PDF)
```bash
./generate_poster.sh poster.md
```

### Individual Steps
```bash
# Generate HTML only
python3 md_to_poster.py poster.md

# Convert HTML to PDF (requires playwright)
python3 html_to_pdf.py poster.html poster.pdf
```

### Setup for PDF Generation
```bash
pip install playwright
playwright install chromium
```

## Markdown Structure

Your markdown file should follow this structure:

```markdown
---
title: Your Poster Title
authors: Author1, Author2, Author3
logo: mats-logo-small.png
---

## Left Column

Content for the first column...

### Section Title
Section content here...

## Middle Column

### Another Section
More content...

![Graph Description](image.png)

## Right Column

### Final Section
- Bullet point 1
- Bullet point 2
```

### Key Rules:

1. **Front matter** (between `---` lines) contains metadata:
   - `title`: Poster title
   - `authors`: Author list
   - `logo`: Logo image filename

2. **Column breaks**: Use `## Column Name` to start new columns (3 columns max)

3. **Sections**: Use `### Section Title` for section headers

4. **Images**: Use `![alt text](filename.png)` for graphs/images

5. **Formatting**:
   - `**bold text**` for bold
   - `*italic text*` for italic
   - `- item` for bullet points
   - Regular paragraphs for text

## Files

- `md_to_poster.py` - Markdown to HTML conversion
- `html_to_pdf.py` - HTML to PDF conversion  
- `generate_poster.sh` - Complete pipeline script
- `serve.sh` - Development server script
- `example-poster.md` - Example markdown file
- `poster.html` - Generated HTML output

## Development

Use `./serve.sh` to start a live-reload server for editing.

## PDF Output

The PDF will be generated at exactly 36" × 24" dimensions, perfect for poster printing.