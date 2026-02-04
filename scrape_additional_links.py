#!/usr/bin/env python3
"""
Scrape additional links from the verification report.
Handles:
- PDF links
- HTML pages and blog posts
- GitHub repositories
- Academic paper citations
- Wikipedia articles
- Documentation sites
"""

import os
import sys
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re
from pathlib import Path

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    from PyPDF2 import PdfReader
    HAS_PYPDF2 = True
except ImportError:
    try:
        from pypdf import PdfReader
        HAS_PYPDF2 = True
    except ImportError:
        HAS_PYPDF2 = False

# All links from the verification report
LINKS = [
    "http://lamport.azurewebsites.net/pubs/interprocess",
    "http://lamport.azurewebsites.net/pubs/pubs.html#di...",
    "http://lamport.azurewebsites.net/pubs/teaching-con",
    "http://lamport.azurewebsites.net/tla/byzpaxos.html",
    "http://lamport.azurewebsites.net/tla/hyperbook.html",
    "http://lamport.azurewebsites.net/tla/proving-safety",
    "http://lamport.azurewebsites.net/tla/two-phase.htm...",
    "http://research.microsoft.com/en-us/um/people/lamport/pubs/pubs.html#paxos-commit",
    "https://ahelwer.ca/post/2023-03-30-pseudocode/",
    "https://ahelwer.ca/post/2023-04-05-checkpoint-coordination;",
    "https://cedric.cnam.fr/fichiers/RC474.pdf",
    "https://dl.acm.org/citation.cfm?id=214134",
    "https://dl.acm.org/citation.cfm?id=226647",
    "https://dl.acm.org/citation.cfm?id=302436",
    "https://dl.acm.org/doi/10.1145/3087801.3087802",
    "https://en.wikipedia.org/wiki/Klotski;",
    "https://en.wikipedia.org/wiki/Sliding_puzzle;",
    "https://en.wikipedia.org/wiki/Tower_of_Hanoi;",
    "https://github.com/Azure/RSL;",
    "https://github.com/Azure/RingMaster",
    "https://github.com/LMAX-Exchange;",
    "https://github.com/TypeDefinition;",
    "https://github.com/banhday/tlabenchmarks/tree/master/benchmarks/spanning",
    "https://github.com/byisystems/byihive.",
    "https://github.com/josehu07/summerset;",
    "https://github.com/josehu07/tla-examples/tree/master/specifications/Paxos",
    "https://github.com/mryndzionek/tlaplus_specs#chameneostla",
    "https://github.com/mryndzionek/tlaplus_specs#cigarettesmokerstla",
    "https://github.com/mryndzionek/tlaplus_specs#slidingpuzzlestla;",
    "https://github.com/nano-o/MultiPaxos/blob/master/DiskPaxos.tla",
    "https://github.com/nano-o/MultiPaxos;",
    "https://github.com/nicholassm/disruptor-rs",
    "https://github.com/ongardie/raft.tla;",
    "https://github.com/sudogandhi;",
    "https://github.com/tlaplus/Examples/issues/9",
    "https://github.com/tlaplus/tlaplus/blob/4613109641676389d97b8df209d6cf4d90d31c1c/tlatools/org.lamport.tlatools/src/tlc2/util/BufferedRandomAccessFile.java",
    "https://github.com/tlaplus/tlaplus/tree/4613109641676389d97b8df209d6cf4d90d31c1c/tlatools/org.lamport.tlatools/src/tlc2/util/BufferedRandomAccessFile.tla;",
    "https://ieeexplore.ieee.org/abstract/document/1633503/",
    "https://ieeexplore.ieee.org/document/1209964/",
    "https://lamport.azurewebsites.net/pubs/disk-paxos.pdf;",
    "https://lamport.azurewebsites.net/tla/toolbox.html",
    "https://link.springer.com/article/10.1007/BF01667080",
    "https://link.springer.com/chapter/10.1007/3-540-44743-1_4",
    "https://link.springer.com/chapter/10.1007/978-3-540-87779-0_30",
    "https://members.loria.fr/SMerz/talks/argentina2005/Charpentier/charpov/Teaching/CS-986/TLC/;",
    "https://raft.github.io/raft.pdf",
    "https://research.nicola-santoro.com/DADA.html",
    "https://www.cs.utexas.edu/users/EWD/ewd09xx/EWD998...",
    "https://www.josehu.com/technical/2024/02/19/practical-MultiPaxos-TLA-spec.html;",
    "https://www.microsoft.com/en-us/research/publication/fast-paxos/",
    "https://www.researchgate.net/publication/271910927_Fast_Paxos_Made_Easy_Theory_and_Implementation;",
    "https://www.youtube.com/watch?v=cYenTPD7740",
    "https://youtu.be/_GP9OpZPUYc?t=742",
]


def clean_url(url):
    """Clean URL by removing trailing punctuation and ellipsis"""
    url = url.rstrip(';')
    url = url.rstrip('.')
    if url.endswith('...'):
        # Try to guess the full extension
        if 'pubs.html#di' in url:
            url = url.replace('...', 'stributed-systems/')
        elif 'teaching-con' in url:
            url = url.replace('...', 'currency.html')
        elif 'two-phase.htm' in url:
            url = url.replace('...', 'l')
        elif 'EWD998' in url:
            url = url.replace('...', 'aaa/EWD998.txt')
    return url


def fetch_url(url, timeout=30):
    """Fetch content from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        return response.content, response.url
    except Exception as e:
        print(f"  ✗ Error fetching {url}: {e}")
        return None, None


def is_pdf_content(content):
    """Check if content is PDF"""
    return content[:4] == b'%PDF'


def extract_pdf_text(content):
    """Extract text from PDF content"""
    try:
        from io import BytesIO
        pdf_file = BytesIO(content)
        
        if HAS_PDFPLUMBER:
            import pdfplumber
            with pdfplumber.open(pdf_file) as pdf:
                text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return '\n\n'.join(text)
        elif HAS_PYPDF2:
            reader = PdfReader(pdf_file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            return '\n\n'.join(text)
    except Exception as e:
        print(f"  ! Could not extract PDF: {e}")
    return None


def sanitize_filename(url):
    """Create safe filename from URL"""
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path) or parsed.netloc
    filename = re.sub(r'[^\w\-_]', '_', filename)
    return filename[:100]


def scrape_link(url, output_dir):
    """Scrape a single link"""
    url = clean_url(url)
    
    print(f"\nProcessing: {url}")
    
    content, final_url = fetch_url(url)
    if not content:
        return False
    
    # Determine file type and save
    if is_pdf_content(content):
        print(f"  ✓ PDF detected")
        text = extract_pdf_text(content)
        if text:
            filename = f"pdf_{sanitize_filename(url)}.txt"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
                f.write(f"Source URL: {url}\n")
                f.write(f"Final URL: {final_url}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
            print(f"  ✓ Saved: {filename} ({len(text)} chars)")
            return True
    else:
        # Save as HTML/text
        try:
            text = content.decode('utf-8', errors='replace')
            filename = f"web_{sanitize_filename(url)}.txt"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Source URL: {url}\n")
                f.write(f"Final URL: {final_url}\n")
                f.write(f"{'='*80}\n\n")
                f.write(text)
            print(f"  ✓ Saved: {filename} ({len(text)} chars)")
            return True
        except Exception as e:
            print(f"  ✗ Error saving content: {e}")
    
    return False


def main():
    output_dir = '/home/espencer2/Papers-dataset/scraped_pdfs/external_links'
    os.makedirs(output_dir, exist_ok=True)
    
    print("="*80)
    print("Scraping Additional External Links")
    print("="*80)
    print(f"Total links to process: {len(LINKS)}")
    print(f"Output directory: {output_dir}\n")
    
    successful = 0
    failed = 0
    skipped = 0
    
    for url in LINKS:
        # Skip certain types
        if url.startswith('https://www.youtube.com') or url.startswith('https://youtu.be'):
            print(f"\nSkipping (video): {url}")
            skipped += 1
            continue
        
        # Skip already scraped PDFs
        if url == "https://cedric.cnam.fr/fichiers/RC474.pdf" or \
           url == "https://raft.github.io/raft.pdf" or \
           url == "https://lamport.azurewebsites.net/pubs/disk-paxos.pdf;":
            print(f"\nSkipping (already scraped): {url}")
            skipped += 1
            continue
        
        if scrape_link(url, output_dir):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Total: {successful + failed + skipped}")
    print(f"\nOutput: {output_dir}")


if __name__ == '__main__':
    main()
