## This file is a bad way of managing context.

from pathlib import Path
from ollama import chat


question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""


context = ""

for file in Path("knowledge").glob("*.txt"):
    context += file.read_text()
    context += "\n\n"

## Call Qwen with student's question and the context from the knowledge base
response = chat(
    model="qwen2.5:latest",
    messages=[
        {"role": "system", "content": "You are a university IT support assistant. Answer the student's question based on the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
)


## Print the total length of the context
print(
    "Context characters:",
    len(context)
)

## Print the response from Qwen
print(response.message.content)
