#!/usr/bin/env python3
"""
Aggressively clean external link files.
Extract only meaningful text: paragraphs, code blocks, headers.
Remove ALL navigation, lists, and boilerplate.
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
from html import unescape

class ContentExtractor(HTMLParser):
    """Extract main content from HTML, ignoring navigation."""
    
    def __init__(self):
        super().__init__()
        self.content = []
        self.in_script = False
        self.in_style = False
        self.in_nav = False
        self.in_footer = False
        self.in_main = False
        self.skip_tags = {'script', 'style', 'noscript', 'meta', 'iframe'}
        self.ignore_classes = [
            'nav', 'navbar', 'menu', 'sidebar', 'footer', 'header',
            'advertisement', 'ad-', 'breadcrumb', 'pagination',
            'comments', 'widget', 'related'
        ]
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Check for main/article content markers
        if tag in ('main', 'article'):
            self.in_main = True
        
        # Skip known junk containers
        if tag in self.skip_tags:
            self.in_script = (tag == 'script')
            self.in_style = (tag == 'style')
            return
        
        class_name = attrs_dict.get('class', '')
        if any(ignore in class_name.lower() for ignore in self.ignore_classes):
            return
        
        # Extract from meaningful tags
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'code', 'pre'):
            if tag.startswith('h'):
                self.content.append(f"\n### {tag.upper()}\n")
            elif tag == 'pre':
                self.content.append("\n```\n")
            elif tag == 'code':
                self.content.append("`")
    
    def handle_endtag(self, tag):
        if tag in ('main', 'article'):
            self.in_main = False
        
        if tag in self.skip_tags:
            self.in_script = False
            self.in_style = False
        
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.content.append('\n')
        elif tag == 'pre':
            self.content.append("\n```\n")
        elif tag == 'code':
            self.content.append("`")
        elif tag == 'p':
            self.content.append('\n')
        elif tag in ('li', 'tr', 'td'):
            self.content.append('\n')
    
    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        
        text = unescape(data).strip()
        if text and len(text) > 2:  # Skip tiny fragments
            self.content.append(text + ' ')
    
    def get_content(self):
        text = ''.join(self.content)
        # Clean up excessive whitespace
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        return text.strip()

def clean_file(file_path):
    """Clean a single file."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Extract metadata
    metadata = {}
    for line in content.split('\n')[:10]:
        if line.startswith('Source URL:'):
            metadata['source_url'] = line.replace('Source URL:', '').strip()
        elif line.startswith('Final URL:'):
            metadata['final_url'] = line.replace('Final URL:', '').strip()
    
    # Remove header
    content = re.sub(r'^Source URL:.*?\n.*?Final URL:.*?\n={10,}\n', '', content, count=1)
    
    # If it's markdown (from html2text), try converting back to text
    if '**' in content or '[' in content:
        # Remove markdown formatting
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)  # Links
        content = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', content)  # Bold/italic
        content = re.sub(r'!?\[.*?\]\(.*?\)', '', content)  # Images
    
    # Apply HTML parser for cleaner extraction
    try:
        extractor = ContentExtractor()
        extractor.feed(content)
        cleaned = extractor.get_content()
    except:
        # Fallback to regex cleaning
        cleaned = re.sub(r'<[^>]+>', '', content)
        cleaned = re.sub(r'\[.*?\]\(.*?\)', '', cleaned)
        cleaned = re.sub(r'\n+', '\n', cleaned)
    
    # Measure content quality
    text_only = re.sub(r'\s+', ' ', cleaned)
    if len(text_only) < 150:
        return False  # Not enough content
    
    # Reconstruct with metadata
    output = []
    if metadata.get('source_url'):
        output.append(f"Source URL: {metadata['source_url']}")
    if metadata.get('final_url'):
        output.append(f"Final URL: {metadata['final_url']}")
    if output:
        output.append('=' * 80)
        output.append('')
    
    output.append(cleaned)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    return True

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    
    files = sorted(links_dir.glob('web_*.txt'))
    print(f"Aggressively cleaning {len(files)} files...\n")
    
    success = 0
    deleted = 0
    
    for file_path in files:
        try:
            if clean_file(file_path):
                success += 1
                print(f"✓ {file_path.name}")
            else:
                # Delete files with insufficient content
                file_path.unlink()
                deleted += 1
                print(f"✗ {file_path.name} (deleted - minimal content)")
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")
    
    print(f"\n{'='*80}")
    print(f"Results: {success} cleaned, {deleted} deleted")
    
    remaining = list(links_dir.glob('web_*.txt'))
    if remaining:
        total_size = sum(f.stat().st_size for f in remaining)
        print(f"Remaining: {len(remaining)} files, {total_size/1024:.1f}KB total")

if __name__ == '__main__':
    main()
