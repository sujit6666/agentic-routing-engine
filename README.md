# 🚦 Helix Intelligent Agentic Router Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://helix-agentic-router.streamlit.app/)

An intent-driven LLM optimization switcher built to analyze user queries, tag their underlying intentions, and dynamically route them across cost-effective local code scripts and generative reasoning cores.

🔗 **Live App:** https://helix-agentic-router.streamlit.app/

## 🚀 Key Architectural Features
- **Deterministic Intent Classification:** Rapidly categorizes queries into 'MATH', 'GREETING', or 'GENERAL' using zero-temperature intent switch gates.
- **Smart Computational Fallbacks:** Features an automated parse guardian. Simple arithmetic is handled instantly for free by local Python, while complex word problems are smoothly re-routed to full LLM reasoning blocks.
- **Live Infrastructure Telemetry:** Renders real-time execution statistics tracking processing counts, route latency metrics, and computed token cost savings.
- **Hybrid Cloud Fallback:** Prioritizes local Ollama inference while seamlessly routing requests through Groq cloud execution for live web deployments.

## 🛠️ Project File Components
- `app.py`: Interactive Streamlit web interface dashboard presenting visual gauges and latency logs.
- `router_brain.py`: The routing core module processing the dual-step classification and fallback handoff loops.
- `requirements.txt`: Production dependency specifications for cloud hosting environments.
- `.gitignore`: Filtering matrix layout file masking local environments and python caching dependencies.

## ⚙️ Quick Installation Guide
To launch this intelligent traffic router framework locally on your computer device terminal:

```cmd
# Activate your python sandbox environment
venv\Scripts\activate

# Install the required modeling and web server dependencies
pip install -r requirements.txt

# Boot up the interactive visualization panel
streamlit run app.py