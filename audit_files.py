#!/usr/bin/env python3
"""
Re-download GitHub files using raw.githubusercontent.com to get actual code.
Also identify and handle other problem cases.
"""

import requests
import re
from pathlib import Path
from urllib.parse import urlparse

# Map of GitHub URLs to raw content URLs
GITHUB_FILES = {
    'https://github.com/tlaplus/Examples/issues/9': 
        'https://github.com/tlaplus/Examples/issues/9',  # Discussion - keep
    'https://github.com/nano-o/MultiPaxos/blob/master/DiskPaxos.tla':
        'https://raw.githubusercontent.com/nano-o/MultiPaxos/master/DiskPaxos.tla',
    'https://github.com/ongardie/raft.tla':
        'https://raw.githubusercontent.com/ongardie/master/raft.tla',
    'https://github.com/josehu07/tla-examples/tree/master/specifications/Paxos':
        'https://raw.githubusercontent.com/josehu07/tla-examples/master/specifications/Paxos.tla',
    'https://github.com/thanh-hai-tran/tlabenchmarks/tree/master/benchmarks/spanning':
        'https://raw.githubusercontent.com/thanh-hai-tran/tlabenchmarks/master/benchmarks/spanning/spanning.tla',
}

def convert_github_url(url):
    """Convert GitHub web URL to raw.githubusercontent.com URL."""
    if 'raw.githubusercontent.com' in url:
        return url  # Already raw
    
    if 'github.com' not in url:
        return None
    
    # Pattern: github.com/user/repo/blob/branch/path
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)', url)
    if match:
        user, repo, branch, path = match.groups()
        return f'https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}'
    
    # Pattern: github.com/user/repo/tree/branch/path (directory)
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)', url)
    if match:
        user, repo, branch, path = match.groups()
        # Try to get main file in directory
        return f'https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}/README.md'
    
    return None

def fetch_url(url, timeout=10):
    """Fetch URL content with headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        return None

def audit_and_fix():
    """Check all files and re-download problematic ones."""
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    
    results = {
        'good': [],
        'github_ui': [],
        'paywalled': [],
        'empty': [],
        'fixable': []
    }
    
    for file_path in sorted(links_dir.glob('web_*.txt')):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract URL
        final_url_line = [l for l in content.split('\n') if l.startswith('Final URL:')]
        if not final_url_line:
            results['empty'].append(file_path.name)
            continue
        
        final_url = final_url_line[0].replace('Final URL:', '').strip()
        
        # Get body
        body = content.split('=' * 10, 1)[1].strip() if '=' * 10 in content else ''
        
        # Classify
        if len(body) < 150:
            if 'github' in final_url.lower():
                results['github_ui'].append({
                    'file': file_path.name,
                    'url': final_url,
                    'size': len(body)
                })
            elif 'ieee' in final_url.lower() or 'springer' in final_url.lower():
                results['paywalled'].append({
                    'file': file_path.name,
                    'url': final_url
                })
            else:
                results['empty'].append({
                    'file': file_path.name,
                    'url': final_url,
                    'size': len(body)
                })
        elif 'github.com' in final_url and 'Search code' in body:
            results['github_ui'].append({
                'file': file_path.name,
                'url': final_url,
                'size': len(body)
            })
        else:
            results['good'].append({
                'file': file_path.name,
                'url': final_url,
                'size': len(body)
            })
    
    return results

def main():
    print("AUDITING EXTERNAL LINKS DATASET")
    print("=" * 80)
    
    results = audit_and_fix()
    
    print(f"\n✓ GOOD FILES: {len(results['good'])}")
    for item in results['good'][:5]:
        print(f"  • {item['file']:40s} ({item['size']:5d}B)")
    if len(results['good']) > 5:
        print(f"  ... and {len(results['good']) - 5} more")
    
    print(f"\n⚠ GITHUB UI ISSUES: {len(results['github_ui'])}")
    for item in results['github_ui']:
        print(f"  • {item['file']:40s} ({item['size']:5d}B)")
        print(f"    URL: {item['url'][:70]}")
    
    print(f"\n✗ PAYWALLED (Can't Fix): {len(results['paywalled'])}")
    for item in results['paywalled']:
        print(f"  • {item['file']:40s}")
        print(f"    URL: {item['url'][:70]}")
    
    print(f"\n✗ EMPTY/MINIMAL: {len(results['empty'])}")
    for item in results['empty']:
        if isinstance(item, dict):
            print(f"  • {item['file']:40s} ({item.get('size', 0):5d}B)")
        else:
            print(f"  • {item}")
    
    print(f"\n{'='*80}")
    print(f"SUMMARY:")
    print(f"  Good:       {len(results['good']):2d}")
    print(f"  GitHub UI:  {len(results['github_ui']):2d} (can potentially fix)")
    print(f"  Paywalled:  {len(results['paywalled']):2d} (delete)")
    print(f"  Empty:      {len(results['empty']):2d} (review)")
    print(f"  TOTAL:      {sum(len(v) if isinstance(v, list) else len(v) for v in results.values()):2d}")

if __name__ == '__main__':
    main()
