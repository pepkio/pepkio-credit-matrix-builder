# Pepkio CRediT Matrix Builder

Standardized NISO Contributor Roles Taxonomy (CRediT) authorship statement generator and JATS XML metadata engine for academic papers.

# What It Does

The `pepkio-credit-matrix-builder` Python package creates, audits, and formats contributor role matrices for multi-author scientific manuscripts. It maps author contributions across all 14 official NISO CRediT roles, supports role degree assignments (Lead, Equal, Supporting), and exports publisher-compliant statements for PLOS, Elsevier, Frontiers, Markdown, and JATS XML 1.3.

# Features

- **14 NISO CRediT Roles**: Full support for all official ANSI/NISO Z39.104-2022 categories.
- **Granular Contribution Levels**: Assign *Lead*, *Equal*, or *Supporting* degrees per author-role pairing.
- **Multi-Publisher Formats**: Output ready-to-paste statements for PLOS, Elsevier, Frontiers, and clean Markdown.
- **JATS XML & CSV Export**: Export machine-readable XML `<contrib>` metadata and tabular CSV matrices.
- **Author Entity Parser**: Parse raw author text lists into structured author records with ORCIDs.
- **CLI & Python API**: Scriptable interface for automated manuscript workflows and publishing systems.

# Installation

```bash
pip install pepkio-credit-matrix-builder
```

Or using `uv`:

```bash
uv add pepkio-credit-matrix-builder
```

# Quick Example

```python
from pepkio_credit_matrix_builder import PepkioClient

with PepkioClient() as client:
    result = client.run({
        "action": "generate",
        "articleType": "empirical",
        "journalFormat": "plain",
        "authors": [
            {"id": "author-1", "name": "Dr. Elena Vasquez", "corresponding": True},
            {"id": "author-2", "name": "Alex Chen", "equalContribution": True}
        ],
        "assignments": {
            "author-1": {"conceptualization": {"assigned": True, "degree": "lead"}},
            "author-2": {"investigation": {"assigned": True, "degree": "lead"}}
        }
    })

    print("CRediT Statement:\n", result.result["statement"])
```

# Typical Use Cases

- **Journal Submissions**: Format compliant author contribution statements for PLOS ONE, Elsevier, Springer Nature, and Frontiers.
- **Authorship Audits**: Establish transparent role attribution among co-authors prior to manuscript submission.
- **JATS Metadata Generation**: Generate machine-readable XML `<role vocab="credit">` tags for publisher ingest.

# Scientific Background

The Contributor Roles Taxonomy (ANSI/NISO Z39.104-2022) replaces ambiguous author order with explicit attribution across 14 practical roles covering ideation, technical investigation, data analysis, and manuscript preparation.

# Web Application

For collaborative visual matrix editing and live previewing, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/credit-matrix-builder

# Documentation and Resources

- GitHub Repository: https://github.com/pepkio/pepkio-credit-matrix-builder
- Web Application: https://www.pepkio.com/tools/credit-matrix-builder
- PyPI Package: https://pypi.org/project/pepkio-credit-matrix-builder/

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

CRediT matrix, contributor roles taxonomy, author contribution statement, NISO Z39.104, authorship matrix, JATS XML contributor, PLOS author contribution, Elsevier CRediT, Frontiers author contribution, academic authorship, manuscript submission, scientific credit attribution, ORCID contributor, author contribution paragraph, co-author credit matrix, research contributor roles, academic publishing, equal contribution, open science transparency
