import sys
import os
import json
import datetime
import time
from pathlib import Path

import fitz
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from round1a_implementation import DocStructureXExtractor


class DocPersonaRanker:
    def __init__(self, persona, job, max_time=55):
        self.persona_job = f"{persona} {job}".strip()
        self.extractor = DocStructureXExtractor()
        self.max_time = max_time
        self.start = time.time()

    def process_collection(self, input_pdf_paths):
        all_sections = []
        for pdf_path in input_pdf_paths:
            outline = self.extractor.extract_outline(str(pdf_path))
            sections = self.extract_sections(str(pdf_path), outline)
            for sec in sections:
                sec['document'] = pdf_path.stem
            all_sections.extend(sections)
            if self.time_left() < 10:
                break

        if not all_sections:
            return [], []

        texts = [self.persona_job] + [sec['text'] for sec in all_sections]
        vectorizer = TfidfVectorizer(stop_words="english", max_features=12000)
        tfidf_matrix = vectorizer.fit_transform(texts)
        scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:]).flatten()

        ranked_sections = []
        for idx, sec in enumerate(all_sections):
            ranked_sections.append({
                "document": sec["document"],
                "page_number": sec["page_number"],
                "section_title": sec["section_title"],
                "importance_rank": -1,
                "relevance_score": float(scores[idx])
            })

        ranked_sections.sort(key=lambda s: -s["relevance_score"])
        for i, sec in enumerate(ranked_sections, start=1):
            sec["importance_rank"] = i

        top_sections = ranked_sections[:15]
        sub_section_results = []
        for sec in top_sections:
            paragraphs = self.extract_paragraphs(all_sections, sec)
            if not paragraphs:
                continue
            para_texts = [p["text"] for p in paragraphs]
            para_texts_with_query = [self.persona_job] + para_texts
            para_tfidf = vectorizer.fit_transform(para_texts_with_query)
            para_scores = cosine_similarity(para_tfidf[0], para_tfidf[1:]).flatten()
            scored_paragraphs = sorted(zip(paragraphs, para_scores), key=lambda x: -x[1])[:3]
            for rank_idx, (para, _) in enumerate(scored_paragraphs, start=1):
                sub_section_results.append({
                    "document": sec["document"],
                    "refined_text": para["text"],
                    "page_number": para["page_number"],
                    "parent_section": sec["section_title"],
                    "rank": rank_idx
                })
            if self.time_left() < 3:
                break

        return ranked_sections[:30], sub_section_results[:30]

    def extract_sections(self, pdf_path, outline):
        doc = fitz.open(pdf_path)
        sections = []
        outlines = outline.get("outline", [])
        outlines_sorted = sorted(outlines, key=lambda s: (s["page"], s["level"], s["text"]))
        for idx, heading in enumerate(outlines_sorted):
            start_page = heading["page"] - 1
            end_page = outlines_sorted[idx + 1]["page"] - 1 if idx + 1 < len(outlines_sorted) else len(doc)
            text = ""
            for pagenum in range(start_page, min(end_page, len(doc))):
                text += doc[pagenum].get_text()
                if len(text) > 5e5:
                    break
            sections.append({
                "section_title": heading["text"],
                "page_number": heading["page"],
                "text": text.strip()
            })
            if self.time_left() < 15:
                break
        doc.close()
        return sections

    def extract_paragraphs(self, all_sections, section):
        matches = [
            s for s in all_sections
            if s["document"] == section["document"] and s["section_title"] == section["section_title"]
        ]
        if not matches:
            return []
        text = matches[0]["text"]
        paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 40]
        return [{"text": p, "page_number": section["page_number"]} for p in paras][:10]

    def time_left(self):
        return self.max_time - (time.time() - self.start)

def main():
    if len(sys.argv) != 5:
        print(f"Usage: python {sys.argv[0]} <input_folder> <persona> <job_to_be_done> <output_file>")
        sys.exit(1)
    _, input_folder, persona, job_to_be_done, output_file = sys.argv
    pdf_dir = Path(input_folder)
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    ranker = DocPersonaRanker(persona, job_to_be_done)
    sections, sub_sections = ranker.process_collection(pdf_files)
    output = {
        "metadata": {
            "input_documents": [file.name for file in pdf_files],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": timestamp
        },
        "extracted_sections": sections,
        "sub_section_analysis": sub_sections
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
