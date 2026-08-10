import ollama

def classify_user_intent(user_query):
    classification_instruction = (
        "You are an elite, rapid routing switch. Analyze the user's input query "
        "and classify it into exactly ONE of these three category strings: "
        "'MATH', 'GREETING', or 'GENERAL'. "
        "Do not write explanations, greetings, or sentences. Output ONLY the raw category word."
    )
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": classification_instruction},
                {"role": "user", "content": user_query}
            ],
            options={"temperature": 0.0}
        )
        category = response['message']['content'].strip().upper().replace("'", "").replace('"', "")
        if category not in ["MATH", "GREETING", "GENERAL"]:
            category = "GENERAL"
        return category
    except Exception:
        return "GENERAL"

def process_query_through_route(category, user_query):
    if category == "GREETING":
        execution_log = "⚡ Fast-Track Route Triggered: [Static Response Engine]"
        final_answer = "Hello there! I am your agentic router switch bot. How can I direct your computational inquiries today? 👋"
        return execution_log, final_answer

    elif category == "MATH":
        try:
            # Attempt local rapid Python execution
            clean_query = user_query.lower().replace("what is", "").replace("calculate", "").replace("?", "").strip()
            clean_query = clean_query.replace("x", "*").replace("times", "*").replace("divided by", "/")
            
            calculated_result = eval(clean_query, {"__builtins__": None}, {})
            execution_log = "🐍 Functional Route Triggered: [Local Python Evaluator Math Core]"
            final_answer = f"The programmatic python calculation result equals: **{calculated_result}**"
            return execution_log, final_answer
        except Exception:
            # 🧠 SMART HANDOFF: If word math math fails, automatically pass it to Llama 3.2!
            execution_log = "🧠 Intelligent Handoff Triggered: [Python Parse Failed -> Re-routed to Llama Full Reasoning]"
            system_instruction = "You are an expert mathematical assistant. Solve the math word problem clearly and step-by-step."
            
            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_query}
                ]
            )
            final_answer = response['message']['content']
            return execution_log, final_answer

    else:
        execution_log = "🧠 Deep Reasoning Route Triggered: [Llama 3.2 Full Generative Core]"
        system_instruction = "You are a helpful knowledge assistant. Answer the question completely and factually."
        
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_query}
            ]
        )
        final_answer = response['message']['content']
        return execution_log, final_answer
