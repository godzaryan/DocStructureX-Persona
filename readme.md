# DocStructureX — Intelligent PDF Outline Extractor & Persona-Driven Document Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents

- [About](#about)  
- [Features](#features)  
- [How It Works](#how-it-works)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Docker Usage](#docker-usage)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  

---

## About

DocStructureX is an advanced PDF processing suite designed for the Adobe India Hackathon 2025 Rounds 1A and 1B.

- **Round 1A:** Precise, fast extraction of hierarchical PDF outlines (title and headings H1, H2, H3).  
- **Round 1B:** Persona-driven intelligent document analysis over multiple PDFs delivering ranked relevant sections per user role and task.

This solution is optimized for CPU execution, is fully offline, respects all hackathon size and runtime constraints, and outputs well-structured JSON compliant with challenge requirements.

---

## Features

- Multi-layer outline extraction: native TOC, font-weight heuristics, regex fallbacks.  
- Fast, modular, and runtime-bound processing for PDFs up to 50 pages in Round 1A.  
- Semantic ranking of sections by persona and job-to-be-done using TF-IDF and cosine similarity.  
- Subsection-level textual analysis and ranking for fine granularity.  
- Fully containerized with a minimal Docker image supporting AMD64 CPU-only runs.  
- No internet dependency at build or run time.  

---

## How It Works

### Round 1A

1. Attempt Table of Contents extraction for speed and accuracy.  
2. If TOC missing, apply heuristic font size and style rules to text blocks.  
3. Fall back to regex-based parsing if needed.  
4. Generate JSON with document title and hierarchical outline with page numbers.

### Round 1B

1. Extract outlines from multiple PDFs using Round 1A extractor.  
2. Extract section texts by parsing pages between headings.  
3. Embed persona and job descriptions with TF-IDF vectorizer.  
4. Rank document sections by semantic similarity to persona+job query.  
5. Extract and rank key paragraphs within top relevant sections.  
6. Output JSON with metadata, ranked sections, and sub-section insights.

---

## Installation

### Requirements

- Python 3.10+  
- Docker (optional for containerized execution)

### Setup

git clone https://github.com/yourusername/DocStructureX.git
cd DocStructureX
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt

text

---

## Usage

### Prepare Input Files

Place your PDF files in the `input/` directory.

### Run Locally

python round1b_solution.py input "Your Persona Description" "Your Job to be Done" output/output.json

text

### Output

Processed JSON files will be saved as specified (default in `output/`).

---

## Docker Usage

### Build Image

docker build --platform linux/amd64 -t docstructurex:latest .

text

### Run Container

docker run --rm
-v $(pwd)/input:/app/input
-v $(pwd)/output:/app/output
--network none
-e PERSONA="PhD Researcher in AI"
-e JOB_TO_BE_DONE="Literature review on neural networks"
docstructurex:latest

text

---

## Project Structure

DocStructureX/
├── input/ # Place input PDFs here
├── output/ # JSON outputs saved here
├── round1a_implementation.py
├── round1b_solution.py
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
├── README.md
├── .gitignore
└── LICENSE

text

---

## Contributing

Contributions are welcome via Pull Requests. Please ensure:

- Compliance with hackathon rules.  
- Code readability and modular design.  
- Incremental testing and documentation.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

*Built by Akash Kumar (Aryan)*