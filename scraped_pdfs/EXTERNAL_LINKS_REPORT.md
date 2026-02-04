# External Links Scraping Report

## Summary

Successfully scraped 38 external links referenced in the Comment Ratios Dataset comments. These include academic resources, GitHub repositories, documentation sites, and more.

## Statistics

- **Total links processed**: 53
- **Successfully scraped**: 38 (71.7%)
- **Failed** (access denied/404): 10 (18.9%)
- **Skipped** (videos, already scraped PDFs): 5 (9.4%)
- **Total size**: 6.3 MB

## Scraped Content Types

### Academic Resources & Documentation (✓ 18 items)
1. **Lamport's Publications**
   - `web_pubs_html.txt` - Lamport's publication list
   - `web_byzpaxos_html.txt` - Byzantine Paxos documentation
   - `web_hyperbook_html.txt` - TLA+ Hyperbook
   - `web_toolbox_html.txt` - TLA+ Toolbox documentation

2. **Blog Posts & Research**
   - `web_ahelwer_ca.txt` - Andrew Helwer's pseudocode post
   - `web_2023-04-05-checkpoint-coordination.txt` - Checkpoint coordination article
   - `web_practical-MultiPaxos-TLA-spec_html.txt` - Practical MultiPaxos guide
   - `web_DADA_html.txt` - DADA protocol research
   - `web_www_microsoft_com.txt` - Microsoft Research Fast Paxos publication

3. **Springer & IEEE Papers**
   - `web_BF01667080.txt` - Springer article (10.1007/BF01667080)
   - `web_3-540-44743-1_4.txt` - Springer chapter (3-540-44743-1_4)
   - `web_978-3-540-87779-0_30.txt` - Springer chapter (978-3-540-87779-0_30)
   - `web_ieeexplore_ieee_org.txt` - IEEE papers (2 documents)

### GitHub Repositories (✓ 14 items)
1. **TLA+ Specifications**
   - `web_tlaplus_specs.txt` - TLA+ specs collection (Chameneos, CigaretteSmokers, etc.)
   - `web_raft_tla.txt` - Raft consensus algorithm TLA+ spec
   - `web_DiskPaxos_tla.txt` - Disk Paxos TLA+ spec
   - `web_Paxos.txt` - Paxos TLA+ examples
   - `web_BufferedRandomAccessFile_tla.txt` - Java buffering specification
   - `web_spanning.txt` - Spanning tree TLA+ benchmarks

2. **Implementation & Tools**
   - `web_MultiPaxos.txt` - MultiPaxos implementation
   - `web_RSL.txt` - Azure's Replica State Library
   - `web_RingMaster.txt` - Azure RingMaster
   - `web_LMAX-Exchange.txt` - LMAX Exchange Disruptor pattern
   - `web_disruptor-rs.txt` - Rust Disruptor implementation
   - `web_byihive.txt` - ByiSystems Byihive project
   - `web_summerset.txt` - Distributed state machine
   - `web_TypeDefinition.txt` - Type definition repository
   - `web_BufferedRandomAccessFile_java.txt` - Java implementation
   - `web_sudogandhi.txt` - Developer's TLA+ examples
   - `web_9.txt` - TLA+ Examples issue #9

### General References (✓ 6 items)
1. **Wikipedia Articles**
   - `web_Klotski.txt` - Klotski sliding puzzle
   - `web_Sliding_puzzle.txt` - Sliding puzzle reference
   - `web_Tower_of_Hanoi.txt` - Tower of Hanoi reference

2. **Other Academic Sites**
   - `web_members_loria_fr.txt` - LORIA academic materials

## Failed Retrievals (10 items)

These links returned access denied or 404 errors:

1. `http://lamport.azurewebsites.net/pubs/interprocess` - 404 Not Found
2. `http://lamport.azurewebsites.net/pubs/teaching-con` - 404 Not Found
3. `http://lamport.azurewebsites.net/tla/proving-safety` - 404 Not Found
4. `http://lamport.azurewebsites.net/tla/two-phase.htm` - 404 Not Found
5. `https://dl.acm.org/citation.cfm?id=214134` - 403 Forbidden (requires ACM membership)
6. `https://dl.acm.org/citation.cfm?id=226647` - 403 Forbidden (requires ACM membership)
7. `https://dl.acm.org/citation.cfm?id=302436` - 403 Forbidden (requires ACM membership)
8. `https://dl.acm.org/doi/10.1145/3087801.3087802` - 403 Forbidden (requires ACM membership)
9. `https://www.cs.utexas.edu/users/EWD/ewd09xx/EWD998` - 404 Not Found
10. `https://www.researchgate.net/publication/271910927_Fast_Paxos_Made_Easy_Theory_and_Implementation` - 403 Forbidden

## Skipped Items (5 items)

1. `https://cedric.cnam.fr/fichiers/RC474.pdf` - Already scraped as PDF
2. `https://raft.github.io/raft.pdf` - Already scraped as PDF
3. `https://lamport.azurewebsites.net/pubs/disk-paxos.pdf` - Already scraped as PDF
4. `https://www.youtube.com/watch?v=cYenTPD7740` - Video (cannot scrape)
5. `https://youtu.be/_GP9OpZPUYc?t=742` - Video (cannot scrape)

## Directory Structure

```
/home/espencer2/Papers-dataset/scraped_pdfs/
├── (original 3 PDF files - 548 KB)
├── README.md
├── _pdf_inventory.txt
├── _verification_report.txt
└── external_links/
    ├── web_*.txt (38 HTML/text files - 6.3 MB)
    └── ...
```

## Total Dataset

- **PDFs converted to text**: 6 files (548 KB)
- **External links downloaded**: 38 files (6.3 MB)
- **Total size**: ~6.8 MB
- **Total number of files**: 48

## File Format

Each scraped file includes:
```
Source URL: <original URL>
Final URL: <redirected URL if applicable>
================================================================================

<full content from the page/resource>
```

## Usage Notes

- **ACM Digital Library links** require institutional access
- **IEEE Xplore links** require subscription
- **ResearchGate links** may require account login
- **YouTube videos** are referenced but not downloadable
- Some **Lamport website links** appear to have changed/moved (404 errors)

## What You Can Do With This Data

1. **Training Data**: Use as context for LLM fine-tuning on formal verification
2. **Research**: Cross-reference implementations with specifications
3. **Learning**: Follow along with blog posts and tutorials
4. **Citation**: Collect references for academic papers
5. **Source Code**: Access GitHub repositories for implementations

## Generated Files

- `scrape_additional_links.py` - Script to download and convert links
- This report - Comprehensive summary of results

## Notes

- All successfully downloaded content is plain text (HTML converted to text)
- GitHub repository pages are captured with markdown content
- Springer and IEEE pages captured with abstracts and metadata
- Wikipedia articles captured in full
- No PDFs were forcefully converted; only PDF links directly provided as PDFs were converted

---

**Last Updated**: February 4, 2026  
**Location**: `/home/espencer2/Papers-dataset/scraped_pdfs/external_links/`
