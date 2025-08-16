# Poster Generator

Convert structured Markdown files to HTML posters automatically.

## Usage

```bash
python3 md_to_poster.py poster.md
```

This generates `poster.html` from your markdown file.

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

- `md_to_poster.py` - Main conversion script
- `example-poster.md` - Example markdown file
- `serve.sh` - Development server script
- `poster.html` - Generated HTML output

## Development

Use `./serve.sh` to start a live-reload server for editing.