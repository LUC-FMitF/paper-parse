#!/usr/bin/env python3
"""Clean up remaining files by extracting actual content from GitHub UI."""

import re
from pathlib import Path

def extract_github_content(content):
    """Extract meaningful parts from GitHub issue/discussion/org pages."""
    
    # Remove GitHub UI crud
    content = re.sub(r'# Search code, repositories,.*?Cancel Create saved search', '', content, flags=re.DOTALL)
    content = re.sub(r'You signed (in|out).*?refresh your session\.', '', content, flags=re.DOTALL)
    content = re.sub(r'You switched accounts.*?refresh your session\.', '', content, flags=re.DOTALL)
    content = re.sub(r'Dismiss alert.*?You must be signed in', '', content, flags=re.DOTALL)
    content = re.sub(r'## Labels.*?### Development', '', content, flags=re.DOTALL)
    content = re.sub(r'## Metadata.*?### Development', '', content, flags=re.DOTALL)
    content = re.sub(r'## Folders and files.*?## History', '', content, flags=re.DOTALL)
    content = re.sub(r'## Latest commit.*?## Repository', '', content, flags=re.DOTALL)
    content = re.sub(r'No branches or pull requests.*', '', content, flags=re.DOTALL)
    content = re.sub(r'## Popular repositories.*?(Loading|No releases)', 'Loading', content, flags=re.DOTALL)
    content = re.sub(r'### Resources.*?### License.*?### Uh oh', '', content, flags=re.DOTALL)
    content = re.sub(r'### License.*?### Uh oh', '', content, flags=re.DOTALL)
    content = re.sub(r'### Uh oh!.*?### Stars', '', content, flags=re.DOTALL)
    content = re.sub(r'### Stars.*?## Languages', '', content, flags=re.DOTALL)
    content = re.sub(r'## Languages.*?\(C\) 2026', '', content, flags=re.DOTALL)
    content = re.sub(r'\(C\) 2026 GitHub, Inc\..*', '', content, flags=re.DOTALL)
    content = re.sub(r'(You can\'t perform that action|You must be signed in|Do not share).*', '', content, flags=re.DOTALL)
    
    # Clean up remaining markdown crud
    content = re.sub(r'\[\]\(\)', '', content)  # Stray empty links
    content = re.sub(r'Loading\n+', '', content)
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)  # Excessive blank lines
    
    return content.strip()

def clean_remaining_files():
    """Clean the remaining problematic files."""
    links_dir = Path('/home/espencer2/Papers-dataset/scraped_pdfs/external_links')
    
    problem_files = [
        'web_9.txt',
        'web_LMAX-Exchange.txt',
        'web_Paxos.txt',
        'web_TypeDefinition.txt',
        'web_sudogandhi.txt',
        'web_tlaplus_specs.txt',
    ]
    
    for filename in problem_files:
        file_path = links_dir / filename
        if not file_path.exists():
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        lines = content.split('\n')
        source_url = None
        final_url = None
        
        for line in lines:
            if line.startswith('Source URL:'):
                source_url = line
            elif line.startswith('Final URL:'):
                final_url = line
        
        # Get body
        body_start = 0
        for i, line in enumerate(lines):
            if '=' * 10 in line:
                body_start = i + 1
                break
        
        body = '\n'.join(lines[body_start:])
        
        # Clean
        body = extract_github_content(body)
        
        # Measure
        if len(body.strip()) < 100:
            print(f"✗ {filename:40s} - Still too small ({len(body)} chars)")
            continue
        
        # Reconstruct
        output = []
        if source_url:
            output.append(source_url)
        if final_url:
            output.append(final_url)
        output.append('=' * 80)
        output.append('')
        output.append(body)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output))
        
        print(f"✓ {filename:40s} - Cleaned ({len(body)} chars)")

if __name__ == '__main__':
    clean_remaining_files()
