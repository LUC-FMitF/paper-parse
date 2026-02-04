#!/usr/bin/env python3
"""Remove remaining navigation patterns at file start/end."""

import re
from pathlib import Path

def cleanup_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Keep metadata
    metadata = []
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith(('Source URL:', 'Final URL:')):
            metadata.append(line)
        elif '=' * 10 in line:
            body_start = i + 1
            break
    
    # Clean body
    body_lines = lines[body_start:]
    
    # Remove leading navigation/section titles that aren't real content
    nav_patterns = [
        r'^(Research areas|People|Microsoft|Labs|Other|Tech|Industries|Search|Global):.*$',
        r'^(Search|Tech|Industries|Global|Partners|Resources).*$',
        r'^(Home|About|Contact|Careers|Events).*$',
    ]
    
    cleaned = []
    for line in body_lines:
        # Skip navigation pattern lines
        if any(re.match(pattern, line) for pattern in nav_patterns):
            continue
        cleaned.append(line)
    
    # Remove excessive blank lines
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    
    # Reconstruct
    output = '\n'.join(metadata)
    output += '\n' + '=' * 80 + '\n\n'
    output += '\n'.join(cleaned)
    
    with open(file_path, 'w') as f:
        f.write(output)

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    files = sorted(links_dir.glob('web_*.txt'))
    
    for file_path in files:
        cleanup_file(file_path)
    
    total = sum(f.stat().st_size for f in files)
    print(f"Cleanup complete: {len(files)} files, {total/1024:.1f}KB")

if __name__ == '__main__':
    main()
