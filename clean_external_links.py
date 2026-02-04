#!/usr/bin/env python3
"""
Clean external link files by extracting actual article content.
Uses trafilatura for better content extraction (removes navigation, ads, etc).
"""

import os
import sys
import trafilatura
from pathlib import Path
import re

def extract_metadata(content):
    """Extract Source URL and Final URL from file header."""
    lines = content.split('\n', 10)
    metadata = {}
    for line in lines[:10]:
        if line.startswith('Source URL:'):
            metadata['source_url'] = line.replace('Source URL:', '').strip()
        elif line.startswith('Final URL:'):
            metadata['final_url'] = line.replace('Final URL:', '').strip()
    return metadata

def clean_file(file_path, backup_dir):
    """Extract main content from file, removing boilerplate."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    metadata = extract_metadata(content)
    
    # Remove metadata header
    content_without_header = re.sub(r'^Source URL:.*?\n.*?Final URL:.*?\n={10,}\n', '', content, count=1)
    
    # Use trafilatura to extract main content (removes navigation, ads, etc)
    try:
        extracted = trafilatura.extract(
            content_without_header,
            include_comments=False,
            favor_precision=True,
            include_tables=True
        )
        
        if extracted:
            cleaned_text = extracted.strip()
        else:
            # Fallback: if trafilatura can't extract, try basic cleanup
            cleaned_text = content_without_header
            # Remove common navigation patterns
            cleaned_text = re.sub(r'\[.*?\]\(.*?\)', '', cleaned_text)  # Remove markdown links
            cleaned_text = re.sub(r'^\*\s+\[.*?\].*?$', '', cleaned_text, flags=re.MULTILINE)  # Remove bullet nav
            cleaned_text = re.sub(r'^(Skip|Jump|Toggle|Click|Sign in|Log in|Menu|Navigation).*?$', 
                                 '', cleaned_text, flags=re.MULTILINE | re.IGNORECASE)
            cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)  # Clean excessive whitespace
    
    except Exception as e:
        print(f"  Error processing {Path(file_path).name}: {e}")
        return False
    
    # Check if content has substance (minimum 200 chars of actual text)
    text_only = re.sub(r'\s+', ' ', cleaned_text)
    if len(text_only) < 200:
        print(f"  SKIP (minimal content): {Path(file_path).name}")
        return False
    
    # Reconstruct file with metadata header + cleaned content
    output = []
    if metadata.get('source_url'):
        output.append(f"Source URL: {metadata['source_url']}")
    if metadata.get('final_url'):
        output.append(f"Final URL: {metadata['final_url']}")
    if output:
        output.append('=' * 80)
        output.append('')
    
    output.append(cleaned_text)
    
    # Write cleaned version
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    return True

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    backup_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links_backup')
    
    if not links_dir.exists():
        print(f"Error: {links_dir} does not exist")
        sys.exit(1)
    
    # Process all web_*.txt files
    files = sorted(links_dir.glob('web_*.txt'))
    print(f"\nCleaning {len(files)} external link files with proper content extraction\n")
    
    success = 0
    skipped = 0
    
    for file_path in files:
        filename = file_path.name
        try:
            if clean_file(file_path, backup_dir):
                success += 1
                print(f"✓ {filename}")
            else:
                skipped += 1
        except Exception as e:
            print(f"✗ {filename}: {e}")
            skipped += 1
    
    print(f"\n{'='*80}")
    print(f"Cleaning complete: {success} cleaned, {skipped} skipped")
    
    # Show before/after stats
    total_size = sum(f.stat().st_size for f in links_dir.glob('web_*.txt'))
    total_files = len(list(links_dir.glob('web_*.txt')))
    print(f"Result: {total_files} files, {total_size/1024/1024:.1f}MB total")

if __name__ == '__main__':
    main()
