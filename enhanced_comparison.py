#!/usr/bin/env python3
"""
Enhanced Text Comparison HTML Generator

This script creates a side-by-side HTML comparison view of multiple text files
in a 3-column format with navigation controls.
Usage: python enhanced_comparison.py file1.txt file2.txt file3.txt [file4.txt ...] [--output filename.html]
       python enhanced_comparison.py --config config.json [--output filename.html]
"""

import sys
import os
import html
import json
import argparse
import webbrowser
from pathlib import Path
from typing import List, Dict, Optional

def read_file_content(file_path: str) -> str:
    """Read and return the content of a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

def format_content_as_paragraphs(content: str) -> str:
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

def get_column_color(index: int, total_columns: int = 3) -> str:
    """Generate a color for each column based on its position."""
    # Default color palette for 3 columns
    colors = [
        '#8b6f47',  # Burlywood
        '#5d6d7e',  # Slate blue gray
        '#6b8e23',  # Olive drab
    ]
    
    if index < len(colors):
        return colors[index]
    else:
        # Generate a color based on hue rotation with muted tones
        hue = (index * 360 / total_columns) % 360
        return f'hsl({hue}, 30%, 40%)'

def read_config_file(config_path: str) -> List[Dict[str, str]]:
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

def generate_file_info_header(total_files: int) -> str:
    """Generate HTML for file information header."""
    return f"""
        <div class="file-info-header">
            <div class="file-counter">Total Files: {total_files}</div>
            <div class="layout-info">Layout: {total_files} files in {(total_files + 2) // 3} rows of 3 columns each</div>
        </div>"""

def generate_html(files_data: List[Dict[str, str]], output_path: Optional[str] = None) -> bool:
    """Generate HTML comparison of multiple text files in row-based layout."""
    
    total_files = len(files_data)
    files_per_row = 3
    total_rows = (total_files + files_per_row - 1) // files_per_row
    
    # Generate file info header
    header_html = generate_file_info_header(total_files)
    
    # Generate all rows HTML
    rows_html = []
    for row in range(total_rows):
        start_idx = row * files_per_row
        end_idx = min(start_idx + files_per_row, total_files)
        row_files = files_data[start_idx:end_idx]
        
        # Generate columns for this row
        columns_html = []
        for i, file_data in enumerate(row_files):
            column_html = f"""
        <div class="column">
            <div class="column-header" style="background: {get_column_color(i)};">
                {html.escape(file_data['name'])}
            </div>
            <div class="column-content">
                <div class="file-info">File: {html.escape(file_data['filename'])}</div>
                {file_data['content']}
            </div>
        </div>"""
            columns_html.append(column_html)
        
        # Add empty columns if needed to maintain 3-column layout
        while len(columns_html) < files_per_row:
            columns_html.append("""
        <div class="column empty-column">
            <div class="column-header" style="background: #f0f0f0; color: #666;">
                No File
            </div>
            <div class="column-content">
                <div class="file-info">No file available</div>
                <p>No file is available for this position.</p>
            </div>
        </div>""")
        
        row_html = f"""
    <div class="row">
        <div class="container">{''.join(columns_html)}
        </div>
    </div>"""
        rows_html.append(row_html)
    
    # Generate complete HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced Text Comparison - {total_files} Files</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f6f4f0;
            line-height: 1.6;
        }}
        
        .file-info-header {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .file-counter, .layout-info {{
            font-size: 16px;
            color: #333;
            font-weight: 500;
            margin: 5px 0;
        }}
        
        .layout-info {{
            color: #666;
            font-size: 14px;
        }}
        
        .row {{
            margin-bottom: 30px;
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
        
        .empty-column {{
            opacity: 0.6;
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
            height: 60vh;
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
                height: 40vh;
            }}
        }}
    </style>
</head>
<body>
    {header_html}
    {''.join(rows_html)}
</body>
</html>"""

    # Determine output path
    if output_path is None:
        output_path = "enhanced_comparison.html"
    
    # Write HTML file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Enhanced HTML comparison created: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {str(e)}")
        return False

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a side-by-side HTML comparison view of multiple text files in a 3-column format with navigation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_comparison.py file1.txt file2.txt file3.txt
  python enhanced_comparison.py file1.txt file2.txt file3.txt file4.txt file5.txt --output comparison.html
  python enhanced_comparison.py --config config.json
  python enhanced_comparison.py --config config.json --output mypage.html
  python enhanced_comparison.py --directory /path/to/directory
  python enhanced_comparison.py --directory . --output all_files.html
        """
    )
    
    parser.add_argument('files', nargs='*', help='Text files to compare')
    parser.add_argument('-c', '--config', 
                       help='JSON configuration file (alternative to command-line files)')
    parser.add_argument('-d', '--directory',
                       help='Directory containing .txt files to compare (alternative to command-line files)')
    parser.add_argument('-o', '--output', 
                       help='Output HTML filename (default: enhanced_comparison.html)',
                       default='enhanced_comparison.html')
    
    args = parser.parse_args()
    
    # Check if we have files, config, or directory
    input_methods = [bool(args.files), bool(args.config), bool(args.directory)]
    if sum(input_methods) == 0:
        print("Error: You must provide either text files as arguments, a config file, or a directory.")
        parser.print_help()
        sys.exit(1)
    
    if sum(input_methods) > 1:
        print("Error: You can only use one input method at a time (files, config, or directory).")
        sys.exit(1)
    
    files_data = []
    
    if args.config:
        # Use config file
        config = read_config_file(args.config)
        for column_config in config:
            content = read_file_content(column_config['filename'])
            formatted_content = format_content_as_paragraphs(content)
            files_data.append({
                'name': column_config['name'],
                'filename': column_config['filename'],
                'content': formatted_content
            })
    elif args.directory:
        # Use directory
        directory_path = args.directory
        if not os.path.exists(directory_path):
            print(f"Error: Directory '{directory_path}' does not exist.")
            sys.exit(1)
        
        if not os.path.isdir(directory_path):
            print(f"Error: '{directory_path}' is not a directory.")
            sys.exit(1)
        
        # Find all .txt files in the directory
        txt_files = []
        try:
            for file_path in Path(directory_path).glob("*.txt"):
                if file_path.is_file():
                    txt_files.append(file_path)
        except Exception as e:
            print(f"Error reading directory '{directory_path}': {str(e)}")
            sys.exit(1)
        
        if not txt_files:
            print(f"Error: No .txt files found in directory '{directory_path}'")
            sys.exit(1)
        
        # Sort files alphabetically for consistent ordering
        txt_files.sort()
        
        print(f"Found {len(txt_files)} .txt files in directory '{directory_path}':")
        for file_path in txt_files:
            print(f"  - {file_path.name}")
        
        # Process each .txt file
        for file_path in txt_files:
            content = read_file_content(str(file_path))
            formatted_content = format_content_as_paragraphs(content)
            name = file_path.stem
            files_data.append({
                'name': name,
                'filename': str(file_path),
                'content': formatted_content
            })
    else:
        # Use command-line files
        for file_path in args.files:
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' does not exist.")
                sys.exit(1)
            
            content = read_file_content(file_path)
            formatted_content = format_content_as_paragraphs(content)
            name = Path(file_path).stem
            files_data.append({
                'name': name,
                'filename': file_path,
                'content': formatted_content
            })
    
    if not files_data:
        print("Error: No valid files to process.")
        sys.exit(1)
    
    # Generate HTML comparison
    success = generate_html(files_data, args.output)
    
    if success:
        print(f"Enhanced comparison generated successfully!")
        print(f"Total files: {len(files_data)}")
        print(f"Total rows: {(len(files_data) + 2) // 3}")
        print(f"Open {args.output} in your web browser to view the comparison.")
        
        # Optionally open in browser
        try:
            webbrowser.open(f'file://{os.path.abspath(args.output)}')
        except:
            pass
    else:
        print("Failed to generate comparison.")
        sys.exit(1)

if __name__ == "__main__":
    main() 