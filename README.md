# Pepkio CRediT Matrix Builder

Generate standardized NISO Contributor Roles Taxonomy (CRediT) authorship statements, contribution audit matrices, and JATS XML metadata for scientific manuscripts in Python and via web interface.

# Overview

Modern biomedical and scientific research relies on large, multidisciplinary collaborative teams comprising molecular biologists, computational bioinformaticians, clinicians, laboratory technicians, and principal investigators. Traditional linear author lists and arbitrary asterisk footnotes fail to convey specific individual contributions, often leading to authorship disputes, lack of credit transparency, and administrative delays during journal submission.

To establish standardized attribution, the National Information Standards Organization (NISO) formalized the **Contributor Roles Taxonomy (CRediT)** (ANSI/NISO Z39.104-2022), which specifies 14 distinct contributor roles spanning research ideation, data collection, software engineering, and manuscript writing. Leading publishers—including PLOS, Elsevier, Springer Nature, Wiley, and Frontiers—increasingly mandate formal CRediT statements and structured JATS XML metadata.

The **Pepkio CRediT Matrix Builder** provides an interactive matrix management system and programmatic Python toolkit for assigning, auditing, and formatting contributor roles. It supports role attribution across 14 CRediT categories, allows optional degree specification (Lead, Equal, Supporting), validates required roles for empirical vs. review articles, and formats ready-to-submit text across major publisher styles (PLOS, Elsevier, Frontiers, Markdown, and JATS XML).

The interactive web tool is available at the [Pepkio CRediT Matrix Builder](https://www.pepkio.com/tools/credit-matrix-builder) web application for collaborative real-time matrix editing. A modular Python package and CLI are maintained in this repository for automated submission systems and editorial workflows.

Common search terms and alternative names for this tool include credit matrix builder, contributor roles taxonomy generator, CRediT author statement generator, NISO Z39.104 tool, authorship contribution matrix, JATS XML contributor metadata generator, PLOS author contribution statement, Elsevier CRediT statement, and academic author role allocator.

# Features

- **Standard 14 NISO CRediT Roles**: Full support for all official taxonomy categories:
  1. *Conceptualization*
  2. *Data curation*
  3. *Formal analysis*
  4. *Funding acquisition*
  5. *Investigation*
  6. *Methodology*
  7. *Project administration*
  8. *Resources*
  9. *Software*
  10. *Supervision*
  11. *Validation*
  12. *Visualization*
  13. *Writing – original draft*
  14. *Writing – review & editing*
- **Granular Contribution Degrees**: Optionally assign *Lead*, *Equal*, or *Supporting* levels to individual author-role pairings for nuanced credit allocation.
- **Multi-Publisher Formatting Engine**:
  - *PLOS Format*: Grouped by role with author initials (e.g., `Conceptualization: E.V., A.C. Methodology: E.V.`).
  - *Elsevier Format*: Author-by-author role enumeration.
  - *Frontiers Format*: Structured narrative contribution paragraphs.
  - *Markdown & Plain Text*: Clean, publication-ready paragraphs for submission portals.
  - *JATS XML (v1.2 / v1.3)*: Machine-readable `<contrib>` XML tags with embedded `<role vocab="credit">` elements for automated publisher ingest.
- **Author Metadata Management**: Track author affiliations, ORCID IDs (e.g., `0000-0002-1825-0097`), corresponding author status, and joint first-author equal contribution designations.
- **Matrix Import & Export**: Export matrices as structured CSV files or JATS XML, and import existing author contribution files directly.
- **Automated Text Parser**: Parse unstructured author lists directly from manuscript title pages into organized author entities.
- **CLI & Python API**: Full programmatic control for laboratory information management systems (LIMS) and automated paper compilation pipelines.

# Common Use Cases

- **Journal Submission Preparation**: Generate compliant author contribution statements formatted specifically for PLOS ONE, Cell Press, Nature Communications, or Frontiers journals.
- **Research Team Authorship Auditing**: Establish transparent contributor role agreements among co-authors prior to manuscript drafting to prevent authorship conflicts.
- **Grant & Institutional Reporting**: Document and export team member contributions for progress reports, NIH biosketches, and tenure dossiers.
- **Publisher & Editorial Ingest**: Convert manuscript author lists into validated JATS XML `<contrib-group>` blocks for automated publication processing.
- **Review Article Authorship Planning**: Filter relevant roles specifically for review articles and meta-analyses.

# Why This Tool Exists

Manually drafting CRediT paragraphs in word processors is tedious, error-prone, and frequently produces mismatched author initials, inconsistent role names, or non-standard punctuation that fails publisher submission checks.

Furthermore, converting contribution matrices into machine-readable XML (such as JATS format required by modern preprint servers and archiving repositories like PubMed Central) typically requires complex manual XML tagging.

The **Pepkio CRediT Matrix Builder** eliminates manual drafting errors by providing a visual, structured matrix that automatically synchronizes with compliant output formatters. Teams can construct matrices interactively online via the [credit matrix web builder](https://www.pepkio.com/tools/credit-matrix-builder) or script matrix generation through the Python package.

# Installation

Install the Python client package from PyPI using `pip`:

```bash
pip install pepkio-credit-matrix-builder
```

Or using `uv`:

```bash
uv add pepkio-credit-matrix-builder
```

Package details are indexed on [PyPI](https://pypi.org/project/pepkio-credit-matrix-builder/).

# Quick Start

### Python API Usage

Set your API key as an environment variable:

```bash
export PEPKIO_API_KEY="your_pepkio_api_key"
```

Generate author contribution statements and XML metadata in Python:

```python
from pepkio_credit_matrix_builder import PepkioClient

with PepkioClient() as client:
    # 1. Generate a standardized PLOS/Plain CRediT statement
    result = client.run({
        "action": "generate",
        "articleType": "empirical",
        "journalFormat": "plain",
        "authors": [
            {
                "id": "author-1",
                "name": "Dr. Elena Vasquez",
                "orcid": "0000-0002-1825-0097",
                "corresponding": True
            },
            {
                "id": "author-2",
                "name": "Alex Chen",
                "equalContribution": True
            }
        ],
        "assignments": {
            "author-1": {
                "conceptualization": {"assigned": True, "degree": "lead"},
                "writing-original-draft": {"assigned": True, "degree": "lead"}
            },
            "author-2": {
                "investigation": {"assigned": True, "degree": "lead"},
                "validation": {"assigned": True, "degree": "equal"}
            }
        }
    })

    print("Author Contribution Statement:\n")
    print(result.result["statement"])

    # 2. Export matrix to JATS XML
    jats_export = client.run({
        "action": "export",
        "format": "jats",
        "authors": [{"id": "author-1", "name": "Dr. Elena Vasquez", "orcid": "0000-0002-1825-0097"}],
        "assignments": {"author-1": {"conceptualization": {"assigned": True}}}
    })
    print("\nJATS XML Output:\n", jats_export.result["content"])
```

### Command Line Interface (CLI)

The package provides a command-line interface executable `pepkio-credit-matrix-builder`:

```bash
# View tool manifest and actions
pepkio-credit-matrix-builder manifest

# Run the built-in empirical generation example
pepkio-credit-matrix-builder run --example generate_example

# Export CSV matrix from command line
pepkio-credit-matrix-builder run --example export_csv
```

# Example Output

Representative formatted plain text statement:

```text
Conceptualization: Dr. Elena Vasquez (Lead). Investigation: Alex Chen (Lead). Validation: Alex Chen (Equal). Writing - original draft: Dr. Elena Vasquez (Lead).
```

Representative JATS XML export snippet:

```xml
<contrib contrib-type="author" corresp="yes">
  <name>
    <surname>Vasquez</surname>
    <given-names>Elena</given-names>
    <prefix>Dr.</prefix>
  </name>
  <contrib-id contrib-id-type="orcid">https://orcid.org/0000-0002-1825-0097</contrib-id>
  <role vocab="credit" vocab-identifier="https://credit.niso.org/" vocab-term="Conceptualization" degree="lead">Conceptualization</role>
  <role vocab="credit" vocab-identifier="https://credit.niso.org/" vocab-term="Writing – original draft" degree="lead">Writing – original draft</role>
</contrib>
```

# Scientific Background

### The NISO CRediT Standard (ANSI/NISO Z39.104-2022)

The Contributor Roles Taxonomy was developed by the Wellcome Trust and Digital Science to resolve the ambiguities of academic authorship. Rather than reducing researcher input to an ordered list of names, CRediT assigns credit across 14 defined operational roles:

- **Ideation & Management**: Conceptualization, Funding acquisition, Project administration, Supervision.
- **Experimental & Technical**: Investigation, Methodology, Resources, Software, Validation.
- **Analytical & Communication**: Data curation, Formal analysis, Visualization, Writing – original draft, Writing – review & editing.

### Degree Allocation

In high-collaboration studies, multiple authors frequently share a single role. The NISO standard allows attributing a **degree** of contribution (*Lead*, *Equal*, or *Supporting*), enabling granular recognition of junior researchers and co-investigators.

# Frequently Asked Questions

### What is the difference between PLOS and Elsevier CRediT formats?
PLOS format groups contributions by role followed by author names/initials (e.g., `Conceptualization: A.B., C.D. Investigation: A.B.`). Elsevier format presents authors individually followed by their roles (e.g., `A.B.: Conceptualization, Investigation. C.D.: Conceptualization.`).

### Is CRediT required for all journals?
An increasing number of publishers (including PLOS, Elsevier, Springer Nature, Cell Press, Frontiers, and eLife) require or strongly recommend formal CRediT statements during manuscript submission.

### What is JATS XML?
Journal Article Tag Suite (JATS) is an XML standard used by academic publishers, PubMed Central (PMC), and preprint repositories to archive and index scientific literature. CRediT roles are tagged using `<role vocab="credit">`.

### Can multiple authors share the same role?
Yes. Multiple authors can be assigned to the same role, and you can specify whether their contributions were *Equal*, *Lead*, or *Supporting*.

### How does the author parser work?
The author text parser accepts comma- or newline-separated author names, detects titles (Dr., Prof.), extracts initials, and formats clean author entities for the matrix.

### Are ORCID identifiers supported?
Yes. You can attach 16-digit ORCID identifiers (e.g., `0000-0002-1825-0097`) to authors, which are automatically embedded in exported JATS XML tags.

### Can I save and share matrix state?
Yes. The web version encodes the entire matrix state into URL hash parameters for bookmarking and cross-team sharing.

# Web Application

For collaborative visual matrix editing and live statement previewing, visit the hosted web application:

Web Application:
https://www.pepkio.com/tools/credit-matrix-builder

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

# Related Resources

- GitHub Repository: https://github.com/pepkio/pepkio-credit-matrix-builder
- PyPI Package: https://pypi.org/project/pepkio-credit-matrix-builder/
- Web Application: https://www.pepkio.com/tools/credit-matrix-builder

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Citation

If you use the Pepkio CRediT Matrix Builder in academic publications, please cite:

```bibtex
@software{pepkio_credit_matrix_builder,
  author = {{Pepkio Open Science}},
  title = {Pepkio CRediT Matrix Builder: Standardized NISO Contributor Roles Taxonomy Statement and JATS XML Generator},
  url = {https://www.pepkio.com/tools/credit-matrix-builder},
  year = {2026}
}
```

# License

Distributed under the MIT License. See `LICENSE` for details.

# Keywords

credit matrix builder, contributor roles taxonomy, CRediT author statement generator, NISO Z39.104, authorship matrix, JATS XML contributor metadata, PLOS author contribution, Elsevier CRediT statement, Frontiers author contributions, academic authorship allocator, manuscript submission preparation, scientific credit attribution, ORCID contributor tagging, author contributions paragraph, co-author credit matrix, research contributor roles, academic publishing tools, journal submission checklist, equal contribution authorship, peer review authorship audit, biomedical authorship management, open science transparency, research credit transparency, PubMed Central JATS XML, author contribution statement creator, lab productivity tools, bioinformatic paper submission, science writing tools, contributor taxonomy generator
