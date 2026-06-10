import gradio as gr

from query import ask


def handle_query(question: str):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s.replace('.txt', '')}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide — Hunter CS Professors") as demo:
    gr.Markdown("# The Unofficial Guide\nAsk anything about Hunter College CS professors based on real student reviews.")

    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. Which professor is best for discrete math?",
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()
