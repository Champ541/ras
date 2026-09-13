# RAS AI 🤖

A RAG-based AI assistant for the **IEEE Robotics & Automation Society (IEEE-RAS) Student Chapter, VIT Chennai**, built using publicly available information.

## What it does

1. Stores curated public IEEE RAS / VIT Chennai information in `data/knowledge_base.json`.
2. Converts the documents into TF-IDF vectors.
3. Retrieves the most relevant documents for a user question.
4. Uses Google Gemini to synthesize a grounded answer when `GEMINI_API_KEY` is configured.
5. Shows retrieved sources for traceability.
6. Falls back to an extractive response if no Gemini key is available.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

For Gemini-powered answers, set `GEMINI_API_KEY` in your environment.

## Deploy on Streamlit Community Cloud

1. Connect this GitHub repository to Streamlit Community Cloud.
2. Select `app.py` as the main file.
3. In the app's Secrets settings, add:

```toml
GEMINI_API_KEY = "YOUR_KEY"
```

4. Deploy.

## RAG architecture

```text
Public IEEE RAS/VIT sources
          ↓
 Curated knowledge base
          ↓
       TF-IDF
          ↓
   Top-k retrieval
          ↓
  Retrieved evidence
          ↓
      Gemini 2.5 Flash
          ↓
 Grounded answer + sources
```

## Design choice

The LLM is not allowed to answer from unrestricted general knowledge. Retrieval happens first, and the generation prompt restricts the answer to the retrieved evidence.

## Sources

- VIT Chennai IEEE Chapters: https://chennai.vit.ac.in/campus/chapters/ieeechapters/
- VIT Chennai Campus Clubs/Chapters: https://chennai.vit.ac.in/campus-category/clubs/
- VIT Chennai IEEE RAS Chapter Activities PDF: https://chennai.vit.ac.in/wp-content/uploads/2021/08/IEEE-RAS-VITCC-ATTACHMENT-CHAPTER-INITIATIVE-GRANT.pdf
- VIT Chennai SENSE Newsletter: https://chennai.vit.ac.in/SENSE/SENSE-Newsletter_2021%20%281%29.pdf
- VIT Chennai IEEE RAS Complete Report: https://chennai.vit.ac.in/wp-content/uploads/2021/08/IEEE_RAS_Complete_Report-2020-21.pdf
- HackVerse: Into the Web: https://hackverse-into-the-web.devfolio.co/
- GLYTCH: https://glytch.devfolio.co/overview

## Example questions

- What is IEEE RAS at VIT Chennai?
- What is the mission of IEEE RAS?
- What did the sensors and mechanical overview talk cover?
- Tell me about the ML and Data Science using Python webinar.
- What is HackVerse: Into the Web?
- What is GLYTCH?
