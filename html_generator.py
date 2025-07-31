#!/usr/bin/env python3
"""
Generic HTML Multi-Column Generator

This script creates a multi-column HTML page based on a JSON configuration file.
Usage: python html_generator.py config.json [--output filename.html]
"""

import sys
import os
import html
import json
import argparse
import webbrowser
from pathlib import Path

def read_config_file(config_path):
    """Read and parse the JSON configuration file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Validate config structure
        if not isinstance(config, list):
            raise ValueError("Configuration must be a list of column dictionaries")
            
        for i, column in enumerate(config):
            if not isinstance(column, dict):
                raise ValueError(f"Column {i+1} must be a dictionary")
            if 'name' not in column or 'filename' not in column:
                raise ValueError(f"Column {i+1} must have 'name' and 'filename' fields")
                
        return config
        
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid configuration format: {str(e)}")
        sys.exit(1)

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

def get_column_color(index, total_columns):
    """Generate a color for each column based on its position."""
    # Default color palette
    colors = [
        '#8b6f47',  # Burlywood
        '#5d6d7e',  # Slate blue gray
        '#6b8e23',  # Olive drab
        '#a0522d',  # Sienna
        '#696969',  # Dim gray
        '#7b68ee',  # Medium slate blue
        '#8b7355',  # Light brown
        '#4a4a4a',  # Dark gray
    ]
    
    if index < len(colors):
        return colors[index]
    else:
        # Generate a color based on hue rotation with muted tones
        hue = (index * 360 / total_columns) % 360
        return f'hsl({hue}, 30%, 40%)'

def generate_html(config, output_path=None):
    """Generate HTML with multiple columns based on configuration."""
    
    # Get the title from config or use default
    title = "Multi-Column Document Viewer"
    
    # Read content for each column
    columns_data = []
    for i, column_config in enumerate(config):
        content = read_file_content(column_config['filename'])
        formatted_content = format_content_as_paragraphs(content)
        
        columns_data.append({
            'name': column_config['name'],
            'filename': column_config['filename'],
            'content': formatted_content,
            'color': get_column_color(i, len(config))
        })
    
    # Generate column HTML
    columns_html = []
    for i, col_data in enumerate(columns_data):
        column_html = f"""
        <div class="column">
            <div class="column-header" style="background: {col_data['color']};">
                {html.escape(col_data['name'])}
            </div>
            <div class="column-content">
                <div class="file-info">File: {html.escape(col_data['filename'])}</div>
                {col_data['content']}
            </div>
        </div>"""
        columns_html.append(column_html)
    
    # Generate complete HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
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
            max-width: 95%;
            margin: 0 auto;
        }}
        
        .column {{
            flex: 1;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            min-width: 0;
        }}
        
        .column-header {{
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 16px;
            text-align: center;
            word-wrap: break-word;
        }}
        
        .column-content {{
            padding: 20px;
            height: 80vh;
            overflow-y: auto;
            font-size: 14px;
        }}
        
        .column-content p {{
            margin-bottom: 12px;
        }}
        
        .column-content::-webkit-scrollbar {{
            width: 8px;
        }}
        
        .column-content::-webkit-scrollbar-track {{
            background: #ebe7e0;
        }}
        
        .column-content::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 4px;
        }}
        
        .column-content::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}
        
        .file-info {{
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
            font-style: italic;
        }}
        
        @media (max-width: 1024px) {{
            .container {{
                flex-direction: column;
            }}
            
            .column-content {{
                height: 50vh;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">{''.join(columns_html)}
    </div>
</body>
</html>"""

    # Determine output path
    if output_path is None:
        output_path = "output.html"
    
    # Write HTML file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML page created: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {str(e)}")
        return False

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a multi-column HTML page from a JSON configuration file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Configuration file format:
[
    {
        "name": "Column Title",
        "filename": "content_file.txt"
    },
    ...
]

Examples:
  python html_generator.py config.json
  python html_generator.py config.json --output mypage.html
  python html_generator.py -o report.html config.json
        """
    )
    
    parser.add_argument('config', help='JSON configuration file')
    parser.add_argument('-o', '--output', 
                       help='Output HTML filename (default: output.html)',
                       default='output.html')
    
    args = parser.parse_args()
    
    # Verify config file exists
    if not os.path.exists(args.config):
        print(f"Error: Configuration file '{args.config}' does not exist.")
        sys.exit(1)
    
    # Read configuration
    config = read_config_file(args.config)
    
    # Generate HTML
    success = generate_html(config, args.output)
    
    if success:
        print(f"Successfully generated {len(config)}-column HTML page!")
        print(f"Opening {args.output} in your web browser...")
        webbrowser.open(f'file://{os.path.abspath(args.output)}')
    else:
        print("Failed to generate HTML page.")
        sys.exit(1)

if __name__ == "__main__":
    main()