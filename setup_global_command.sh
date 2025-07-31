#!/bin/bash

# Setup script to make enhanced_comparison.py available globally

# Get the current directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create a wrapper script in /usr/local/bin
sudo tee /usr/local/bin/compare-texts > /dev/null << 'EOF'
#!/bin/bash

# Wrapper script for enhanced text comparison tool
python3 /Users/michaelbernaski/Documents/sidebyside/enhanced_comparison.py "$@"
EOF

# Make the wrapper script executable
sudo chmod +x /usr/local/bin/compare-texts

echo "✅ Enhanced text comparison tool is now available as 'compare-texts'"
echo ""
echo "Usage examples:"
echo "  compare-texts file1.txt file2.txt file3.txt"
echo "  compare-texts --directory ."
echo "  compare-texts --config config.json"
echo "  compare-texts --directory /path/to/directory --output comparison.html"
echo ""
echo "You can now run 'compare-texts' from anywhere on your computer!" 