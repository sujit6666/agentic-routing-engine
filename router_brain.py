import os
import streamlit as st


def get_groq_api_key() -> str:
    """Safely extracts GROQ_API_KEY from Streamlit secrets or OS environment."""
    # 1. Direct key access in st.secrets
    if "GROQ_API_KEY" in st.secrets:
        return str(st.secrets["GROQ_API_KEY"]).strip()
    
    # 2. Key nested inside a [secrets] or custom section
    try:
        if hasattr(st.secrets, "get") and st.secrets.get("GROQ_API_KEY"):
            return str(st.secrets.get("GROQ_API_KEY")).strip()
    except Exception:
        pass

    # 3. Local OS environment fallback
    return os.environ.get("GROQ_API_KEY", "").strip()


def call_model_switch(system_instruction: str, user_prompt: str, temperature: float = 0.0) -> str:
    """Attempts local Ollama first; automatically falls back to Groq Cloud LLM."""
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
        if res and "message" in res and "content" in res["message"]:
            return res["message"]["content"]
    except Exception:
        pass

    # 2. Groq Cloud Fallback
    api_key = get_groq_api_key()
    if api_key:
        try:
            from groq import Groq
            groq_client = Groq(api_key=api_key)
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Cloud Inference Error: {e}"

    return "Error: Local Ollama daemon is offline and GROQ_API_KEY was not found in Streamlit Secrets."


def classify_user_intent(user_query: str) -> str:
    """Classifies user intent deterministically into MATH, GREETING, or GENERAL."""
    classification_instruction = (
        "You are an elite, rapid routing switch. Analyze the user's input query "
        "and classify it into exactly ONE of these three category strings: "
        "'MATH', 'GREETING', or 'GENERAL'. "
        "Do not write explanations, greetings, or sentences. Output ONLY the raw category word."
    )
    try:
        raw_output = call_model_switch(classification_instruction, user_query, temperature=0.0)
        category = raw_output.strip().upper().replace("'", "").replace('"', "").replace(".", "")
        if "MATH" in category:
            return "MATH"
        elif "GREET" in category:
            return "GREETING"
        return "GENERAL"
    except Exception:
        return "GENERAL"


def process_query_through_route(category: str, user_query: str):
    """Executes deterministic code engine or generative LLM handoff."""
    if category == "GREETING":
        execution_log = "⚡ Fast-Track Route Triggered: [Static Response Engine]"
        final_answer = "Hello there! I am your agentic router switch bot. How can I direct your computational inquiries today? 👋"
        return execution_log, final_answer

    elif category == "MATH":
        # Rapid local Python execution for clean arithmetic expressions
        try:
            clean_query = user_query.lower().replace("what is", "").replace("calculate", "").replace("?", "").strip()
            clean_query = clean_query.replace("x", "*").replace("times", "*").replace("divided by", "/")
            
            allowed_chars = set("0123456789+-*/(). %")
            if all(c in allowed_chars for c in clean_query) and any(c.isdigit() for c in clean_query):
                calculated_result = eval(clean_query, {"__builtins__": None}, {})
                execution_log = "🐍 Functional Route Triggered: [Local Python Evaluator Math Core]"
                final_answer = f"The programmatic python calculation result equals: **{calculated_result}**"
                return execution_log, final_answer
        except Exception:
            pass

        # SMART HANDOFF: Pass algebraic equations (e.g. solve 3x+5=20) or word problems to LLM
        execution_log = "🧠 Intelligent Handoff Triggered: [Python Parse Failed -> Re-routed to Full LLM Reasoning]"
        system_instruction = "You are an expert mathematical assistant. Solve the math problem clearly and step-by-step."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.1)
        return execution_log, final_answer

    else:
        execution_log = "🧠 Deep Reasoning Route Triggered: [Llama Full Generative Core]"
        system_instruction = "You are a helpful knowledge assistant. Answer the question completely and factually."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.2)
        return execution_log, final_answer