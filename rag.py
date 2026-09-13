import json
import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RASRetriever:
    def __init__(self, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.docs = data["documents"]
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.matrix = self.vectorizer.fit_transform([d["text"] for d in self.docs])

    def retrieve(self, query, k=5):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).ravel()
        order = scores.argsort()[::-1][:k]
        return [
            {**self.docs[i], "score": float(scores[i])}
            for i in order
            if scores[i] > 0
        ]


def generate_answer(question, docs):
    if not docs:
        return "I couldn't find relevant information in my IEEE RAS VIT Chennai knowledge base. Try asking about the chapter, robotics, automation, events, or workshops."

    context = "\n\n".join(
        f"SOURCE: {d['title']}\nURL: {d['url']}\nCONTENT: {d['text']}"
        for d in docs
    )

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""You are RAS AI, an information assistant for the IEEE Robotics & Automation Society Student Chapter at VIT Chennai.

Answer the user's question using ONLY the retrieved public sources below.
- Do not invent names, dates, statistics, events, or claims.
- If the sources do not contain enough information, say so clearly.
- Keep the answer concise but useful.
- Mention relevant event names and dates when the evidence provides them.

USER QUESTION:
{question}

RETRIEVED SOURCES:
{context}
"""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception:
            pass

    best = docs[0]
    return (
        f"Based on the retrieved IEEE RAS VIT Chennai information, the closest match is **{best['title']}**.\n\n"
        f"{best['text']}\n\n"
        f"*The response is generated from the local retrieval knowledge base. Add `GEMINI_API_KEY` for conversational synthesis.*"
    )
