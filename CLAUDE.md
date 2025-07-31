# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a text comparison tool that generates HTML pages for side-by-side comparison of text files. The project consists of two main Python scripts that create self-contained HTML files with embedded CSS styling.

## Commands

### Running the Text Comparison Tools

```bash
# Three-column comparison (fixed layout)
python text_comparison.py file1.txt file2.txt file3.txt
python text_comparison.py file1.txt file2.txt file3.txt --output custom_output.html

# Flexible multi-column comparison (JSON-based)
python html_generator.py config.json
python html_generator.py config.json --output custom_output.html
```

### Example Usage

```bash
# Compare the three sample files
python text_comparison.py trumpintelligence.txt studentWork.txt aiassessment.txt

# Use the example configuration
python html_generator.py config_example.json
```

## Architecture

The codebase follows a simple architecture:

1. **text_comparison.py** - Handles exactly 3 text files, creates a fixed 3-column layout with predefined colors (red, blue, green)
2. **html_generator.py** - Reads a JSON configuration to support any number of columns with dynamic color assignment, automatically opens the generated HTML in browser
3. Both scripts generate self-contained HTML files with embedded CSS - no external dependencies or build process required

### Key Implementation Details

- Uses only Python standard library (no external dependencies)
- Text is formatted by splitting on double newlines (falls back to single newlines)
- HTML content is properly escaped to prevent injection
- Responsive design using CSS flexbox that stacks columns on mobile
- Each column has scrollable content areas (80vh height)
- Column headers show the filename without extension

### JSON Configuration Format

For `html_generator.py`:
```json
[
    {
        "name": "Display Name",
        "filename": "path/to/file.txt"
    }
]
```

## Development Notes

- No test suite or linting configuration exists
- No dependency management (uses only standard library)
- Not currently under version control (no .git directory)
- All generated HTML files are self-contained and can be opened directly in a browser