#!/usr/bin/env python3
"""
Batch convert all PDFs from /raw to text using PyMuPDF (best performer).
Compares results with manual regex extraction where available.
"""

import os
import json
import time
import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List

RAW_PDF_DIR = "/home/espencer2/Papers-dataset/scraped_pdfs/raw"
REGEX_DIR = "/home/espencer2/Papers-dataset/scraped_pdfs/regex"
OUTPUT_DIR = "/home/espencer2/Papers-dataset/scraped_pdfs/pymupdf"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all PDF files
pdf_files = sorted([f for f in os.listdir(RAW_PDF_DIR) if f.endswith('.pdf')])
print(f"Found {len(pdf_files)} PDF files to convert")
print("=" * 70)

stats = {
    'total': len(pdf_files),
    'successful': 0,
    'failed': 0,
    'total_chars': 0,
    'total_pages': 0,
    'total_time': 0,
    'errors': [],
    'files': []
}

start_batch = time.time()

for i, pdf_file in enumerate(pdf_files, 1):
    pdf_path = os.path.join(RAW_PDF_DIR, pdf_file)
    output_file = os.path.join(OUTPUT_DIR, pdf_file.replace('.pdf', '.txt'))
    
    try:
        start = time.time()
        text = ""
        
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        
        for page_num, page in enumerate(doc):
            page_text = page.get_text()
            if page_text:
                text += f"\n--- Page {page_num + 1} ---\n" + page_text
        
        doc.close()
        elapsed = time.time() - start
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        char_count = len(text)
        stats['successful'] += 1
        stats['total_chars'] += char_count
        stats['total_pages'] += page_count
        stats['total_time'] += elapsed
        
        stats['files'].append({
            'filename': pdf_file,
            'pages': page_count,
            'chars': char_count,
            'time': elapsed
        })
        
        # Progress indicator
        status = "✓"
        print(f"[{i:3d}/{len(pdf_files)}] {status} {pdf_file:50s} | {page_count:3d}p | {char_count:8d}c | {elapsed:6.3f}s")
        
    except Exception as e:
        stats['failed'] += 1
        error_msg = str(e)[:100]
        stats['errors'].append({
            'filename': pdf_file,
            'error': error_msg
        })
        print(f"[{i:3d}/{len(pdf_files)}] ✗ {pdf_file:50s} | ERROR: {error_msg}")

elapsed_batch = time.time() - start_batch

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("BATCH CONVERSION SUMMARY")
print("=" * 70)
print(f"Total PDFs: {stats['total']}")
print(f"Successful: {stats['successful']}")
print(f"Failed: {stats['failed']}")
print(f"Success Rate: {stats['successful']/stats['total']*100:.1f}%")
print(f"Total Characters: {stats['total_chars']:,}")
print(f"Total Pages: {stats['total_pages']:,}")
print(f"Total Time: {stats['total_time']:.2f}s")
print(f"Batch Time: {elapsed_batch:.2f}s")
print(f"Avg Time per PDF: {stats['total_time']/stats['successful']:.3f}s")

# ============================================================================
# Compare with regex extraction where available
# ============================================================================
print("\n" + "=" * 70)
print("COMPARISON WITH MANUAL REGEX EXTRACTION")
print("=" * 70)

comparison_stats = {
    'total_compared': 0,
    'matches': [],
    'differences': []
}

regex_files = [f for f in os.listdir(REGEX_DIR) if f.endswith('.txt')]

for regex_file in regex_files:
    # Try to find corresponding PDF
    pdf_name = regex_file.replace('pdf_', '').replace('_github.txt', '.pdf')
    
    # Handle special naming
    if regex_file.startswith('mryndzionek'):
        pdf_name = regex_file.replace('mryndzionek_tlaplus_specs_', '').replace('_github.txt', '.pdf')
    elif regex_file.startswith('nano-o'):
        pdf_name = 'MultiPaxos.pdf'
    
    pdf_path = os.path.join(RAW_PDF_DIR, pdf_name)
    
    if os.path.exists(pdf_path):
        pymupdf_file = os.path.join(OUTPUT_DIR, pdf_name.replace('.pdf', '.txt'))
        regex_path = os.path.join(REGEX_DIR, regex_file)
        
        if os.path.exists(pymupdf_file):
            with open(pymupdf_file, 'r', encoding='utf-8', errors='ignore') as f:
                pymupdf_text = f.read()
            
            with open(regex_path, 'r', encoding='utf-8', errors='ignore') as f:
                regex_text = f.read()
            
            pymupdf_chars = len(pymupdf_text)
            regex_chars = len(regex_text)
            char_diff = abs(pymupdf_chars - regex_chars)
            char_diff_pct = (char_diff / max(pymupdf_chars, regex_chars)) * 100 if max(pymupdf_chars, regex_chars) > 0 else 0
            
            comparison_stats['total_compared'] += 1
            
            if char_diff_pct < 10:
                status = "SIMILAR"
                comparison_stats['matches'].append({
                    'file': pdf_name,
                    'pymupdf_chars': pymupdf_chars,
                    'regex_chars': regex_chars,
                    'diff_pct': char_diff_pct
                })
            else:
                status = "DIFFERENT"
                comparison_stats['differences'].append({
                    'file': pdf_name,
                    'pymupdf_chars': pymupdf_chars,
                    'regex_chars': regex_chars,
                    'diff_pct': char_diff_pct
                })
            
            print(f"{status:10s} | {pdf_name:40s} | PyMuPDF: {pymupdf_chars:8d} | Regex: {regex_chars:8d} | Diff: {char_diff_pct:5.1f}%")

print(f"\nTotal Compared: {comparison_stats['total_compared']}")
print(f"Similar: {len(comparison_stats['matches'])}")
print(f"Different: {len(comparison_stats['differences'])}")

# ============================================================================
# Save summary
# ============================================================================
summary = {
    'conversion_stats': stats,
    'comparison_stats': comparison_stats,
    'output_directory': OUTPUT_DIR,
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

with open(os.path.join(OUTPUT_DIR, '_conversion_summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\n📁 Output saved to: {OUTPUT_DIR}")
print(f"📊 Summary saved to: {os.path.join(OUTPUT_DIR, '_conversion_summary.json')}")
