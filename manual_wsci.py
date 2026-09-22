from pathlib import Path
from ollama import chat


question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

selected_files = [
    "knowledge/password_changes.txt",
    "knowledge/service_status.txt",
    "knowledge/wifi_setup.txt"
]


context = ""

## Read selected files into context
for file_path in selected_files:
    with open(file_path, "r") as f:
        context += f.read()
        context += "\n\n"

## Call Qwen with the question and the selected context
response = chat(
    model="qwen2.5:latest",
    messages=[
        {"role": "system", "content": "You are a university IT support assistant. Answer the student's question based on the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
)

print(
    "Context characters:",
    len(context)
)
print(response.message.content)
