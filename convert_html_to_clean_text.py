#!/usr/bin/env python3
"""
Convert HTML content files to clean, structured text.
Similar to how PDFs are converted - extracts meaningful content only.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

def extract_metadata(content, filename):
    """Extract metadata from the file header"""
    lines = content.split('\n', 10)
    metadata = {}
    
    for line in lines[:5]:
        if line.startswith('Source URL:'):
            metadata['source_url'] = line.replace('Source URL:', '').strip()
        elif line.startswith('Final URL:'):
            metadata['final_url'] = line.replace('Final URL:', '').strip()
    
    return metadata

def convert_html_to_clean_text(html_content):
    """Convert HTML to clean markdown text"""
    try:
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'meta', 'noscript']):
            script.decompose()
        
        # Remove common navigation/footer elements
        for element in soup(['nav', 'footer', 'header', '.sidebar', '.nav']):
            element.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Use html2text for better formatting if there's actual HTML
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # No wrapping
        
        try:
            markdown_text = h.handle(html_content)
            # Use markdown if it looks good
            if len(markdown_text) > len(text) * 0.5:
                text = markdown_text
        except:
            pass
        
        # Clean up excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip excessive empty lines
            if not stripped:
                if not prev_empty:
                    cleaned_lines.append('')
                    prev_empty = True
            else:
                cleaned_lines.append(stripped)
                prev_empty = False
        
        # Join and clean
        result = '\n'.join(cleaned_lines).strip()
        
        # Remove excessive junk
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        return result
    except Exception as e:
        print(f"Error processing HTML: {e}")
        return html_content


def process_file(input_path, output_path):
    """Process a single HTML file"""
    try:
        with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Extract metadata from header
        metadata = extract_metadata(content, os.path.basename(input_path))
        
        # Find the content section (after metadata)
        lines = content.split('\n')
        metadata_end = 0
        for i, line in enumerate(lines):
            if line.startswith('Source URL:') or line.startswith('Final URL:') or line.startswith('='):
                metadata_end = i + 1
        
        # Get just the content part
        content_part = '\n'.join(lines[metadata_end:])
        
        # Convert HTML to clean text
        clean_text = convert_html_to_clean_text(content_part)
        
        # Write output with metadata
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            if 'source_url' in metadata:
                f.write(f"Source URL: {metadata['source_url']}\n")
            if 'final_url' in metadata:
                f.write(f"Final URL: {metadata['final_url']}\n")
            f.write('='*80 + '\n\n')
            
            # Write cleaned content
            f.write(clean_text)
        
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def main():
    external_dir = '/home/espencer2/Papers-dataset/scraped_pdfs/external_links'
    backup_dir = '/home/espencer2/Papers-dataset/scraped_pdfs/external_links_backup'
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    print("="*80)
    print("Converting HTML Files to Clean Text")
    print("="*80)
    print(f"Source: {external_dir}")
    print(f"Backup: {backup_dir}\n")
    
    successful = 0
    failed = 0
    
    # Process all web_*.txt files
    for filename in sorted(os.listdir(external_dir)):
        if not filename.startswith('web_') or not filename.endswith('.txt'):
            continue
        
        input_path = os.path.join(external_dir, filename)
        backup_path = os.path.join(backup_dir, filename)
        
        # Create backup
        try:
            with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
        except:
            pass
        
        print(f"Processing: {filename}")
        
        # Convert file
        if process_file(input_path, input_path):
            successful += 1
            print(f"  ✓ Converted and saved")
        else:
            failed += 1
            print(f"  ✗ Failed to convert")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Successfully converted: {successful}")
    print(f"Failed: {failed}")
    print(f"\nBackup saved to: {backup_dir}")
    print(f"Converted files in: {external_dir}")


if __name__ == '__main__':
    main()
