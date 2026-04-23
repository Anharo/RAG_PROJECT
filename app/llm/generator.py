import requests
from app.core.config import OPENROUTER_API_KEY
from app.llm.prompts import build_prompt


def generate_answer(query, chunks):
    # ✅ Handle empty retrieval
    if not chunks:
        return "I couldn't find relevant information in the document."

    # ✅ Extract text from chunk dicts
    context_chunks = [c["text"] for c in chunks]

    prompt = build_prompt(query, context_chunks)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()

        # ✅ Safe extraction
        return data.get("choices", [{}])[0].get("message", {}).get(
            "content",
            "Error generating response."
        )

    except Exception as e:
        return f"LLM Error: {str(e)}"