import os
import streamlit as st

# Cloud Fallback Inference Helper
try:
    from groq import Groq
    groq_api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
except Exception:
    groq_client = None

def call_model_switch(system_instruction: str, user_prompt: str, temperature: float = 0.0) -> str:
    """Attempts local Ollama first; falls back to Groq Cloud LLM automatically."""
    # 1. Local Ollama Attempt
    try:
        import ollama
        res = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": temperature}
        )
        return res["message"]["content"]
    except Exception:
        pass

    # 2. Groq Cloud Fallback
    if groq_client and groq_client.api_key:
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Cloud Inference Error: {e}"

    return "Error: Local Ollama offline and no GROQ_API_KEY found in Streamlit Secrets."


def classify_user_intent(user_query: str) -> str:
    classification_instruction = (
        "You are an elite, rapid routing switch. Analyze the user's input query "
        "and classify it into exactly ONE of these three category strings: "
        "'MATH', 'GREETING', or 'GENERAL'. "
        "Do not write explanations, greetings, or sentences. Output ONLY the raw category word."
    )
    try:
        raw_output = call_model_switch(classification_instruction, user_query, temperature=0.0)
        category = raw_output.strip().upper().replace("'", "").replace('"', "")
        if category not in ["MATH", "GREETING", "GENERAL"]:
            category = "GENERAL"
        return category
    except Exception:
        return "GENERAL"


def process_query_through_route(category: str, user_query: str):
    if category == "GREETING":
        execution_log = "⚡ Fast-Track Route Triggered: [Static Response Engine]"
        final_answer = "Hello there! I am your agentic router switch bot. How can I direct your computational inquiries today? 👋"
        return execution_log, final_answer

    elif category == "MATH":
        try:
            # Rapid local Python execution
            clean_query = user_query.lower().replace("what is", "").replace("calculate", "").replace("?", "").strip()
            clean_query = clean_query.replace("x", "*").replace("times", "*").replace("divided by", "/")
            
            calculated_result = eval(clean_query, {"__builtins__": None}, {})
            execution_log = "🐍 Functional Route Triggered: [Local Python Evaluator Math Core]"
            final_answer = f"The programmatic python calculation result equals: **{calculated_result}**"
            return execution_log, final_answer
        except Exception:
            # SMART HANDOFF: Pass word math or complex equations to LLM
            execution_log = "🧠 Intelligent Handoff Triggered: [Python Parse Failed -> Re-routed to Full LLM Reasoning]"
            system_instruction = "You are an expert mathematical assistant. Solve the math problem clearly and step-by-step."
            final_answer = call_model_switch(system_instruction, user_query, temperature=0.1)
            return execution_log, final_answer

    else:
        execution_log = "🧠 Deep Reasoning Route Triggered: [Llama Full Generative Core]"
        system_instruction = "You are a helpful knowledge assistant. Answer the question completely and factually."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.2)
        return execution_log, final_answer