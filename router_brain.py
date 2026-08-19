import os
import re
import streamlit as st


def get_groq_client():
    """Safely initializes and returns Groq client using secrets or env vars."""
    api_key = None
    
    # 1. Check Streamlit secrets
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = str(st.secrets["GROQ_API_KEY"]).strip()
        elif hasattr(st.secrets, "get") and st.secrets.get("GROQ_API_KEY"):
            api_key = str(st.secrets.get("GROQ_API_KEY")).strip()
    except Exception:
        pass

    # 2. Check OS environment
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if not api_key:
        return None, "GROQ_API_KEY secret was not found in Streamlit Secrets or Environment."

    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        return client, None
    except Exception as e:
        return None, f"Failed to initialize Groq client: {e}"


def run_groq_inference(system_instruction: str, user_prompt: str, temperature: float = 0.0) -> str:
    """Queries Groq with official active production models."""
    client, err = get_groq_client()
    if err:
        return f"Configuration Error: {err}"

    # Active production Groq models
    active_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    
    last_err = ""
    for model_id in active_models:
        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return completion.choices[0].message.content
        except Exception as e:
            last_err = str(e)
            continue

    return f"Cloud Inference Error: {last_err}"


def solve_algebra_equation(query: str):
    """Deterministic linear equation solver for patterns like '3x+5=20' or '2x - 4 = 10'."""
    q = query.lower().replace("solve", "").replace("for x", "").replace(" ", "")
    if "=" in q:
        # Match pattern: [+-]?ax [+-] b = c
        match = re.match(r"^([+-]?\d*)x([+-]\d+)?=([+-]?\d+)$", q)
        if match:
            a_str, b_str, c_str = match.groups()
            a = 1 if a_str in ("", "+") else (-1 if a_str == "-" else int(a_str))
            b = int(b_str) if b_str else 0
            c = int(c_str)
            x_val = (c - b) / a
            step = f"1. Given: {a}x + ({b}) = {c}\n2. Subtract {b} from both sides: {a}x = {c - b}\n3. Divide by {a}: **x = {x_val:g}**"
            return f"Algebra Solution (Local Python Symbolic Engine):\n\n{step}"
    return None


def call_model_switch(system_instruction: str, user_prompt: str, temperature: float = 0.0) -> str:
    """Attempts local Ollama first; automatically falls back to Groq Cloud."""
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
    return run_groq_inference(system_instruction, user_prompt, temperature)


def classify_user_intent(user_query: str) -> str:
    """Deterministic intent classification."""
    q = user_query.strip().lower()

    greetings = {"hello", "hi", "hey", "good morning", "good evening", "howdy", "sup", "greetings"}
    if q in greetings or any(q.startswith(g + " ") for g in greetings):
        return "GREETING"

    math_indicators = ["solve", "calculate", "+", "-", "*", "/", "=", "^", "sqrt"]
    if any(ind in q for ind in math_indicators) and any(char.isdigit() for char in q):
        return "MATH"

    return "GENERAL"


def process_query_through_route(category: str, user_query: str):
    """Executes deterministic code engine or generative LLM handoff."""
    if category == "GREETING":
        execution_log = "⚡ Fast-Track Route Triggered: [Static Response Engine]"
        final_answer = "Hello there! I am your agentic router switch bot. How can I direct your computational inquiries today? 👋"
        return execution_log, final_answer

    elif category == "MATH":
        # 1. Check for linear algebraic equations (e.g. solve 3x+5=20)
        algebra_solution = solve_algebra_equation(user_query)
        if algebra_solution:
            execution_log = "🐍 Functional Route Triggered: [Local Symbolic Equation Core]"
            return execution_log, algebra_solution

        # 2. Check for standard arithmetic expressions
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

        # 3. Smart Handoff: Re-route complex word problems to LLM
        execution_log = "🧠 Intelligent Handoff Triggered: [Python Parse Failed -> Re-routed to Full LLM Reasoning]"
        system_instruction = "You are an expert mathematical assistant. Solve the math problem clearly and step-by-step."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.1)
        return execution_log, final_answer

    else:
        execution_log = "🧠 Deep Reasoning Route Triggered: [Llama Full Generative Core]"
        system_instruction = "You are a helpful knowledge assistant. Answer the question completely and factually."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.2)
        return execution_log, final_answer