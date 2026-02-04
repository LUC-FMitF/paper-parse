#!/usr/bin/env python3
"""
Re-download GitHub files using raw.githubusercontent.com for actual code.
"""

import requests
import re
from pathlib import Path
import time

def convert_github_to_raw(url):
    """Convert GitHub web URL to raw.githubusercontent.com URL."""
    if 'raw.githubusercontent.com' in url:
        return url
    
    if 'github.com' not in url:
        return None
    
    # blob URLs: github.com/user/repo/blob/branch/path
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)', url)
    if match:
        user, repo, branch, path = match.groups()
        return f'https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}'
    
    # tree URLs: github.com/user/repo/tree/branch/path
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)', url)
    if match:
        user, repo, branch, path = match.groups()
        # Try README first, then the path as a file
        raw_url = f'https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}/README.md'
        return raw_url
    
    # Just repo: github.com/user/repo
    match = re.match(r'https://github\.com/([^/]+)/([^/]+)/?$', url)
    if match:
        user, repo = match.groups()
        return f'https://raw.githubusercontent.com/{user}/{repo}/master/README.md'
    
    return None

def fetch_content(url, timeout=10):
    """Fetch content with proper headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Accept': 'text/plain,*/*'
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        pass
    return None

def fix_github_file(file_path):
    """Try to fix a GitHub file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get URL
    lines = content.split('\n')
    final_url = None
    source_url = None
    
    for line in lines:
        if line.startswith('Final URL:'):
            final_url = line.replace('Final URL:', '').strip()
        elif line.startswith('Source URL:'):
            source_url = line.replace('Source URL:', '').strip()
    
    if not final_url:
        return False, 'No URL'
    
    # Check if it's GitHub
    if 'github.com' not in final_url:
        return False, 'Not GitHub'
    
    # Already contains code?
    body = content.split('=' * 10, 1)[1] if '=' * 10 in content else ''
    if 'Search code' not in body and len(body) > 1000:
        return False, 'Already good'
    
    # Convert to raw URL
    raw_url = convert_github_to_raw(final_url)
    if not raw_url:
        return False, f'Cannot convert URL'
    
    # Fetch raw content
    raw_content = fetch_content(raw_url)
    
    if not raw_content or len(raw_content) < 100:
        # Try alternate approaches
        if '/blob/' in final_url:
            # It's a file, try as-is
            alt_url = raw_url.replace('blob/', '')
            raw_content = fetch_content(alt_url)
        
        if not raw_content or len(raw_content) < 100:
            return False, f'Fetch failed or empty (tried {raw_url})'
    
    # Write back with metadata
    output = f'Source URL: {source_url or final_url}\n'
    output += f'Final URL: {final_url}\n'
    output += '=' * 80 + '\n\n'
    output += raw_content.strip()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return True, f'Fixed ({len(raw_content)} bytes)'

def main():
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    
    # List of files with GitHub UI issues to fix
    github_files = [
        'web_9.txt',
        'web_BufferedRandomAccessFile_java.txt',
        'web_BufferedRandomAccessFile_tla.txt',
        'web_DiskPaxos_tla.txt',
        'web_LMAX-Exchange.txt',
        'web_MultiPaxos.txt',
        'web_Paxos.txt',
        'web_RSL.txt',
        'web_RingMaster.txt',
        'web_TypeDefinition.txt',
        'web_byihive.txt',
        'web_disruptor-rs.txt',
        'web_raft_tla.txt',
        'web_spanning.txt',
        'web_sudogandhi.txt',
        'web_summerset.txt',
        'web_tlaplus_specs.txt',
    ]
    
    print(f"Attempting to fix {len(github_files)} GitHub files...\n")
    
    fixed = 0
    failed = []
    
    for filename in github_files:
        file_path = links_dir / filename
        if not file_path.exists():
            continue
        
        success, msg = fix_github_file(file_path)
        
        if success:
            print(f"✓ {filename:40s} {msg}")
            fixed += 1
        else:
            print(f"✗ {filename:40s} {msg}")
            failed.append((filename, msg))
        
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n{'='*80}")
    print(f"Results: {fixed} fixed, {len(failed)} failed")
    
    if failed and fixed < len(github_files) / 2:
        print("\nFailed files:")
        for filename, msg in failed:
            print(f"  • {filename}: {msg}")

if __name__ == '__main__':
    main()
