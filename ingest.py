import html
import random
import re
from pathlib import Path


def clean_text(text: str) -> str:
    """Normalize common artifacts from manually copied RMP text."""
    # Decode HTML entities (&amp; &nbsp; &#39; etc.)
    text = html.unescape(text)
    # Normalize curly/smart quotes to straight quotes
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    # Normalize em-dash and en-dash to hyphens
    text = text.replace("—", "--").replace("–", "-")
    # Collapse runs of blank lines to a single newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_and_chunk_documents(docs_dir: str = "documents") -> list[dict]:
    """Load all .txt files from docs_dir, split on ---, return chunks with source metadata.

    Each review chunk is prefixed with its professor name and course so that
    every chunk is independently searchable by name or subject.
    """
    chunks = []
    docs_path = Path(docs_dir)

    for txt_file in sorted(docs_path.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8")
        raw_chunks = content.split("---")

        professor = ""
        current_course = ""

        for raw in raw_chunks:
            text = clean_text(raw)
            if not text:
                continue

            # Update professor name if this chunk contains one
            prof_match = re.search(r"^Professor:\s*(.+)", text, re.MULTILINE)
            if prof_match:
                professor = prof_match.group(1).strip()

            # Update current course whenever a new Course: line appears
            course_match = re.search(r"^Course:\s*(.+)", text, re.MULTILINE)
            if course_match:
                current_course = course_match.group(1).strip()

            # Strip header lines (Professor/Course/Rating) to isolate the review text
            review = re.sub(r"^(Professor|Course|Rating):.*\n?", "", text, flags=re.MULTILINE).strip()
            if not review:
                continue

            # Prepend professor + course context to every review chunk
            header = f"Professor: {professor} | Course: {current_course}"
            chunks.append({"text": f"{header}\n{review}", "source": txt_file.name})

    return chunks


if __name__ == "__main__":
    # Print one raw document so we can verify cleaning worked
    docs_path = Path("documents")
    sample_file = next(docs_path.glob("*.txt"))
    print(f"=== Raw document: {sample_file.name} ===")
    print(sample_file.read_text(encoding="utf-8")[:500])
    print("\n=== After cleaning ===")
    print(clean_text(sample_file.read_text(encoding="utf-8"))[:500])
    print()

    chunks = load_and_chunk_documents()

    print(f"Total chunks loaded: {len(chunks)}\n")

    sample = random.sample(chunks, min(5, len(chunks)))
    for i, chunk in enumerate(sample, 1):
        print(f"--- Sample {i} ---")
        print(f"Source: {chunk['source']}")
        print(f"Text:   {chunk['text'][:300]}")
        print()
