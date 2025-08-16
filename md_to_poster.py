#!/usr/bin/env python3
"""
Convert a structured Markdown file to poster HTML format.

The markdown should be structured with:
- YAML front matter for metadata
- Level 2 headers (##) for column breaks  
- Level 3 headers (###) for section titles
- ![](image.png) for images/graphs
"""

import re
import sys
from pathlib import Path

def parse_markdown(md_content):
    """Parse markdown content into structured data."""
    
    # Extract front matter (between --- lines)
    front_matter = {}
    if md_content.startswith('---'):
        parts = md_content.split('---', 2)
        if len(parts) >= 3:
            # Parse YAML-like front matter
            for line in parts[1].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    front_matter[key.strip()] = value.strip()
            md_content = parts[2]
    
    # Split content by ## headers (columns)
    columns = []
    current_column = []
    
    lines = md_content.strip().split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('## '):
            # New column
            if current_column:
                columns.append(current_column)
            current_column = []
            # Skip the column header itself
            i += 1
            continue
            
        current_column.append(line)
        i += 1
    
    # Add last column
    if current_column:
        columns.append(current_column)
    
    # Parse each column into sections
    parsed_columns = []
    for col_lines in columns:
        sections = []
        current_section = {'title': None, 'content': []}
        
        for line in col_lines:
            if line.startswith('### '):
                # New section
                if current_section['content'] or current_section['title']:
                    sections.append(current_section)
                current_section = {
                    'title': line[4:].strip(),
                    'content': []
                }
            else:
                current_section['content'].append(line)
        
        # Add last section
        if current_section['content'] or current_section['title']:
            sections.append(current_section)
        
        parsed_columns.append(sections)
    
    return front_matter, parsed_columns

def markdown_to_html(text):
    """Convert markdown text to HTML."""
    # Handle images
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    
    # Handle bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Handle italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Handle links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text

def generate_section_html(section):
    """Generate HTML for a section."""
    html = '<div class="section">\n'
    
    if section['title']:
        html += f'\t<div class="section-title">{section["title"]}</div>\n'
    
    html += '\t<div class="section-content">\n'
    
    content = '\n'.join(section['content']).strip()
    
    # Check if content contains an image
    if '![' in content:
        # Extract and handle images specially
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('!['):
                html += '\t\t<div class="graph-container">\n'
                html += f'\t\t\t{markdown_to_html(line)}\n'
                html += '\t\t</div>\n'
            elif line.strip():
                html += f'\t\t<p>{markdown_to_html(line)}</p>\n'
    else:
        # Regular paragraph content
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Check for bullet points
                if para.strip().startswith('- ') or para.strip().startswith('* '):
                    html += '\t\t<ul>\n'
                    for line in para.split('\n'):
                        if line.strip().startswith(('- ', '* ')):
                            item = line.strip()[2:]
                            html += f'\t\t\t<li>{markdown_to_html(item)}</li>\n'
                    html += '\t\t</ul>\n'
                else:
                    html += f'\t\t<p>{markdown_to_html(para)}</p>\n'
    
    html += '\t</div>\n'
    html += '</div>'
    
    return html

def generate_poster_html(front_matter, columns):
    """Generate the complete poster HTML."""
    
    title = front_matter.get('title', 'Untitled Poster')
    authors = front_matter.get('authors', '')
    logo = front_matter.get('logo', 'mats-logo-small.png')
    
    html = '''<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>''' + title + '''</title>
	<style>
		* {
			margin: 0;
			padding: 0;
			box-sizing: border-box;
		}

		body {
			font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
			background: white;
			color: #333;
			line-height: 1.4;
		}

		.poster {
			width: 36in;
			height: 24in;
			background: white;
			display: flex;
			flex-direction: column;
			padding: 0;
			margin: 0 auto;
			transform-origin: top left;
			transform: scale(0.33);
			box-shadow: 0 0 20px rgba(0,0,0,0.3);
		}

		/* Header Section */
		.header {
			display: flex;
			align-items: center;
			justify-content: space-between;
			background: #801323;
			padding: 0.4in 0.5in;
			margin-bottom: 0;
			height: 3in;
		}

		.logo {
			display: flex;
			align-items: center;
			height: 100%;
		}

		.logo-icon {
			height: 100%;
			aspect-ratio: 1;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		.logo-icon img {
			width: 100%;
			height: 100%;
			object-fit: contain;
		}

		.title-section {
			flex-grow: 1;
			text-align: center;
			padding: 0 1in;
		}

		h1 {
			font-size: 1.6in;
			color: white;
			font-weight: 600;
			margin-bottom: 0.2in;
			line-height: 1;
		}

		.authors {
			font-size: 0.35in;
			color: #f0f0f0;
			line-height: 1.3;
		}

		/* Main Content Grid */
		.content {
			display: grid;
			grid-template-columns: 1fr 1fr 1fr;
			gap: 0.4in;
			flex-grow: 1;
			padding: 0.5in;
		}

		.column {
			display: flex;
			flex-direction: column;
			gap: 0.3in;
		}

		/* Section Boxes */
		.section {
			background: #f9f9f9;
			padding: 0.3in;
			border-radius: 0.1in;
			border: 1px solid #ddd;
		}

		.section-title {
			background: #801323;
			color: white;
			padding: 0.12in 0.25in;
			margin: -0.3in -0.3in 0.25in -0.3in;
			font-size: 0.35in;
			font-weight: 600;
			border-radius: 0.1in 0.1in 0 0;
		}

		.section-content {
			font-size: 0.25in;
			line-height: 1.4;
		}

		.section-content p {
			margin-bottom: 0.15in;
		}

		/* Graph placeholder */
		.graph-container {
			background: white;
			padding: 0.3in;
			border-radius: 0.1in;
			margin: 0.3in 0;
			text-align: center;
			min-height: 3in;
			display: flex;
			align-items: center;
			justify-content: center;
		}

		.graph-container img {
			max-width: 100%;
			height: auto;
		}

		/* Bullet Points */
		ul {
			padding-left: 0.3in;
		}

		li {
			margin-bottom: 0.15in;
		}
	</style>
</head>

<body>
	<div class="poster">
		<!-- Header -->
		<div class="header">
			<div class="logo">
				<div class="logo-icon">
					<img src="''' + logo + '''" alt="Logo">
				</div>
			</div>
			<div class="title-section">
				<h1>''' + title + '''</h1>
				<div class="authors">
					''' + authors + '''
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="content">
'''
    
    # Generate columns
    for i, column_sections in enumerate(columns):
        column_names = ['Left', 'Middle', 'Right']
        html += f'\t\t\t<!-- {column_names[i] if i < 3 else f"Column {i+1}"} Column -->\n'
        html += '\t\t\t<div class="column">\n'
        
        for section in column_sections:
            section_html = generate_section_html(section)
            # Indent properly
            for line in section_html.split('\n'):
                html += '\t\t\t\t' + line + '\n'
        
        html += '\t\t\t</div>\n\n'
    
    html += '''		</div>
	</div>
</body>

</html>'''
    
    return html

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 md_to_poster.py input.md")
        print("Output will be written to poster.html")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)
    
    # Read markdown
    md_content = input_file.read_text()
    
    # Parse markdown
    front_matter, columns = parse_markdown(md_content)
    
    # Generate HTML
    html = generate_poster_html(front_matter, columns)
    
    # Write output
    output_file = Path('poster.html')
    output_file.write_text(html)
    
    print(f"✓ Generated {output_file}")

if __name__ == '__main__':
    main()