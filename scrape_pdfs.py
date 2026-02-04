#!/usr/bin/env python3
"""
Scrape PDF links from Comment Ratios Dataset and convert PDFs to text files.
"""

import csv
import re
import os
import sys
from urllib.parse import urlparse
import requests
from io import BytesIO

# Try importing PDF libraries
try:
    from PyPDF2 import PdfReader
    HAS_PYPDF2 = True
except ImportError:
    try:
        from pypdf import PdfReader
        HAS_PYPDF2 = True
    except ImportError:
        HAS_PYPDF2 = False
        print("Warning: PyPDF2 not installed. Install with: pip install PyPDF2")

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False
    print("Warning: pdfplumber not installed. Install with: pip install pdfplumber")


def extract_pdf_links(text):
    """Extract all PDF links from text"""
    if not text:
        return []
    
    # Pattern to match URLs ending with .pdf
    pdf_pattern = r'https?://[^\s<>"{}|\\^\[\]`]+\.pdf'
    
    # Also check for PDF links in notes column
    all_links = re.findall(pdf_pattern, text, re.IGNORECASE)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_links = []
    for link in all_links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    
    return unique_links


def download_pdf(url, timeout=30):
    """Download PDF from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def extract_text_pypdf2(pdf_file):
    """Extract text using PyPDF2"""
    try:
        reader = PdfReader(pdf_file)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
        return '\n\n'.join(text)
    except Exception as e:
        print(f"Error extracting with PyPDF2: {e}")
        return None


def extract_text_pdfplumber(pdf_file):
    """Extract text using pdfplumber"""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            text = []
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return '\n\n'.join(text)
    except Exception as e:
        print(f"Error extracting with pdfplumber: {e}")
        return None


def pdf_to_text(pdf_file):
    """Convert PDF to text using available library"""
    # Try pdfplumber first (better quality)
    if HAS_PDFPLUMBER:
        text = extract_text_pdfplumber(pdf_file)
        if text:
            return text
    
    # Fall back to PyPDF2
    if HAS_PYPDF2:
        pdf_file.seek(0)  # Reset file pointer
        text = extract_text_pypdf2(pdf_file)
        if text:
            return text
    
    return None


def sanitize_filename(url):
    """Create a safe filename from URL"""
    # Extract filename from URL
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    
    # Remove .pdf extension and sanitize
    filename = filename.replace('.pdf', '')
    filename = re.sub(r'[^\w\-_]', '_', filename)
    
    return filename + '.txt'


def process_csv(csv_path, output_dir):
    """Process the CSV file and extract PDFs"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Track results
    results = {
        'total_rows': 0,
        'rows_with_pdfs': 0,
        'total_pdf_links': 0,
        'successful_downloads': 0,
        'failed_downloads': 0,
        'pdf_links': []
    }
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    f = None
    
    for encoding in encodings:
        try:
            f = open(csv_path, 'r', encoding=encoding, errors='replace')
            break
        except:
            continue
    
    if f is None:
        raise Exception("Could not open file with any encoding")
    
    with f:
        reader = csv.DictReader(f)
        
        for row in reader:
            results['total_rows'] += 1
            
            # Get all text that might contain links
            description = row.get('', '')  # The large description column
            notes = row.get('notes', '')
            has_external = row.get('has_external_doc_ref', 'FALSE')
            
            # Combine all text
            all_text = f"{description} {notes}"
            
            # Extract PDF links
            pdf_links = extract_pdf_links(all_text)
            
            if pdf_links:
                results['rows_with_pdfs'] += 1
                results['total_pdf_links'] += len(pdf_links)
                
                project = row.get('project', 'unknown')
                model = row.get('model', 'unknown')
                
                print(f"\n{'='*80}")
                print(f"Project: {project}, Model: {model}")
                print(f"Found {len(pdf_links)} PDF link(s):")
                
                for link in pdf_links:
                    print(f"  - {link}")
                    results['pdf_links'].append({
                        'project': project,
                        'model': model,
                        'url': link
                    })
                    
                    # Download and convert PDF
                    filename = sanitize_filename(link)
                    output_path = os.path.join(output_dir, f"{project}_{model}_{filename}")
                    
                    if os.path.exists(output_path):
                        print(f"    Already exists: {output_path}")
                        results['successful_downloads'] += 1
                        continue
                    
                    print(f"    Downloading...")
                    pdf_data = download_pdf(link)
                    
                    if pdf_data:
                        print(f"    Converting to text...")
                        text = pdf_to_text(pdf_data)
                        
                        if text:
                            with open(output_path, 'w', encoding='utf-8') as out:
                                out.write(f"Source URL: {link}\n")
                                out.write(f"Project: {project}\n")
                                out.write(f"Model: {model}\n")
                                out.write(f"{'='*80}\n\n")
                                out.write(text)
                            print(f"    ✓ Saved to: {output_path}")
                            results['successful_downloads'] += 1
                        else:
                            print(f"    ✗ Failed to extract text")
                            results['failed_downloads'] += 1
                    else:
                        results['failed_downloads'] += 1
    
    return results


def main():
    csv_path = '/home/espencer2/Papers-dataset/Comment Ratios Dataset(Comments Ratio).csv'
    output_dir = '/home/espencer2/FormaLLM/scraped_pdfs'
    
    print("PDF Scraper for Comment Ratios Dataset")
    print("="*80)
    print(f"Input CSV: {csv_path}")
    print(f"Output directory: {output_dir}")
    print()
    
    if not HAS_PYPDF2 and not HAS_PDFPLUMBER:
        print("ERROR: No PDF library available!")
        print("Please install one of:")
        print("  pip install PyPDF2")
        print("  pip install pdfplumber")
        return 1
    
    print("Processing CSV file...")
    results = process_csv(csv_path, output_dir)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total rows processed: {results['total_rows']}")
    print(f"Rows with PDF links: {results['rows_with_pdfs']}")
    print(f"Total PDF links found: {results['total_pdf_links']}")
    print(f"Successful downloads: {results['successful_downloads']}")
    print(f"Failed downloads: {results['failed_downloads']}")
    
    # Save link inventory
    inventory_path = os.path.join(output_dir, '_pdf_inventory.txt')
    with open(inventory_path, 'w', encoding='utf-8') as f:
        f.write("PDF Links Inventory\n")
        f.write("="*80 + "\n\n")
        for item in results['pdf_links']:
            f.write(f"Project: {item['project']}\n")
            f.write(f"Model: {item['model']}\n")
            f.write(f"URL: {item['url']}\n")
            f.write("-"*80 + "\n")
    
    print(f"\nInventory saved to: {inventory_path}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
