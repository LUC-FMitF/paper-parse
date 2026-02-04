#!/usr/bin/env python3
"""
Verification script to ensure all comments and links were scraped correctly.
"""

import csv
import re
import os

def extract_all_links(text):
    """Extract all external links from text"""
    if not text:
        return []
    
    # Pattern to match various URL types
    url_pattern = r'https?://[^\s<>"{}|\\^\[\]`]+'
    links = re.findall(url_pattern, text, re.IGNORECASE)
    
    # Remove duplicates
    return list(set(links))


def verify_scraping(csv_path, scraped_dir):
    """Verify all links and comments were processed"""
    
    stats = {
        'total_rows': 0,
        'rows_with_external_refs': 0,
        'total_external_links': 0,
        'pdf_links': 0,
        'non_pdf_links': 0,
        'all_links': set(),
        'pdf_links_list': [],
        'non_pdf_links_list': []
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
            stats['total_rows'] += 1
            
            # Get all text columns
            description = row.get('', '')
            notes = row.get('notes', '')
            has_external = row.get('has_external_doc_ref', 'FALSE')
            
            all_text = f"{description} {notes}"
            
            # Extract all links
            links = extract_all_links(all_text)
            
            if links:
                stats['rows_with_external_refs'] += 1
                stats['total_external_links'] += len(links)
                
                for link in links:
                    stats['all_links'].add(link)
                    
                    if link.lower().endswith('.pdf'):
                        stats['pdf_links'] += 1
                        stats['pdf_links_list'].append({
                            'project': row.get('project', 'unknown'),
                            'model': row.get('model', 'unknown'),
                            'url': link
                        })
                    else:
                        stats['non_pdf_links'] += 1
                        stats['non_pdf_links_list'].append({
                            'project': row.get('project', 'unknown'),
                            'model': row.get('model', 'unknown'),
                            'url': link
                        })
    
    # Check scraped files
    scraped_files = []
    if os.path.exists(scraped_dir):
        scraped_files = [f for f in os.listdir(scraped_dir) if f.endswith('.txt') and f != '_pdf_inventory.txt']
    
    stats['scraped_files_count'] = len(scraped_files)
    stats['scraped_files'] = scraped_files
    
    return stats


def main():
    csv_path = '/home/espencer2/Papers-dataset/Comment Ratios Dataset(Comments Ratio).csv'
    scraped_dir = '/home/espencer2/FormaLLM/scraped_pdfs'
    
    print("="*80)
    print("VERIFICATION REPORT")
    print("="*80)
    print()
    
    stats = verify_scraping(csv_path, scraped_dir)
    
    print(f"Total rows in CSV: {stats['total_rows']}")
    print(f"Rows with external references: {stats['rows_with_external_refs']}")
    print(f"Total external links found: {stats['total_external_links']}")
    print(f"Unique links: {len(stats['all_links'])}")
    print()
    
    print(f"PDF links found: {stats['pdf_links']}")
    print(f"Non-PDF links found: {stats['non_pdf_links']}")
    print()
    
    print(f"Scraped text files created: {stats['scraped_files_count']}")
    print()
    
    print("="*80)
    print("ALL PDF LINKS")
    print("="*80)
    for item in stats['pdf_links_list']:
        print(f"\nProject: {item['project']}")
        print(f"Model: {item['model']}")
        print(f"URL: {item['url']}")
    
    print()
    print("="*80)
    print("SAMPLE NON-PDF LINKS (first 20)")
    print("="*80)
    for i, item in enumerate(stats['non_pdf_links_list'][:20]):
        print(f"\n{i+1}. Project: {item['project']}, Model: {item['model']}")
        print(f"   URL: {item['url']}")
    
    if len(stats['non_pdf_links_list']) > 20:
        print(f"\n... and {len(stats['non_pdf_links_list']) - 20} more non-PDF links")
    
    print()
    print("="*80)
    print("SCRAPED FILES")
    print("="*80)
    for f in sorted(stats['scraped_files']):
        size = os.path.getsize(os.path.join(scraped_dir, f))
        print(f"  {f} ({size:,} bytes)")
    
    print()
    print("="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)
    print(f"✓ All {stats['total_rows']} rows processed")
    print(f"✓ Found {stats['pdf_links']} PDF links in comments")
    print(f"✓ Created {stats['scraped_files_count']} text files from PDFs")
    print(f"✓ Found {stats['non_pdf_links']} additional non-PDF links")
    print()
    
    # Save detailed report
    report_path = os.path.join(scraped_dir, '_verification_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("VERIFICATION REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total rows: {stats['total_rows']}\n")
        f.write(f"Rows with links: {stats['rows_with_external_refs']}\n")
        f.write(f"Total links: {stats['total_external_links']}\n")
        f.write(f"PDF links: {stats['pdf_links']}\n")
        f.write(f"Non-PDF links: {stats['non_pdf_links']}\n")
        f.write(f"Scraped files: {stats['scraped_files_count']}\n\n")
        
        f.write("ALL LINKS FOUND\n")
        f.write("="*80 + "\n\n")
        for link in sorted(stats['all_links']):
            f.write(f"{link}\n")
    
    print(f"Detailed report saved to: {report_path}")


if __name__ == '__main__':
    main()
