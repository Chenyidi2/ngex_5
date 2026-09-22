from pathlib import Path
from ollama import chat
import json


question = """
I changed my university password this morning.
Now my Windows laptop won't connect to campus Wi-Fi,
but my phone still works.
"""

## WRITE ##
service_status = {
    "wifi": "operational"
}

state = {
    "problem": question,
    "wifi_status": "operational",
    "wifi_check": True
}

with open("state.json", "w") as file:
    json.dump(
        state,
        file,
        indent=2
    )

with open("state.json", "r") as file:
    state = json.load(file)

print(state)


## SELECT ##
## Select relevant files based on keywords in the question
def select_context(question):
    q = question.lower()
    selected = []

    if "printer" in q or "print" in q:
        selected.append("knowledge/printing.txt")

    if "vpn" in q:
        selected.append("knowledge/vpn.txt")

    if "password" in q or "credential" in q:
        selected.append("knowledge/password_changes.txt")

    if "email" in q:
        selected.append("knowledge/email_setup.txt")

    if "wifi" in q or "network" in q or "connect" in q:
        selected.append("knowledge/service_status.txt")
        selected.append("knowledge/wifi_setup.txt")

    if "projector" in q or "display" in q:
        selected.append("knowledge/classroom_projectors.txt")

    return selected


selected_files = select_context(question)

## Read selected files into context
context = ""

for file_path in selected_files:
    with open(file_path, "r") as f:
        context += f.read()
        context += "\n\n"


## COMPRESS ##
def compress_context(context, question):
    response = chat(
        model="qwen2.5:latest",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Extract only the information from the context that is relevant to answering the user's question. Be concise and remove unnecessary details."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\n\nExtract only the relevant information:"}
        ]
    )
    return response.message.content


compressed_context = compress_context(context, question)

## Print compressed context length
print("Compressed context length:", len(compressed_context))

## Call Qwen with compressed context and structured output requirement
response = chat(
    model="qwen2.5:latest",
    messages=[
        {"role": "system", "content": "You are a university IT support assistant. Answer the question based on the given context. Provide your answer in a structured format."},
        {"role": "user", "content": f"Context:\n{compressed_context}\n\nQuestion: {question}\n\nPlease provide a structured answer with: 1) Diagnosis 2) Likely cause 3) Recommended steps to fix"}
    ]
)

print(response.message.content)

## WRITE the output to state.json
state["diagnosis"] = response.message.content
state["relevant_files"] = selected_files
state["compressed_context"] = compressed_context

with open("state.json", "w") as file:
    json.dump(state, file, indent=2)

## Use state.json as part of context for future calls
with open("state.json", "r") as file:
    state = json.load(file)

## Only use relevant parts from state, not the entire artifact
relevant_state = {
    "wifi_status": state.get("wifi_status"),
    "diagnosis": state.get("diagnosis")
}

print("\nState artifact:", json.dumps(relevant_state, indent=2))

## ISOLATE ##
diagnostic_context = {
    "problem": question,
    "device": "windows laptop",
    "wifi_status": "operational"
}

report_context = {
    "total_wifi_cases": 37,
    "resolved_cases": 29,
    "unresolved_cases": 8
}

print("\nDiagnostic context:", diagnostic_context)
print("Report context:", report_context)


