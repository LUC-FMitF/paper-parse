# Scraped PDFs and External Links Index

## Quick Navigation

Start here for understanding what you have:

### 📋 Documentation Files (Read These First)
1. **[COMPLETE_DATASET_SUMMARY.md](COMPLETE_DATASET_SUMMARY.md)** - Comprehensive overview of everything
2. **[EXTERNAL_LINKS_REPORT.md](EXTERNAL_LINKS_REPORT.md)** - Detailed report on 38 scraped external links
3. **[README.md](README.md)** - Directory overview and usage guide

### 📊 Index & Verification Files
- **[_verification_report.txt](_verification_report.txt)** - All 53 unique links found with catalog
- **[_pdf_inventory.txt](_pdf_inventory.txt)** - PDF-to-project mapping

## 📚 Content at a Glance

### Direct PDF Files (6 files, 548 KB)

Three unique academic papers converted to text format:

#### Concurrency & Distributed Systems Papers

| File | Topic | Size |
|------|-------|------|
| `Chameneos_Chameneos_RC474.txt` | Concurrency game (Java, Ada, C/Posix) | 43 KB |
| `diskpaxos_DiskSynod_disk-paxos.txt` | Lamport's Disk Paxos algorithm | 108 KB |
| `diskpaxos_HDiskSynod_disk-paxos.txt` | Lamport's Disk Paxos algorithm | 108 KB |
| `diskpaxos_Synod_disk-paxos.txt` | Lamport's Disk Paxos algorithm | 108 KB |
| `raft_raft_raft.txt` | Raft consensus algorithm | 83 KB |
| `raft_raft_clean_raft.txt` | Raft consensus algorithm | 83 KB |

### External Links (38 files, 6.3 MB)

#### 📚 Academic & Documentation Resources

```
external_links/
├── web_pubs_html.txt                          # Lamport's publications index
├── web_byzpaxos_html.txt                      # Byzantine Paxos spec
├── web_hyperbook_html.txt                     # TLA+ Hyperbook
├── web_toolbox_html.txt                       # TLA+ Toolbox docs
├── web_DADA_html.txt                          # DADA protocol research
├── web_members_loria_fr.txt                   # Academic materials
```

#### 💻 GitHub Repositories (Implementation & Specifications)

```
external_links/
├── web_tlaplus_specs.txt                      # TLA+ specs collection
├── web_raft_tla.txt                           # Raft consensus TLA+
├── web_DiskPaxos_tla.txt                      # Disk Paxos TLA+
├── web_Paxos.txt                              # Paxos examples
├── web_BufferedRandomAccessFile_tla.txt       # Buffer spec
├── web_spanning.txt                           # Spanning tree TLA+
├── web_MultiPaxos.txt                         # MultiPaxos impl
├── web_RSL.txt                                # Azure Replica State Library
├── web_RingMaster.txt                         # Azure RingMaster
├── web_LMAX-Exchange.txt                      # LMAX Disruptor
├── web_disruptor-rs.txt                       # Rust Disruptor
├── web_byihive.txt                            # Byihive project
├── web_summerset.txt                          # Distributed state machine
├── web_sudogandhi.txt                         # TLA+ examples
└── web_TypeDefinition.txt                     # Type definitions
```

#### 📖 Blog Posts & Articles

```
external_links/
├── web_ahelwer_ca.txt                         # Pseudocode blog post
├── web_2023-04-05-checkpoint-coordination.txt # Coordination article
├── web_practical-MultiPaxos-TLA-spec_html.txt # MultiPaxos guide
└── web_www_microsoft_com.txt                  # Microsoft Research
```

#### 📰 Academic Papers (Springer, IEEE, Wikipedia)

```
external_links/
├── web_BF01667080.txt                         # Springer article
├── web_3-540-44743-1_4.txt                    # Springer chapter
├── web_978-3-540-87779-0_30.txt               # Springer chapter
├── web_ieeexplore_ieee_org.txt                # IEEE papers
├── web_Klotski.txt                            # Wikipedia: Klotski
├── web_Sliding_puzzle.txt                     # Wikipedia: Puzzles
├── web_Tower_of_Hanoi.txt                     # Wikipedia: Hanoi
├── web_BufferedRandomAccessFile_java.txt      # Java implementation
└── web_9.txt                                  # GitHub issue
```

## 📊 Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total files** | 45 |
| **Total size** | 6.9 MB |
| **PDF files** | 6 (548 KB) |
| **External links** | 38 (6.3 MB) |
| **Documentation** | 4 (12 KB) |
| **Unique PDF sources** | 3 |
| **Unique external sources** | 53 |
| **Success rate** | 77% |

## 🎯 Use Cases

### For LLM Training
- Augment datasets with formal verification context
- Train on consensus algorithms and distributed systems
- Learn from multiple specification formats (TLA+, Rust, Java)

### For Research
- Study formal verification patterns
- Compare algorithm implementations across languages
- Analyze consensus algorithm variations

### For Learning
- Understand TLA+ specification writing
- Follow along with tutorials and blog posts
- Reference algorithm implementations
- Study distributed systems theory

### For Development
- Reference correct implementations
- Understand specification patterns
- Learn from real-world examples
- Copy algorithm pseudocode

## 🔍 How to Search

### Find consensus-related content:
```bash
grep -r "consensus" . --include="*.txt" | head -20
```

### Find Paxos content:
```bash
grep -r "paxos" external_links/ --include="*.txt" -i
```

### Find distributed systems content:
```bash
grep -r "distributed\|replica" . --include="*.txt" -i
```

### See file sizes:
```bash
ls -lh external_links/web_*.txt | sort -k5 -h
```

## 📥 Integration Examples

### Python - Load all files:
```python
import os
content = {}
for file in os.listdir('scraped_pdfs'):
    if file.endswith('.txt'):
        with open(f'scraped_pdfs/{file}') as f:
            content[file] = f.read()
```

### Bash - Count words in all files:
```bash
wc -w *.txt external_links/*.txt | tail -1
```

### Bash - Extract links:
```bash
grep -h "^Source URL:" * external_links/* | sort | uniq
```

## ✅ What's Included

- ✓ 100% of available PDFs (3 unique, 6 files with duplicates)
- ✓ 76% of accessible external links (38 of 50)
- ✓ All documentation and verification reports
- ✓ Complete source URLs and metadata
- ✓ Cross-referenced inventory files

## ❌ What's Not Included (and Why)

- Paywalled content (ACM, IEEE, ResearchGate) - Requires institutional access
- YouTube videos - Cannot download video content
- Some Lamport pages - URLs changed or moved (404 errors)

## 🛠️ Tools & Scripts

Located in `/home/espencer2/Papers-dataset/`:

1. **scrape_pdfs.py** - Extracts PDFs from CSV comments
2. **verify_scraping.py** - Verifies and catalogs all links
3. **scrape_additional_links.py** - Downloads external references

## 📝 Files Generated

- **COMPLETE_DATASET_SUMMARY.md** - Main reference document
- **EXTERNAL_LINKS_REPORT.md** - Detailed link report
- **README.md** - Directory overview
- **_verification_report.txt** - All 53 links with URLs
- **_pdf_inventory.txt** - PDF-to-project mapping

---

**Status**: ✅ Complete and ready for use  
**Location**: `/home/espencer2/Papers-dataset/scraped_pdfs/`  
**Date**: February 4, 2026  
**Total Content**: 6.9 MB across 45 files
