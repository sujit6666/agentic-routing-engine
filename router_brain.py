import os
import re
import math
import streamlit as st


def get_groq_client():
    """Extracts API key and initializes Groq client safely across environments."""
    api_key = None
    
    # 1. Streamlit Cloud secrets lookup
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = str(st.secrets["GROQ_API_KEY"]).strip()
        elif hasattr(st.secrets, "get") and st.secrets.get("GROQ_API_KEY"):
            api_key = str(st.secrets.get("GROQ_API_KEY")).strip()
    except Exception:
        pass

    # 2. Local environment fallback
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if not api_key:
        return None, "GROQ_API_KEY was not found in Streamlit Secrets or Environment."

    try:
        from groq import Groq
        return Groq(api_key=api_key), None
    except Exception as e:
        return None, f"Groq initialization error: {e}"


def run_groq_inference(system_instruction: str, user_prompt: str, temperature: float = 0.1) -> str:
    """Queries Groq by dynamically discovering available production models on your key."""
    client, err = get_groq_client()
    if err:
        return f"Configuration Error: {err}"

    # Default production models prioritized by availability
    candidate_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "llama3-70b-8192",
        "llama3-8b-8192"
    ]

    # Dynamically detect active models permitted on your specific Groq key
    try:
        active_key_models = [
            m.id for m in client.models.list().data 
            if not any(x in m.id for x in ["whisper", "guard", "vision", "embed"])
        ]
        if active_key_models:
            candidate_models = active_key_models + candidate_models
    except Exception:
        pass

    last_error = ""
    for model_id in candidate_models:
        try:
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            last_error = str(e)
            continue

    return f"Cloud Inference Error: {last_error}"


# ==========================================
# LOCAL ZERO-COST MATH COMPUTATION ENGINES
# ==========================================

def solve_algebraic_equation(query: str):
    """Solves linear equations like 3x+5=20, 2x-8=10, 4x=100, x/2=15."""
    clean = query.lower().replace("solve", "").replace("for x", "").replace("find x", "").replace(" ", "")
    if "=" in clean:
        parts = clean.split("=")
        if len(parts) == 2:
            left, right = parts[0], parts[1]
            # Match standard ax + b = c pattern
            match = re.match(r"^([+-]?\d*(?:\.\d+)?)x([+-]\d+(?:\.\d+)?)?$", left)
            if match and re.match(r"^[+-]?\d+(?:\.\d+)?$", right):
                a_str, b_str = match.groups()
                a = 1.0 if a_str in ("", "+") else (-1.0 if a_str == "-" else float(a_str))
                b = float(b_str) if b_str else 0.0
                c = float(right)
                
                if a != 0:
                    x_val = (c - b) / a
                    x_formatted = int(x_val) if x_val.is_integer() else round(x_val, 4)
                    return (
                        f"**Algebraic Solution (Local Symbolic Solver)**\n\n"
                        f"1. Given Equation: `{a:g}x + ({b:g}) = {c:g}`\n"
                        f"2. Isolate variable: `{a:g}x = {c - b:g}`\n"
                        f"3. Divide by coefficient: **x = {x_formatted}**"
                    )
    return None


def calculate_general_math(query: str):
    """Evaluates arithmetic, powers, roots, percentages, and natural language math."""
    q = query.lower().strip()
    
    # Strip common conversational math question prefixes
    for prefix in ["what is", "calculate", "compute", "how much is", "evaluate", "value of", "solve", "?", "!"]:
        q = q.replace(prefix, "")

    # Natural language operator normalization
    replacements = {
        "multiplied by": "*", "times": "*", "into": "*", "x": "*",
        "divided by": "/", "over": "/", "by": "/",
        "plus": "+", "add": "+", "added to": "+",
        "minus": "-", "subtract": "-", "subtracted from": "-",
        "power of": "**", "power": "**", "^": "**",
        "squared": "**2", "cubed": "**3",
        "percent of": "/100*", "percentage of": "/100*", "% of": "/100*"
    }
    for word, sym in replacements.items():
        q = q.replace(word, sym)

    # Square root support: "sqrt(144)" or "sqrt 144"
    if "sqrt" in q:
        q = re.sub(r"sqrt\s*\(?(\d+(?:\.\d+)?)\)?", r"math.sqrt(\1)", q)

    allowed_chars = set("0123456789+-*/(). %math.sqrt")
    clean_q = "".join(c for c in q if c in allowed_chars).strip()

    if clean_q and any(c.isdigit() for c in clean_q):
        try:
            safe_scope = {"__builtins__": None, "math": math}
            result = eval(clean_q, safe_scope, {})
            formatted_res = int(result) if isinstance(result, float) and result.is_integer() else round(result, 4)
            return f"Calculated Result (Deterministic Python Core): **{formatted_res}**"
        except Exception:
            return None
    return None


# ==========================================
# CLASSIFICATION & ROUTING SWITCH
# ==========================================

def call_model_switch(system_instruction: str, user_prompt: str, temperature: float = 0.0) -> str:
    """Routes to local Ollama if active; otherwise fails over to Groq Cloud."""
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

    return run_groq_inference(system_instruction, user_prompt, temperature)


def classify_user_intent(user_query: str) -> str:
    """Fast deterministic intent categorizer."""
    q = user_query.strip().lower()

    # 1. Greetings Gate
    greetings = {"hello", "hi", "hey", "good morning", "good evening", "howdy", "sup", "greetings"}
    if q in greetings or any(q.startswith(g + " ") for g in greetings) or any(q == g for g in greetings):
        return "GREETING"

    # 2. Math Gate (Words, numbers, or symbols)
    math_signals = [
        "+", "-", "*", "/", "=", "^", "%", "sqrt", "solve", "calculate", "compute",
        "times", "plus", "minus", "divided", "multiply", "algebra", "equation", "integral", "derivative"
    ]
    if any(sig in q for sig in math_signals) and any(char.isdigit() for char in q):
        return "MATH"

    return "GENERAL"


def process_query_through_route(category: str, user_query: str):
    """Executes deterministic code engine or generative LLM handoff."""
    if category == "GREETING":
        execution_log = "⚡ Fast-Track Route Triggered: [Static Response Engine]"
        final_answer = "Hello! I am your agentic router switch bot. How can I direct your computational inquiries today? 👋"
        return execution_log, final_answer

    elif category == "MATH":
        # 1. Check for linear algebraic equations (e.g. solve 3x+5=20)
        algebra_res = solve_algebraic_equation(user_query)
        if algebra_res:
            execution_log = "🐍 Functional Route Triggered: [Local Symbolic Equation Core]"
            return execution_log, algebra_res

        # 2. Check for arithmetic and natural language calculations (e.g. 125 times 5, 25% of 800, sqrt 144)
        general_math_res = calculate_general_math(user_query)
        if general_math_res:
            execution_log = "🐍 Functional Route Triggered: [Local Python Evaluator Math Core]"
            return execution_log, general_math_res

        # 3. Smart Fallback for complex word problems, proofs, or calculus
        execution_log = "🧠 Intelligent Handoff Triggered: [Complex Query -> Re-routed to Deep Reasoning LLM]"
        system_instruction = "You are an expert mathematical and analytical reasoning engine. Solve the problem thoroughly with clear, step-by-step mathematical logic."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.1)
        return execution_log, final_answer

    else:
        execution_log = "🧠 Deep Reasoning Route Triggered: [Llama Full Generative Core]"
        system_instruction = "You are a helpful knowledge and analytical reasoning assistant. Answer questions clearly, accurately, and thoroughly."
        final_answer = call_model_switch(system_instruction, user_query, temperature=0.2)
        return execution_log, final_answer