import streamlit as st
import time
from router_brain import classify_user_intent, process_query_through_route

# 1. Page Configuration and Layout
st.set_page_config(page_title="Helix Agentic Router", page_icon="🚦", layout="wide")

# 2. Inject High-Contrast CSS Styles for Interactive Traffic Routing Cards
st.markdown("""
    <style>
    .glow-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.05em;
        margin-bottom: 5px;
    }
    
    /* System theme adaptations */
    [data-theme="light"] .stMarkdown p { color: #0f172a !important; }
    [data-theme="dark"] .stMarkdown p { color: #f1f5f9 !important; }
    
    /* Route log telemetry indicator styles */
    .route-badge {
        background-color: #1e293b;
        color: #38bdf8;
        border: 1px solid #0284c7;
        border-radius: 6px;
        padding: 6px 12px;
        font-family: monospace;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="glow-title">🚦 Helix Intelligent Agentic Router</h1>', unsafe_allow_html=True)
st.write("An intent-driven optimization switcher routing queries across local code blocks and LLM reasoning cores.")

# 3. Sidebar Metric Telemetry Counters
st.sidebar.markdown("### 📊 Infrastructure Live Statistics")
if "math_count" not in st.session_state: st.session_state.math_count = 0
if "greet_count" not in st.session_state: st.session_state.greet_count = 0
if "llm_count" not in st.session_state: st.session_state.llm_count = 0

st.sidebar.metric("🔢 Total Python Math Triggers", st.session_state.math_count)
st.sidebar.metric("👋 Total Static Greeting Triggers", st.session_state.greet_count)
st.sidebar.metric("🧠 Total Full LLM Computations", st.session_state.llm_count)

# 4. User Interaction Prompt Input Row
user_input = st.text_input("Enter your question or math problem here:", placeholder="e.g., What is 125 times 5? or Hello bot!")

# 5. Core Execution Loop Trigger
if user_input:
    with st.spinner("Analyzing query intent layout structures..."):
        # Record initial execution click timestamp
        start_time = time.time()
        
        # Run step 1: Classify intent category string token
        intent_category = classify_user_intent(user_input)
        
        # Run step 2: Execute cost-optimized routing track
        route_log, answer = process_query_through_route(intent_category, user_input)
        
        # Calculate full system latency timing metrics
        execution_latency = time.time() - start_time
        
        # Update live telemetry counters inside the sidebar session data cache
        if intent_category == "MATH": st.session_state.math_count += 1
        elif intent_category == "GREETING": st.session_state.greet_count += 1
        else: st.session_state.llm_count += 1

        # 6. Render Components dynamically to User Screen Surface Panels
        st.markdown("### 🤖 Router System Output")
        
        # Color-coded visual alert statuses depending on classification type
        if intent_category == "MATH":
            st.success(f"🎯 **Intent Tagged:** `[MATH]`")
            st.markdown(f"<div class='route-badge'>{route_log}</div>", unsafe_allow_html=True)
            st.info(answer)
        elif intent_category == "GREETING":
            st.success(f"🎯 **Intent Tagged:** `[GREETING]`")
            st.markdown(f"<div class='route-badge'>{route_log}</div>", unsafe_allow_html=True)
            st.info(answer)
        else:
            st.warning(f"🎯 **Intent Tagged:** `[GENERAL REASONING]`")
            st.markdown(f"<div class='route-badge'>{route_log}</div>", unsafe_allow_html=True)
            st.markdown(answer)
            
        # Display operational metrics widget stats
        st.markdown("---")
        col1, col2 = st.columns(2)
        col1.metric("Execution Router Latency", f"{execution_latency:.3f} seconds")
        
        # Calculate computational savings feedback strings
        if intent_category in ["MATH", "GREETING"]:
            col2.metric("LLM Token Computing Cost Saved", "100.0% Saved", delta="Free Local Core")
        else:
            col2.metric("LLM Token Computing Cost Saved", "0.0% (Standard Run)", delta="Heavy LLM Core", delta_color="inverse")
