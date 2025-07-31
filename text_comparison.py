#!/usr/bin/env python3
"""
Text Comparison HTML Generator

This script creates a side-by-side HTML comparison view of three text files.
Usage: python text_comparison.py file1.txt file2.txt file3.txt [--output filename.html]
"""

import sys
import os
import html
import argparse
from pathlib import Path

def read_file_content(file_path):
    """Read and return the content of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

def format_content_as_paragraphs(content):
    """Format text content as HTML paragraphs."""
    # Escape HTML characters
    content = html.escape(content)
    
    # Split into paragraphs (double newlines or single newlines for short text)
    paragraphs = content.split('\n\n')
    if len(paragraphs) == 1:
        # If no double newlines, split on single newlines
        paragraphs = content.split('\n')
    
    # Filter out empty paragraphs and wrap in <p> tags
    formatted_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para:
            # Replace single newlines within paragraphs with <br> tags
            para = para.replace('\n', '<br>')
            formatted_paragraphs.append(f'<p>{para}</p>')
    
    return '\n                '.join(formatted_paragraphs)

def generate_html(file1_path, file2_path, file3_path, output_path=None):
    """Generate HTML comparison of three text files."""
    
    # Read file contents
    content1 = read_file_content(file1_path)
    content2 = read_file_content(file2_path)
    content3 = read_file_content(file3_path)
    
    # Get file names for headers
    name1 = Path(file1_path).stem
    name2 = Path(file2_path).stem
    name3 = Path(file3_path).stem
    
    # Format content as paragraphs
    formatted_content1 = format_content_as_paragraphs(content1)
    formatted_content2 = format_content_as_paragraphs(content2)
    formatted_content3 = format_content_as_paragraphs(content3)
    
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Three-Column Text Comparison</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f6f4f0;
            line-height: 1.6;
        }}
        
        .container {{
            display: flex;
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .column {{
            flex: 1;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .column-header {{
            background: #3d3d3d;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 18px;
            text-align: center;
        }}
        
        .column-content {{
            padding: 20px;
            height: 80vh;
            overflow-y: auto;
            font-size: 14px;
        }}
        
        .column1-header {{
            background: #8b6f47;
        }}
        
        .column2-header {{
            background: #5d6d7e;
        }}
        
        .column3-header {{
            background: #6b8e23;
        }}
        
        .column-content p {{
            margin-bottom: 12px;
        }}
        
        .column-content::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .column-content::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}
        
        .column-content::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 4px;
        }}
        
        .column-content::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}
        
        @media (max-width: 1024px) {{
            .container {{
                flex-direction: column;
            }}
            
            .column-content {{
                height: 50vh;
            }}
        }}
        
        .file-info {{
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="column">
            <div class="column-header column1-header">
                {name1}
            </div>
            <div class="column-content">
                <div class="file-info">File: {file1_path}</div>
                {formatted_content1}
            </div>
        </div>

        <div class="column">
            <div class="column-header column2-header">
                {name2}
            </div>
            <div class="column-content">
                <div class="file-info">File: {file2_path}</div>
                {formatted_content2}
            </div>
        </div>

        <div class="column">
            <div class="column-header column3-header">
                {name3}
            </div>
            <div class="column-content">
                <div class="file-info">File: {file3_path}</div>
                {formatted_content3}
            </div>
        </div>
    </div>
</body>
</html>"""

    # Determine output path
    if output_path is None:
        output_path = "text_comparison.html"
    
    # Write HTML file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML comparison created: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {str(e)}")
        return False

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a side-by-side HTML comparison view of three text files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python text_comparison.py file1.txt file2.txt file3.txt
  python text_comparison.py doc1.txt doc2.txt doc3.txt --output comparison.html
  python text_comparison.py -o report.html text1.txt text2.txt text3.txt
        """
    )
    
    parser.add_argument('file1', help='First text file to compare')
    parser.add_argument('file2', help='Second text file to compare')
    parser.add_argument('file3', help='Third text file to compare')
    parser.add_argument('-o', '--output', 
                       help='Output HTML filename (default: text_comparison.html)',
                       default='text_comparison.html')
    
    args = parser.parse_args()
    
    # Verify input files exist
    for file_path in [args.file1, args.file2, args.file3]:
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            sys.exit(1)
    
    # Generate HTML comparison
    success = generate_html(args.file1, args.file2, args.file3, args.output)
    
    if success:
        print("Comparison generated successfully!")
        print(f"Open {args.output} in your web browser to view the comparison.")
    else:
        print("Failed to generate comparison.")
        sys.exit(1)

if __name__ == "__main__":
    main()