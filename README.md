# DocStructureX-Persona — Persona-Driven Document Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents

- [About](#about)  
- [Key Features](#key-features)  
- [How It Works](#how-it-works)  
- [Architecture](#architecture)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Docker Usage](#docker-usage)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  

---

## About

**DocStructureX-Persona** is a production-ready, fully offline, CPU-optimized tool developed for the Adobe India Hackathon 2025 Round 1B challenge — *Persona-Driven Document Intelligence*.

The system analyzes a collection of related PDFs and extracts the most relevant sections tailored to a user’s unique persona and their specific job-to-be-done. It builds on robust structural outline extraction from Round 1A, combining lightweight natural language processing with fast semantic ranking using TF-IDF vectorization.

Designed to work efficiently without any internet access, respecting stringent model size (≤1GB) and runtime (≤60 seconds) constraints, DocStructureX-Persona delivers insightful and personalized extracts for research, analysis, education, and more.

---

## Key Features

- **Persona-Aware Relevance:** Customizes content extraction and ranking based on a user’s role and task.
- **Multi-Document Support:** Processes 3–10 related PDFs as a knowledge collection.
- **Accurate Structure Extraction:** Leverages strong Round 1A document outline detection for precise section identification.
- **Lightweight Semantic Ranking:** Uses TF-IDF vectorization for fast and interpretable similarity scoring.
- **Granular Sub-Section Analysis:** Breaks down sections into paragraphs and ranks them for fine-grained insights.
- **Offline and CPU-Only:** Requires no internet connection or GPU hardware, fully compatible with AMD64 architecture.
- **Compliant Output:** Produces JSON in the exact format required for hackathon evaluation.
- **Modular and Extendable:** Clear code separation enables easy enhancement or integration with other pipelines.

---

## How It Works

1. **Outline Extraction:**  
   Uses the Round 1A extractor to identify titles and hierarchical headings (H1, H2, H3) across all PDFs.

2. **Text Extraction:**  
   Extracts text content for each identified section by parsing pages bounded by headings.

3. **Persona and Job Encoding:**  
   Combines the persona description and job-to-be-done into a semantic query for relevance comparison.

4. **Semantic Ranking:**  
   Employs TF-IDF vectorization and cosine similarity to score and rank document sections in terms of importance for the persona’s task.

5. **Subsection Refinement:**  
   Analyzes and ranks paragraphs inside top-ranked sections to highlight key insights.

6. **Structured Output:**  
   Generates a comprehensive JSON file detailing metadata, section rankings, and sub-section analysis suitable for downstream applications.

---

## Architecture

DocStructureX-Persona Architecture Flow
├── PDF Input Collection
├── Round 1A Extractor (Outline detection)
├── Section Text Extraction (via PyMuPDF)
├── Text Vectorization (TF-IDF)
├── Semantic Similarity Scoring
├── Section Ranking by Persona/Job Query
├── Paragraph-level Subsection Analysis
└── JSON Output Generation



- Built using pure Python with industry standard libraries.
- Modular components allow independent development, testing, and extensibility.
- Runtime and model size constraints rigorously enforced via timers and lightweight NLP.

---

## Installation

Clone the repository and set up your Python environment:

git clone https://github.com/godzaryan/DocStructureX-Persona.git
cd DocStructureX-Persona
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt



---

## Usage

1. **Prepare Input PDFs**

   Place your 3 to 10 relevant PDF files inside the `input/` folder.

2. **Run Extraction**

   Execute the main script with persona and job-to-be-done inputs:

python round1b_solution.py input "Senior Python Developer" "Tutorial on how Python 'Hello World' program is written" output/output.json



3. **Review Output**

The output JSON will be saved at the specified path (`output/output.json`) containing:

- Metadata (input docs, persona, job description, timestamp)
- Ranked document sections with page numbers and relevance scores
- Ranked sub-section textual insights for deeper context

---

## Docker Usage

Ensure Docker is installed and running on your system.

### Build the Docker Image
```
docker build --platform linux/amd64 -t docstructurex-persona:latest .
```


### Run the Container
```
docker run --rm -v %cd%\input:/app/input -v %cd%\output:/app/output --network none -e PERSONA="PhD Researcher in AI" -e JOB_TO_BE_DONE="Literature review on neural networks" docstructurex-persona:latest
```

for windows (cmd) :
```
docker run --rm -v %cd%\input:/app/input -v %cd%\output:/app/output --network none -e PERSONA="PhD Researcher in AI" -e JOB_TO_BE_DONE="Literature review on neural networks" docstructurex-persona:latest
```


---

## Project Structure

DocStructureX-Persona/
├── input/ # Put your PDF files here
├── output/ # Output JSON files will be written here
├── round1a_implementation.py
├── main.py
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
├── README.md
└── LICENSE



---

## Contributing

Contributions, suggestions, and improvements are welcome!  
Please fork the repo, create a feature branch, and submit a pull request.  
Ensure your changes adhere to offline execution and model size/runtime constraints.

---

## License

This project is licensed under the **MIT License**. See the LICENSE file for details.

---

## Acknowledgments

- **PyMuPDF** — fast, reliable PDF processing.  
- **scikit-learn** — robust TF-IDF vectorization and similarity tools.  
- Hackathon mentors and Adobe for guiding the challenge framework.  
- Open-source community for their invaluable tools and inspiration.

---

*Built by Akash Kumar (Aryan)*
