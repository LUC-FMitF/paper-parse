#!/usr/bin/env python3
"""Nuclear option: Extract ONLY paragraphs with actual substance."""

import re
from pathlib import Path

def extract_substance(file_path):
    """Keep only lines that have actual content (sentences, code, headers)."""
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    # Extract metadata
    metadata_lines = []
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith('Source URL:') or line.startswith('Final URL:'):
            metadata_lines.append(line.rstrip())
        elif '=' * 10 in line:
            body_start = i + 1
            break
    
    # Filter body: keep only lines with substance
    content_lines = []
    for line in lines[body_start:]:
        stripped = line.strip()
        
        # Skip empty or whitespace-only
        if not stripped:
            continue
        
        # Skip single characters (noise)
        if len(stripped) < 3:
            continue
        
        # Skip lines that are mostly symbols/nav (like "* [] * []")
        if re.match(r'^[\s\[\]\-\*\(\)]+$', stripped):
            continue
        
        # Skip navigation keywords (if line is JUST that)
        nav_words = ['menu', 'navigation', 'breadcrumb', 'sidebar', 'footer', 
                     'advertisement', 'subscribe', 'follow us', 'contact us',
                     'cookie', 'privacy', 'terms', 'sign in', 'log in']
        if any(word in stripped.lower() for word in nav_words) and len(stripped) < 30:
            continue
        
        # Keep lines with: sentences (end with . ! ?), headers (#), code (```), or substance
        if any(c in stripped for c in ['.', '!', '?', '#', '`']) or len(stripped) > 20:
            # Clean up remaining markdown on this line
            stripped = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', stripped)
            stripped = re.sub(r'!\[.*?\]\([^)]*\)', '', stripped)
            stripped = re.sub(r'\*\*([^*]+)\*\*', r'\1', stripped)
            stripped = re.sub(r'__([^_]+)__', r'\1', stripped)
            
            content_lines.append(stripped)
    
    # Reconstruct with spacing
    output = '\n'.join(metadata_lines)
    output += '\n' + '=' * 80 + '\n\n'
    output += '\n'.join(content_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    files = sorted(links_dir.glob('web_*.txt'))
    
    print(f"Extracting substance from {len(files)} files...\n")
    
    for file_path in files:
        try:
            extract_substance(file_path)
            size_kb = file_path.stat().st_size / 1024
            print(f"✓ {file_path.name:40s} ({size_kb:6.1f}KB)")
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
    
    total_size = sum(f.stat().st_size for f in files)
    print(f"\nComplete: {len(files)} files, {total_size/1024:.1f}KB")

if __name__ == '__main__':
    main()
