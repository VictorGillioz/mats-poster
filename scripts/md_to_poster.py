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

# Poster Configuration Constants
POSTER_WIDTH = "36in"
POSTER_HEIGHT = "24in"
HEADER_HEIGHT = "4in"
HEADER_BACKGROUND = "#801323"
HEADER_PADDING = "0.5in 0.75in"

# Typography
TITLE_FONT_SIZE = "1.3in"
TITLE_MARGIN_BOTTOM = "0.2in"
AUTHORS_FONT_SIZE = "0.45in"
SECTION_TITLE_FONT_SIZE = "0.5in"
SECTION_CONTENT_FONT_SIZE = "0.35in"

# Colors
PRIMARY_COLOR = "#801323"
SECTION_BACKGROUND = "#f9f9f9"
SECTION_BORDER = "#ddd"
AUTHORS_COLOR = "#f0f0f0"

# Spacing and Layout
CONTENT_PADDING = "0.75in"
CONTENT_GAP = "0.6in"
COLUMN_GAP = "0.5in"
SECTION_PADDING = "0.5in"
SECTION_BORDER_RADIUS = "0.1in"
SECTION_TITLE_PADDING = "0.2in 0.4in"
SECTION_TITLE_MARGIN = "-0.5in -0.5in 0.4in -0.5in"
PARAGRAPH_MARGIN = "0.25in"
TITLE_SECTION_PADDING = "0 1in"

# Graph/Image containers
GRAPH_PADDING = "0.5in"
GRAPH_MARGIN = "0.5in 0"
GRAPH_MIN_HEIGHT = "4in"

# Lists
LIST_PADDING_LEFT = "0.5in"
LIST_ITEM_MARGIN = "0.25in"


def parse_markdown(md_content):
    """Parse markdown content into structured data."""

    # Extract front matter (between --- lines)
    front_matter = {}
    if md_content.startswith("---"):
        parts = md_content.split("---", 2)
        if len(parts) >= 3:
            # Parse YAML-like front matter
            lines = parts[1].strip().split("\n")
            current_key = None
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    current_key = key.strip()
                    front_matter[current_key] = value.strip()
                elif current_key and line.strip():
                    # Continuation line - add to current key with newline
                    if front_matter[current_key]:
                        front_matter[current_key] += "\n" + line.strip()
                    else:
                        front_matter[current_key] = line.strip()
            md_content = parts[2]

    # Split content by ## headers (columns)
    columns = []
    current_column = []

    lines = md_content.strip().split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("## "):
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
        current_section = {"title": None, "content": []}

        for line in col_lines:
            if line.startswith("### "):
                # New section - only add previous section if it has content
                if current_section["title"] or any(
                    line.strip() for line in current_section["content"]
                ):
                    sections.append(current_section)
                current_section = {"title": line[4:].strip(), "content": []}
            else:
                current_section["content"].append(line)

        # Add last section only if it has title or non-empty content
        if current_section["title"] or any(
            line.strip() for line in current_section["content"]
        ):
            sections.append(current_section)

        parsed_columns.append(sections)

    return front_matter, parsed_columns


def process_image_path(image_path):
    """Process image path to automatically use assets directory if no path specified."""
    # If path doesn't contain a directory separator, prepend ../assets/
    if "/" not in image_path and "\\" not in image_path:
        return f"../assets/{image_path}"
    return image_path


def parse_nested_list(lines):
    """Parse nested markdown lists and convert to HTML."""
    if not lines:
        return ""

    result = []
    stack = []  # Stack to track nested levels: (indent_level, has_open_li)

    for line in lines:
        # Count leading spaces/tabs to determine indent level
        stripped = line.lstrip()
        if not stripped.startswith(("- ", "* ")):
            continue

        # Calculate indent level (each 2 spaces = 1 level)
        indent = (len(line) - len(stripped)) // 2
        item_text = stripped[2:]  # Remove "- " or "* "

        # Close lists and list items if we're at a shallower level
        while len(stack) > indent + 1:
            level, has_open_li = stack.pop()
            if has_open_li:
                result.append("\t\t" + "\t" * len(stack) + "\t</li>")
            result.append("\t\t" + "\t" * len(stack) + "</ul>")

        # Close current list item if we're starting a new one at same level
        if len(stack) == indent + 1:
            level, has_open_li = stack[-1]
            if has_open_li:
                result.append("\t\t" + "\t" * (len(stack) - 1) + "\t</li>")
                stack[-1] = (level, False)

        # Open new list if we're at a deeper level
        if len(stack) <= indent:
            while len(stack) <= indent:
                result.append("\t\t" + "\t" * len(stack) + "<ul>")
                stack.append((len(stack), False))

        # Add the list item (opening tag)
        result.append("\t\t" + "\t" * len(stack) + f"<li>{markdown_to_html(item_text)}")

        # Mark that we have an open li at this level
        if len(stack) > 0:
            stack[-1] = (stack[-1][0], True)

    # Close all remaining open list items and lists
    while stack:
        level, has_open_li = stack.pop()
        if has_open_li:
            result.append("\t\t" + "\t" * len(stack) + "</li>")
        result.append("\t\t" + "\t" * len(stack) + "</ul>")

    return "\n".join(result) + "\n"


def markdown_to_html(text):
    """Convert markdown text to HTML."""

    # Handle images with automatic asset path processing
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        processed_path = process_image_path(image_path)
        return f'<img src="{processed_path}" alt="{alt_text}">'

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, text)

    # Handle bold
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)

    # Handle italic
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)

    # Handle links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    return text


def generate_section_html(section):
    """Generate HTML for a section."""
    # Skip sections with no content
    content = "\n".join(section["content"]).strip()
    if not content and not section["title"]:
        return ""

    html = '<div class="section">\n'

    if section["title"]:
        html += f'\t<div class="section-title">{section["title"]}</div>\n'

    html += '\t<div class="section-content">\n'

    # Check if content contains an image
    if "![" in content:
        # Extract and handle images specially
        lines = content.split("\n")
        for line in lines:
            if line.strip().startswith("!["):
                html += '\t\t<div class="graph-container">\n'
                html += f"\t\t\t{markdown_to_html(line)}\n"
                html += "\t\t</div>\n"
            elif line.strip():
                html += f"\t\t<p>{markdown_to_html(line)}</p>\n"
    else:
        # Regular paragraph content
        paragraphs = content.split("\n\n")
        for para in paragraphs:
            if para.strip():
                # Check for bullet points
                if para.strip().startswith("- ") or para.strip().startswith("* "):
                    # Use the nested list parser
                    list_lines = para.split("\n")
                    html += parse_nested_list(list_lines)
                else:
                    html += f"\t\t<p>{markdown_to_html(para)}</p>\n"

    html += "\t</div>\n"
    html += "</div>"

    return html


def generate_poster_html(front_matter, columns):
    """Generate the complete poster HTML."""

    title = front_matter.get("title", "Untitled Poster")
    # Convert newlines in title to HTML line breaks
    title = title.replace("\n", "<br>")
    authors = front_matter.get("authors", "")
    logo = front_matter.get("logo", "mats-logo-small.png")
    # Process logo path
    logo = process_image_path(logo)

    html = """<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{title}</title>
	<style>
		* {{
			margin: 0;
			padding: 0;
			box-sizing: border-box;
		}}

		body {{
			font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
			background: white;
			color: #333;
			line-height: 1.4;
		}}

		.poster {{
			width: {POSTER_WIDTH};
			height: {POSTER_HEIGHT};
			background: white;
			display: flex;
			flex-direction: column;
			padding: 0;
			margin: 0 auto;
			box-shadow: 0 0 20px rgba(0,0,0,0.3);
		}}

		/* Header Section */
		.header {{
			display: flex;
			align-items: center;
			justify-content: space-between;
			background: {HEADER_BACKGROUND};
			padding: {HEADER_PADDING};
			margin-bottom: 0;
			height: {HEADER_HEIGHT};
		}}

		.logo {{
			display: flex;
			align-items: center;
			height: 100%;
		}}

		.logo-icon {{
			height: 100%;
			aspect-ratio: 1;
			display: flex;
			align-items: center;
			justify-content: center;
		}}

		.logo-icon img {{
			width: 100%;
			height: 100%;
			object-fit: contain;
		}}

		.title-section {{
			flex-grow: 1;
			text-align: center;
			padding: {TITLE_SECTION_PADDING};
		}}

		h1 {{
			font-size: {TITLE_FONT_SIZE};
			color: white;
			font-weight: 600;
			margin-bottom: {TITLE_MARGIN_BOTTOM};
			line-height: 1;
		}}

		.authors {{
			font-size: {AUTHORS_FONT_SIZE};
			color: {AUTHORS_COLOR};
			line-height: 1.3;
		}}

		/* Main Content Grid */
		.content {{
			display: grid;
			grid-template-columns: 1fr 1fr 1fr;
			gap: {CONTENT_GAP};
			flex-grow: 1;
			padding: {CONTENT_PADDING};
		}}

		.column {{
			display: flex;
			flex-direction: column;
			gap: {COLUMN_GAP};
		}}

		/* Section Boxes */
		.section {{
			background: {SECTION_BACKGROUND};
			padding: {SECTION_PADDING};
			border-radius: {SECTION_BORDER_RADIUS};
			border: 1px solid {SECTION_BORDER};
		}}

		.section-title {{
			background: {PRIMARY_COLOR};
			color: white;
			padding: {SECTION_TITLE_PADDING};
			margin: {SECTION_TITLE_MARGIN};
			font-size: {SECTION_TITLE_FONT_SIZE};
			font-weight: 600;
			border-radius: {SECTION_BORDER_RADIUS} {SECTION_BORDER_RADIUS} 0 0;
		}}

		.section-content {{
			font-size: {SECTION_CONTENT_FONT_SIZE};
			line-height: 1.5;
		}}

		.section-content p {{
			margin-bottom: {PARAGRAPH_MARGIN};
		}}

		/* Graph placeholder */
		.graph-container {{
			background: white;
			padding: {GRAPH_PADDING};
			border-radius: {SECTION_BORDER_RADIUS};
			margin: {GRAPH_MARGIN};
			text-align: center;
			min-height: {GRAPH_MIN_HEIGHT};
			display: flex;
			align-items: center;
			justify-content: center;
		}}

		.graph-container img {{
			max-width: 100%;
			height: auto;
		}}

		/* Bullet Points */
		ul {{
			padding-left: {LIST_PADDING_LEFT};
		}}

		li {{
			margin-bottom: {LIST_ITEM_MARGIN};
		}}
	</style>
</head>

<body>
	<div class="poster">
		<!-- Header -->
		<div class="header">
			<div class="logo">
				<div class="logo-icon">
					<img src="{logo}" alt="Logo">
				</div>
			</div>
			<div class="title-section">
				<h1>{title}</h1>
				<div class="authors">
					{authors}
				</div>
			</div>
		</div>

		<!-- Main Content -->
		<div class="content">
"""

    # Generate columns
    for i, column_sections in enumerate(columns):
        column_names = ["Left", "Middle", "Right"]
        html += (
            f"\t\t\t<!-- {column_names[i] if i < 3 else f'Column {i + 1}'} Column -->\n"
        )
        html += '\t\t\t<div class="column">\n'

        for section in column_sections:
            section_html = generate_section_html(section)
            if section_html:  # Only add non-empty sections
                # Indent properly
                for line in section_html.split("\n"):
                    html += "\t\t\t\t" + line + "\n"

        html += "\t\t\t</div>\n\n"

    html += """		</div>
	</div>
</body>

</html>"""

    return html.format(
        title=title,
        authors=authors,
        logo=logo,
        POSTER_WIDTH=POSTER_WIDTH,
        POSTER_HEIGHT=POSTER_HEIGHT,
        HEADER_BACKGROUND=HEADER_BACKGROUND,
        HEADER_PADDING=HEADER_PADDING,
        HEADER_HEIGHT=HEADER_HEIGHT,
        TITLE_SECTION_PADDING=TITLE_SECTION_PADDING,
        TITLE_FONT_SIZE=TITLE_FONT_SIZE,
        TITLE_MARGIN_BOTTOM=TITLE_MARGIN_BOTTOM,
        AUTHORS_FONT_SIZE=AUTHORS_FONT_SIZE,
        AUTHORS_COLOR=AUTHORS_COLOR,
        CONTENT_GAP=CONTENT_GAP,
        CONTENT_PADDING=CONTENT_PADDING,
        COLUMN_GAP=COLUMN_GAP,
        SECTION_BACKGROUND=SECTION_BACKGROUND,
        SECTION_PADDING=SECTION_PADDING,
        SECTION_BORDER_RADIUS=SECTION_BORDER_RADIUS,
        SECTION_BORDER=SECTION_BORDER,
        PRIMARY_COLOR=PRIMARY_COLOR,
        SECTION_TITLE_PADDING=SECTION_TITLE_PADDING,
        SECTION_TITLE_MARGIN=SECTION_TITLE_MARGIN,
        SECTION_TITLE_FONT_SIZE=SECTION_TITLE_FONT_SIZE,
        SECTION_CONTENT_FONT_SIZE=SECTION_CONTENT_FONT_SIZE,
        PARAGRAPH_MARGIN=PARAGRAPH_MARGIN,
        GRAPH_PADDING=GRAPH_PADDING,
        GRAPH_MARGIN=GRAPH_MARGIN,
        GRAPH_MIN_HEIGHT=GRAPH_MIN_HEIGHT,
        LIST_PADDING_LEFT=LIST_PADDING_LEFT,
        LIST_ITEM_MARGIN=LIST_ITEM_MARGIN,
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 md_to_poster.py input.md")
        print("Output will be written to output/poster.html")
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
    output_file = Path("output/poster.html")
    output_file.parent.mkdir(exist_ok=True)  # Ensure output directory exists
    output_file.write_text(html)

    print(f"✓ Generated {output_file}")


if __name__ == "__main__":
    main()
