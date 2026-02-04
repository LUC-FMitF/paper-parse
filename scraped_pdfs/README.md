# Scraped PDFs Directory

This directory contains PDFs extracted from external links in the Comment Ratios Dataset, converted to text format.

## Directory Contents

### PDF Text Files (6 files)
All academic papers and specifications referenced in the TLA+ dataset comments:

1. **Chameneos_Chameneos_RC474.txt** (43 KB)
   - Paper: "Chameneos, a Concurrency Game for Java, Ada and Others"
   - Authors: Claude Kaiser, Jean-François Pradat-Peyre
   - Source: https://cedric.cnam.fr/fichiers/RC474.pdf

2. **diskpaxos_DiskSynod_disk-paxos.txt** (108 KB)
   - Paper: "Disk Paxos" by Leslie Lamport
   - Source: https://lamport.azurewebsites.net/pubs/disk-paxos.pdf
   - Referenced by: DiskSynod model

3. **diskpaxos_HDiskSynod_disk-paxos.txt** (108 KB)
   - Same paper as above
   - Referenced by: HDiskSynod model

4. **diskpaxos_Synod_disk-paxos.txt** (108 KB)
   - Same paper as above
   - Referenced by: Synod model

5. **raft_raft_raft.txt** (83 KB)
   - Paper: "In Search of an Understandable Consensus Algorithm"
   - The Raft consensus algorithm specification
   - Source: https://raft.github.io/raft.pdf
   - Referenced by: raft model

6. **raft_raft_clean_raft.txt** (83 KB)
   - Same paper as above
   - Referenced by: raft_clean model

### Inventory Files (2 files)

7. **_pdf_inventory.txt** (1.6 KB)
   - Complete list of all PDF links found in the dataset
   - Maps each PDF to its project and model

8. **_verification_report.txt** (3.2 KB)
   - Complete list of all 53 unique external links found in dataset
   - Includes both PDF and non-PDF links (GitHub, ACM, IEEE, etc.)

## Statistics

- **Total files**: 8
- **Total size**: 548 KB
- **PDF text files**: 6
- **Unique PDF sources**: 3
- **Inventory files**: 2

## Data Format

Each PDF text file contains:
```
Source URL: <original PDF URL>
Project: <project name>
Model: <model name>
================================================================================

<extracted text content>
```

## Usage

These files can be used for:
- Understanding the theoretical background of TLA+ specifications
- Providing context for formal verification models
- Training data augmentation for FormaLLM
- Reference documentation for TLA+ learners

## Source

All PDFs were automatically extracted from the "Comment Ratios Dataset" CSV file located at:
`/home/espencer2/Papers-dataset/Comment Ratios Dataset(Comments Ratio).csv`

## Tools

Generated using:
- `scrape_pdfs.py` - Main scraping and conversion script
- `verify_scraping.py` - Verification and reporting script

Libraries used:
- pdfplumber (v0.11.9) - Primary PDF text extraction
- PyPDF2 (v3.0.1) - Fallback PDF text extraction
- requests (v2.32.5) - PDF download

## Last Updated

February 4, 2026
