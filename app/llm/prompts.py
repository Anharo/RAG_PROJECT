def build_prompt(query, context_chunks):
    context = "\n\n".join(context_chunks)

    return f"""
You are a helpful assistant.

Based on the context, describe the answer clearly and concisely.
If the question is about a person, describe who they are based on available context.

Do NOT make up facts.

Context:
{context}

Question:
{query}

Answer:
"""