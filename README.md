# Enhanced Text Comparison Tool

A powerful Python tool for creating beautiful side-by-side HTML comparisons of multiple text files. Perfect for comparing documents, code, or any text-based content in a clean, responsive 3-column layout.

## ✨ Features

- **Multi-file Support**: Compare any number of text files (not limited to 3)
- **Row-based Layout**: All files displayed on one long, scrollable page
- **3-Column Format**: Always maintains a clean 3-column layout per row
- **Directory Processing**: Automatically process all `.txt` files in a directory
- **Global Command**: Use `compare-texts` from anywhere on your system
- **Config File Support**: Use JSON configuration for custom file names and paths
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **No Dependencies**: Uses only Python standard library

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mjbernaski/sidebyside.git
   cd sidebyside
   ```

2. **Set up global command (optional):**
   ```bash
   ./setup_global_command.sh
   ```

### Basic Usage

#### Compare Specific Files
```bash
# Compare 3 files
python3 enhanced_comparison.py file1.txt file2.txt file3.txt

# Compare 5 files (will create 2 rows)
python3 enhanced_comparison.py file1.txt file2.txt file3.txt file4.txt file5.txt

# Specify output file
python3 enhanced_comparison.py file1.txt file2.txt file3.txt --output my_comparison.html
```

#### Compare All Files in a Directory
```bash
# Current directory
python3 enhanced_comparison.py --directory .

# Specific directory
python3 enhanced_comparison.py --directory /path/to/directory

# With custom output
python3 enhanced_comparison.py --directory . --output all_files.html
```

#### Use Configuration File
```bash
# Use JSON config file
python3 enhanced_comparison.py --config config.json

# With custom output
python3 enhanced_comparison.py --config config.json --output custom.html
```

#### Global Command (after setup)
```bash
# From anywhere on your system
compare-texts file1.txt file2.txt file3.txt
compare-texts --directory .
compare-texts --config config.json
```

## 📁 Configuration File Format

Create a JSON file to specify custom display names and file paths:

```json
[
    {
        "name": "Trump Intelligence Analysis",
        "filename": "trumpintelligence.txt"
    },
    {
        "name": "Student Work - AI Session",
        "filename": "studentWork.txt"
    },
    {
        "name": "AI Assessment Report",
        "filename": "aiassessment.txt"
    }
]
```

## 🎨 Output Features

### Layout
- **Row-based**: Files are arranged in rows of 3 columns each
- **Scrollable**: Each column has independent scrolling
- **Responsive**: Stacks vertically on mobile devices
- **Empty Handling**: Incomplete rows show placeholder columns

### Styling
- **Modern Design**: Clean, professional appearance
- **Color-coded Headers**: Each column has a distinct color
- **File Information**: Shows file paths and total count
- **Typography**: Optimized for readability

### Navigation
- **Single Page**: All content on one long, scrollable page
- **File Counter**: Shows total files and layout information
- **No Pagination**: Simple, intuitive browsing

## 📋 Command Line Options

```bash
python3 enhanced_comparison.py [OPTIONS] [FILES...]

Options:
  -h, --help            Show help message
  -c, --config CONFIG   JSON configuration file
  -d, --directory DIR   Directory containing .txt files
  -o, --output FILE     Output HTML filename (default: enhanced_comparison.html)

Input Methods (use only one):
  - Individual files: file1.txt file2.txt file3.txt
  - Config file: --config config.json
  - Directory: --directory /path/to/directory
```

## 🔧 Installation Details

### Global Command Setup

The `setup_global_command.sh` script:
1. Creates a wrapper script in `/usr/local/bin/compare-texts`
2. Makes it executable system-wide
3. Allows you to use `compare-texts` from any directory

### Requirements
- Python 3.6+
- No external dependencies (uses only standard library)

## 📂 Project Structure

```
sidebyside/
├── enhanced_comparison.py      # Main enhanced comparison tool
├── text_comparison.py          # Original 3-file comparison tool
├── html_generator.py           # Original config-based generator
├── setup_global_command.sh     # Global command installation script
├── config_example.json         # Example configuration file
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🆚 Comparison with Original Tools

| Feature | Original `text_comparison.py` | Original `html_generator.py` | Enhanced `enhanced_comparison.py` |
|---------|------------------------------|------------------------------|-----------------------------------|
| File Limit | Exactly 3 files | Unlimited | Unlimited |
| Layout | Fixed 3 columns | Configurable columns | Fixed 3 columns per row |
| Navigation | None (single page) | None (single page) | Row-based scrolling |
| Directory Support | ❌ | ❌ | ✅ |
| Global Command | ❌ | ❌ | ✅ |
| Config Support | ❌ | ✅ | ✅ |

## 🎯 Use Cases

- **Document Comparison**: Compare multiple versions of documents
- **Code Review**: Side-by-side code comparison
- **Research**: Compare multiple text sources
- **Content Analysis**: Analyze multiple text files simultaneously
- **Teaching**: Show different examples or solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Issues and Support

If you encounter any issues or have questions:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include your Python version and operating system

---

**Made with ❤️ for easy text comparison** 