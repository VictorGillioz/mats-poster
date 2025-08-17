#!/usr/bin/env python3
"""
Convert poster HTML to PDF with proper dimensions.
Requires: pip install playwright
"""

import sys
import asyncio
from pathlib import Path

async def html_to_pdf(html_file, output_file=None):
    """Convert HTML poster to PDF with proper dimensions."""
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: playwright not installed")
        print("Install with: pip install playwright")
        print("Then run: playwright install chromium")
        sys.exit(1)
    
    html_path = Path(html_file)
    if not html_path.exists():
        print(f"Error: {html_file} not found")
        sys.exit(1)
    
    if output_file is None:
        output_file = html_path.stem + '.pdf'
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Load the HTML file
        await page.goto(f"file://{html_path.absolute()}")
        
        # Wait for any images to load
        await page.wait_for_load_state('networkidle')
        
        # Generate PDF with exact poster dimensions
        # 36" x 24" at 300 DPI = 10800 x 7200 pixels
        await page.pdf(
            path=output_file,
            width='36in',  # Poster width
            height='24in', # Poster height
            margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
            print_background=True,
            scale=1.0
        )
        
        await browser.close()
    
    print(f"✓ Generated {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 html_to_pdf.py poster.html [output.pdf]")
        print("Example: python3 html_to_pdf.py poster.html poster.pdf")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Run the async function
    asyncio.run(html_to_pdf(html_file, output_file))

if __name__ == '__main__':
    main()