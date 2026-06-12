source# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
<p align ="left">
The domain of this project are the student reviews of Hunter College Computer Science professors. This is useful because official course catalogs and professor pages only list descriptions and office hours, not teaching style, the difficulty of the exams, the workload, or how responsive a professor is. Students typically have to search through multiple Rate My Professor pages individually to compare professors for the same course. This system brings all that information together in one place, making it easier for Hunter CS students to make informed decisions when registering for their upcoming courses.
</p>
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source |      Type     | URL or location |
|---|--------|  -------------|-----------------|
| 1 | RMP    |Mneimneh Rating|https://www.ratemyprofessors.com/professor/926045|
| 2 | RMP    |Lynch Rating   |https://www.ratemyprofessors.com/professor/2505090|
| 3 | RMP    |Dietrich Rating|https://www.ratemyprofessors.com/professor/2674099|
| 4 | RMP    |Eric Rating    |https://www.ratemyprofessors.com/professor/257192|
| 5 | RMP    |Maryash Rating |https://www.ratemyprofessors.com/professor/1137095|
| 6 | RMP    |Oyewole Rating |https://www.ratemyprofessors.com/professor/2558461|
| 7 | RMP    |Shankar Rating |https://www.ratemyprofessors.com/professor/257190|
| 8 | RMP    |Shostak Rating |https://www.ratemyprofessors.com/professor/1823870|
| 9 | RMP    |Stamos Rating  |https://www.ratemyprofessors.com/professor/64427|
| 10| RMP    |Tojeira Rating |https://www.ratemyprofessors.com/professor/1660967|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
One review per chunk that splits on the --- separator. Reviews range from 50-300 characters each
**Overlap:**
There is no overlap, every review is a complete, independent opinion. There is no meaninful content that spans two reviews. 
**Why these choices fit your documents:**
These choices fit my documents because each document is a collection of reviews from the RMP website that are separated by dashes. It would be natural to analyzse by each of those chunks.
**Final chunk count:**
Ultimately had 85 chunks in total accross the 10 .txt files
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
The model that was used was the "all-MiniLM-L6-v2" via sentence transformers. This model was chosen because it runs fully locally with no API key or rate limits which was great for this small project with just 85 chunks.
**Production tradeoff reflection:**
All-MiniLM-L6-v2 is good for local free use but its a small model trained on general text, not specifically on student slang or academic language, so it may be hard for the LLM to understand some of the "non-formal" reviews.
OpenAI's text-embedding-3-large would give better accuracy but costs money per API call.
Lastly, MiniLM is English only, this attribute may negatively impact results if reviews are written in other languages. 
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt given to llama-3.3-70b-versatile reads:"Answer the question by analyzing and synthesizing ONLY the information provided in the context below. You may draw conclusions and make comparisons based on what the reviews say. If the context does not contain enough information to answer the question, respond with: 'I don't have enough information in my documents to answer that.' Do not use any knowledge from your training data. Every claim in your answer must be traceable to the provided context."
**How source attribution is surfaced in the response:**
Source attribution is handled programmatically in query.py — the unique source filenames are collected from the retrieved chunks before the LLM is called, and returned alongside the answer. This means attribution is guaranteed regardless of what the model says. The Gradio UI displays them in a separate "Retrieved from" output box.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I gave it dihh
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
