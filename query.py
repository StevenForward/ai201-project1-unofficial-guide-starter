import os

from dotenv import load_dotenv
from groq import Groq

from embed import get_collection, retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a helpful assistant for Hunter College CS students looking for professor reviews.

Answer the question by analyzing and synthesizing ONLY the information provided in the context below.
You may draw conclusions and make comparisons based on what the reviews say.
If the context does not contain enough information to answer the question, respond with:
"I don't have enough information in my documents to answer that."

Do not use any knowledge from your training data. Every claim in your answer must be traceable to the provided context."""


def ask(query: str) -> dict:
    """Retrieve relevant chunks and return a grounded answer with sources."""
    collection = get_collection()
    results = retrieve(query, collection)

    context = "\n\n".join(
        f"[{i}] {chunk['text']}" for i, chunk in enumerate(results, 1)
    )

    # Sources are collected programmatically — not left to the LLM
    sources = list(dict.fromkeys(chunk["source"] for chunk in results))

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
        ],
        temperature=0.3,
    )

    return {"answer": response.choices[0].message.content, "sources": sources}


if __name__ == "__main__":
    test_queries = [
        "Which CS professor is the best for discrete math?",
        "Who is better for Computer Architecture 2, Shankar or Shostak?",
        "What is the best pizza place near Hunter College?",  # out of scope
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Q: {query}")
        print("="*60)
        result = ask(query)
        print(f"A: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
