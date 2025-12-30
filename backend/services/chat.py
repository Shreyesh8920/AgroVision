import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError("OPENROUTER_API_KEY not found in .env")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

PRIMARY_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
FALLBACK_MODEL = "mistralai/mistral-7b-instruct:free"

MAX_CONTEXT_MESSAGES = 6  

# OPENROUTER CALL

def call_openrouter(model, messages):
    if not model.endswith(":free"):
        raise RuntimeError("Blocked non-free model")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 300,
        "provider": {
            "max_price": {
                "prompt": 0,
                "completion": 0
            },
            "allow_fallbacks": False
        }
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "Referer": "http://localhost",
        "X-Title": "Agri Chatbot"
    }
    try:
        r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=20
        )

    except requests.exceptions.RequestException as e: 
        raise RuntimeError(f"Network error: {e}")
    
    if r.status_code != 200:
        raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {r.text}")

    data = r.json()
    content = data["choices"][0]["message"].get("content", "").strip()

    if not content:
        raise RuntimeError("Free pool busy")

    return content

context_store = {}

def load_context(session_id):
    if session_id not in context_store:
        context_store[session_id] = []
    return context_store[session_id]


def save_message(session_id, role, text):
    if session_id not in context_store:
        context_store[session_id] = []

    context_store[session_id].append({
        "role": role,
        "text": text
    })

    
    if len(context_store[session_id]) > MAX_CONTEXT_MESSAGES:
        context_store[session_id] = context_store[session_id][-MAX_CONTEXT_MESSAGES:]


def clear_context(session_id):
    if session_id in context_store:
        del context_store[session_id]

# SEARCH DECISION
def realtime_search(message):
    keywords = [
        "today", "latest", "current", "price",
        "mandi", "weather", "aaj", "kal", "news"
    ]
    return any(k in message.lower() for k in keywords)

def search_api(query):
    time.sleep(0.5)
    return f"[SEARCH RESULT] Info related to: {query}"


# MESSAGE BUILDER
def build_messages(context_messages, search_data=None):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an agriculture assistant for farmers. "
                "Always give clear and practical answers. "
                "You MUST strictly use previous user messages for context. "
                "If you ignore earlier conditions, the answer is wrong. "
                "reply in the language, that user uses. "
            )
        }
    ]

    for msg in context_messages:
        #guard against bad data
        if not isinstance(msg, dict):
            continue

        role = msg.get("role")
        text = msg.get("text")

        if role == "ai":
            role = "assistant"

        if not isinstance(role, str):
            continue

        if not isinstance(text, str):
            text = str(text)

        messages.append({
            "role": role,
            "content": text
        })

    if search_data:
        messages.append({
            "role": "system",
            "content": str(search_data)
        })

    return messages
#LLM logic
def llm(context, search_data=None):
    messages = build_messages(context, search_data)

    for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
        try:
            return call_openrouter(model, messages)

        except RuntimeError as e:
            msg = str(e)
            if "Blocked non-free model" in msg:
                continue

            if "free pool busy" in msg or "Empty completion" in msg:
                continue

            if "HTTP 401" in msg:
                return "Warning, API key invalid."

            if "HTTP 402" in msg:
                return "Warning, Free pool unavailable. Paid usage blocked."

            if "HTTP 429" in msg:
                return "Warning, Rate limit hit. Try later."

            return f"OpenRouter error: {msg}"

    return "Warning, Free models currently unavailable. Try later."

#chat engine
def chat_engine(session_id, user_message):
    context = load_context(session_id)

    save_message(session_id, "user", user_message)
    search_data = None

    if realtime_search(user_message):
        search_data = search_api(user_message)

    
    reply = llm(
        context=context,
        search_data=search_data
    )

    if not reply.startswith(("Warning")):
        save_message(session_id, "assistant", reply)

    return reply
#for testing in dev
if __name__ == "__main__":
    print("=== AGRI CHAT ENGINE (DEV MODE) ===")
    print("Type 'exit' to quit, 'clear' to reset context\n")

    session_id = "dev-user-1" #dummy testing S_id

    while True:
        user_input = input("User: ").strip()

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "clear":
            clear_context(session_id)
            print("Bot: Context cleared.\n")
            continue

        response = chat_engine(session_id, user_input)
        print(f"Bot: {response}\n")
