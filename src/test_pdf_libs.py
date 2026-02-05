#!/usr/bin/env python3
"""
Test three different Python libraries for PDF to text conversion.
Compare effectiveness on sample PDFs from the Papers-dataset.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Tuple, Any

# Test PDF path
TEST_PDF_DIR = "/home/espencer2/Papers-dataset/scraped_pdfs/raw"
OUTPUT_DIR = "/home/espencer2/Papers-dataset/test_results"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get first 3 PDFs for testing
pdf_files = sorted([f for f in os.listdir(TEST_PDF_DIR) if f.endswith('.pdf')])[:3]
print(f"Testing with PDFs: {pdf_files}\n")

results = {
    'pdfplumber': {'success': 0, 'errors': [], 'times': []},
    'pymupdf': {'success': 0, 'errors': [], 'times': []},
    'pdfminer': {'success': 0, 'errors': [], 'times': []},
}

# ============================================================================
# Library 1: pdfplumber
# ============================================================================
print("=" * 70)
print("LIBRARY 1: pdfplumber")
print("=" * 70)
try:
    import pdfplumber
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(TEST_PDF_DIR, pdf_file)
        output_file = os.path.join(OUTPUT_DIR, f"pdfplumber_{pdf_file.replace('.pdf', '.txt')}")
        
        try:
            start = time.time()
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n" + page_text
            elapsed = time.time() - start
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results['pdfplumber']['success'] += 1
            results['pdfplumber']['times'].append(elapsed)
            
            char_count = len(text)
            print(f"✓ {pdf_file}: {len(pdf.pages)} pages, {char_count} chars, {elapsed:.2f}s")
            
        except Exception as e:
            results['pdfplumber']['errors'].append({
                'file': pdf_file,
                'error': str(e)
            })
            print(f"✗ {pdf_file}: {str(e)[:80]}")
            
except ImportError as e:
    print(f"✗ pdfplumber not installed: {e}")
    print("  Installing...")
    os.system("pip install -q pdfplumber")
    # Retry
    import pdfplumber
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(TEST_PDF_DIR, pdf_file)
        output_file = os.path.join(OUTPUT_DIR, f"pdfplumber_{pdf_file.replace('.pdf', '.txt')}")
        
        try:
            start = time.time()
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {i+1} ---\n" + page_text
            elapsed = time.time() - start
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results['pdfplumber']['success'] += 1
            results['pdfplumber']['times'].append(elapsed)
            
            char_count = len(text)
            print(f"✓ {pdf_file}: {len(pdf.pages)} pages, {char_count} chars, {elapsed:.2f}s")
            
        except Exception as e:
            results['pdfplumber']['errors'].append({
                'file': pdf_file,
                'error': str(e)
            })
            print(f"✗ {pdf_file}: {str(e)[:80]}")

# ============================================================================
# Library 2: PyMuPDF (fitz)
# ============================================================================
print("\n" + "=" * 70)
print("LIBRARY 2: PyMuPDF (fitz)")
print("=" * 70)
try:
    import fitz  # PyMuPDF
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(TEST_PDF_DIR, pdf_file)
        output_file = os.path.join(OUTPUT_DIR, f"pymupdf_{pdf_file.replace('.pdf', '.txt')}")
        
        try:
            start = time.time()
            text = ""
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            for i, page in enumerate(doc):
                page_text = page.get_text()
                if page_text:
                    text += f"\n--- Page {i+1} ---\n" + page_text
            elapsed = time.time() - start
            doc.close()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results['pymupdf']['success'] += 1
            results['pymupdf']['times'].append(elapsed)
            
            char_count = len(text)
            print(f"✓ {pdf_file}: {page_count} pages, {char_count} chars, {elapsed:.2f}s")
            
        except Exception as e:
            results['pymupdf']['errors'].append({
                'file': pdf_file,
                'error': str(e)
            })
            print(f"✗ {pdf_file}: {str(e)[:80]}")
            
except ImportError as e:
    print(f"✗ PyMuPDF not installed: {e}")
    print("  Installing...")
    os.system("pip install -q PyMuPDF")
    # Retry
    import fitz
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(TEST_PDF_DIR, pdf_file)
        output_file = os.path.join(OUTPUT_DIR, f"pymupdf_{pdf_file.replace('.pdf', '.txt')}")
        
        try:
            start = time.time()
            text = ""
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            for i, page in enumerate(doc):
                page_text = page.get_text()
                if page_text:
                    text += f"\n--- Page {i+1} ---\n" + page_text
            elapsed = time.time() - start
            doc.close()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results['pymupdf']['success'] += 1
            results['pymupdf']['times'].append(elapsed)
            
            char_count = len(text)
            print(f"✓ {pdf_file}: {page_count} pages, {char_count} chars, {elapsed:.2f}s")
            
        except Exception as e:
            results['pymupdf']['errors'].append({
                'file': pdf_file,
                'error': str(e)
            })
            print(f"✗ {pdf_file}: {str(e)[:80]}")

# ============================================================================
# Library 3: pdfminer.six
# ============================================================================
print("\n" + "=" * 70)
print("LIBRARY 3: pdfminer.six")
print("=" * 70)
try:
    from pdfminer.high_level import extract_text
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(TEST_PDF_DIR, pdf_file)
        output_file = os.path.join(OUTPUT_DIR, f"pdfminer_{pdf_file.replace('.pdf', '.txt')}")
        
        try:
            start = time.time()
            text = extract_text(pdf_path)
            elapsed = time.time() - start
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results['pdfminer']['success'] += 1
            results['pdfminer']['times'].append(elapsed)
            
            char_count = len(text)
            print(f"✓ {pdf_file}: {char_count} chars, {elapsed:.2f}s")
            
        except Exception as e:
            results['pdfminer']['errors'].append({
                'file': pdf_file,
                'error': str(e)
            })
            print(f"✗ {pdf_file}: {str(e)[:80]}")
            
except ImportError as e:
    print(f"✗ pdfminer.six not installed: {e}")
    print("  Installing...")
    os.system("pip install -q pdfminer.six")
    # Retry
    from pdfminer.high_level import extract_text
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(TEST_PDF_DIR, pdf_file)
        output_file = os.path.join(OUTPUT_DIR, f"pdfminer_{pdf_file.replace('.pdf', '.txt')}")
        
        try:
            start = time.time()
            text = extract_text(pdf_path)
            elapsed = time.time() - start
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            results['pdfminer']['success'] += 1
            results['pdfminer']['times'].append(elapsed)
            
            char_count = len(text)
            print(f"✓ {pdf_file}: {char_count} chars, {elapsed:.2f}s")
            
        except Exception as e:
            results['pdfminer']['errors'].append({
                'file': pdf_file,
                'error': str(e)
            })
            print(f"✗ {pdf_file}: {str(e)[:80]}")

# ============================================================================
# Summary Report
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY & RATINGS")
print("=" * 70)

ratings = {}
for lib_name, lib_results in results.items():
    if lib_results['success'] == 0:
        rating = 0
    else:
        success_rate = lib_results['success'] / len(pdf_files)
        avg_time = sum(lib_results['times']) / len(lib_results['times']) if lib_results['times'] else float('inf')
        # Rating: Higher success, lower time = higher rating
        rating = (success_rate * 100) - (avg_time * 10)  # Weighted score
    
    ratings[lib_name] = rating
    
    print(f"\n{lib_name.upper()}:")
    print(f"  Success Rate: {lib_results['success']}/{len(pdf_files)}")
    print(f"  Avg Time: {sum(lib_results['times'])/len(lib_results['times']):.3f}s" if lib_results['times'] else "  Avg Time: N/A")
    print(f"  Rating Score: {rating:.1f}")
    if lib_results['errors']:
        print(f"  Errors: {len(lib_results['errors'])}")

# Rank libraries
ranked = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
print("\n" + "=" * 70)
print("RANKING (Best to Worst):")
print("=" * 70)
for i, (lib, score) in enumerate(ranked, 1):
    print(f"{i}. {lib.upper()} (Score: {score:.1f})")

best_lib = ranked[0][0]
print(f"\n🏆 BEST LIBRARY: {best_lib.upper()}\n")

# Save results to JSON
with open(os.path.join(OUTPUT_DIR, 'comparison_results.json'), 'w') as f:
    json.dump({
        'ratings': ratings,
        'ranked': [(lib, score) for lib, score in ranked],
        'best_library': best_lib,
        'results': results
    }, f, indent=2)

print(f"Results saved to {OUTPUT_DIR}")
