#!/usr/bin/env python3

import json
import argparse
import sys
from pathlib import Path

def create_config():
    parser = argparse.ArgumentParser(
        description='Create a JSON configuration file for html_generator.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python config.py output.json
  python config.py my_config.json --add "Title 1" file1.txt --add "Title 2" file2.txt
  python config.py comparison.json -a "Report A" report_a.txt -a "Report B" report_b.txt
        '''
    )
    
    parser.add_argument('output', help='Output JSON filename (must end with .json)')
    parser.add_argument('-a', '--add', nargs=2, metavar=('NAME', 'FILENAME'), 
                        action='append', dest='entries',
                        help='Add an entry with display name and filename')
    
    args = parser.parse_args()
    
    if not args.output.endswith('.json'):
        print(f"Error: Output filename must end with .json", file=sys.stderr)
        sys.exit(1)
    
    if not args.entries:
        print("Interactive mode: Enter column details (press Ctrl+C to finish)")
        entries = []
        try:
            while True:
                name = input(f"\nColumn {len(entries) + 1} display name (or press Enter to finish): ").strip()
                if not name:
                    break
                    
                filename = input(f"Filename for '{name}': ").strip()
                if not filename:
                    print("Error: Filename cannot be empty")
                    continue
                    
                if not Path(filename).exists():
                    response = input(f"Warning: '{filename}' does not exist. Continue anyway? (y/n): ")
                    if response.lower() != 'y':
                        continue
                
                entries.append([name, filename])
                
        except KeyboardInterrupt:
            print("\n")
    else:
        entries = args.entries
        for name, filename in entries:
            if not Path(filename).exists():
                print(f"Warning: '{filename}' does not exist")
    
    if not entries:
        print("Error: No entries provided", file=sys.stderr)
        sys.exit(1)
    
    config = []
    for name, filename in entries:
        config.append({
            "name": name,
            "filename": filename
        })
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        f.write('\n')
    
    print(f"\nConfiguration saved to: {args.output}")
    print(f"Entries: {len(config)}")
    
    print(f"\nTo use this configuration:")
    print(f"  python html_generator.py {args.output}")

if __name__ == "__main__":
    create_config()