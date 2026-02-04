#!/usr/bin/env python3
"""Final extraction: Keep only real sentences and code."""

import re
from pathlib import Path

def is_real_sentence(line):
    """Check if line is a real sentence with substance."""
    # Must have letters and words
    if not re.search(r'[a-zA-Z]', line):
        return False
    
    # Must be reasonable length (not just keywords)
    words = line.split()
    if len(words) < 3:
        return False
    
    # Skip common nav/junk patterns
    if any(x in line.lower() for x in [
        'linkedin', 'reddit', 'facebook', 'twitter', 'email',
        'subscribe', 'sign in', 'log in', 'manage cookies',
        'privacy', 'cookie', 'terms of use',
    ]):
        return False
    
    # Skip URL fragments and share buttons
    if 'http' in line and '://' in line:
        return False
    
    # Skip lines that are mostly symbols
    symbol_count = len(re.findall(r'[)(]{}\[\]]+', line))
    if symbol_count > len(words) / 2:
        return False
    
    return True

def extract_substance(file_path):
    """Extract real content."""
    
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
    
    # Filter body
    content_lines = []
    for line in lines[body_start:]:
        stripped = line.strip()
        
        if not stripped or len(stripped) < 3:
            continue
        
        # Keep headers
        if stripped.startswith('#'):
            content_lines.append(stripped)
            continue
        
        # Keep code blocks
        if '```' in stripped or stripped.startswith('def ') or stripped.startswith('class '):
            content_lines.append(stripped)
            continue
        
        # Keep real sentences
        if is_real_sentence(stripped):
            # Clean markdown
            stripped = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', stripped)
            stripped = re.sub(r'!\[.*?\]\([^)]*\)', '', stripped)
            content_lines.append(stripped)
    
    # Reconstruct
    output = '\n'.join(metadata_lines)
    output += '\n' + '=' * 80 + '\n\n'
    output += '\n'.join(content_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    files = sorted(links_dir.glob('web_*.txt'))
    
    print(f"Final extraction of substance...\n")
    
    for file_path in files:
        try:
            extract_substance(file_path)
            size_kb = file_path.stat().st_size / 1024
            print(f"✓ {file_path.name:40s} ({size_kb:6.1f}KB)")
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
    
    total_size = sum(f.stat().st_size for f in files)
    avg_size = total_size / len(files)
    print(f"\n{'='*60}")
    print(f"Final: {len(files)} files, {total_size/1024:.1f}KB total, {avg_size/1024:.1f}KB avg")

if __name__ == '__main__':
    main()
