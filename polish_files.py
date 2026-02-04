#!/usr/bin/env python3
"""Final polish: remove markdown artifacts and excessive spacing."""

import re
from pathlib import Path

def polish_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Preserve metadata header
    header_lines = 0
    for i, line in enumerate(lines):
        if line.startswith('Source URL:') or line.startswith('Final URL:') or '=' * 10 in line:
            header_lines = i + 2
    
    metadata = '\n'.join(lines[:header_lines])
    body = '\n'.join(lines[header_lines:])
    
    # Clean markdown artifacts
    body = re.sub(r'!\[.*?\]\(.*?\)', '', body)  # Images
    body = re.sub(r'\[([^\]]+)\]\(([^)]*)\)', r'\1', body)  # Links: [text](url) → text
    body = re.sub(r'\*\*([^*]+)\*\*', r'\1', body)  # **bold** → bold
    body = re.sub(r'__([^_]+)__', r'\1', body)  # __bold__ → bold
    body = re.sub(r'\*([^*]+)\*', r'\1', body)  # *italic* → italic
    body = re.sub(r'_([^_]+)_', r'\1', body)  # _italic_ → italic
    body = re.sub(r'`([^`]+)`', r'\1', body)  # `code` → code
    
    # Clean stray markdown/html remnants
    body = re.sub(r'^\]\(', '', body, flags=re.MULTILINE)  # orphaned ](
    body = re.sub(r'^\|$', '', body, flags=re.MULTILINE)  # stray table separators
    body = re.sub(r'^---$', '', body, flags=re.MULTILINE)  # stray lines
    body = re.sub(r'^#+\s*$', '', body, flags=re.MULTILINE)  # empty headers
    
    # Clean excessive whitespace (but preserve paragraphs)
    body = re.sub(r' +', ' ', body)  # Multiple spaces → single
    body = re.sub(r'\n\s*\n\s*\n\s*\n+', '\n\n', body)  # Multiple blank lines
    body = body.strip()
    
    # Reconstruct
    output = metadata.rstrip() + '\n\n' + body
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    files = sorted(links_dir.glob('web_*.txt'))
    
    print(f"Polishing {len(files)} files...\n")
    
    for file_path in files:
        try:
            polish_file(file_path)
            print(f"✓ {file_path.name}")
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
    
    total_size = sum(f.stat().st_size for f in files)
    print(f"\nComplete: {len(files)} files, {total_size/1024:.1f}KB")

if __name__ == '__main__':
    main()
