import streamlit as st
import os
import base64
from swarm_interface import SwarmAgentSystem

st.set_page_config(page_title="Swarm Multi-Agent – PA Italiana", layout="wide", page_icon="📊")

# Logo opzionale (assicurati che sia presente il file Logo_Reply.png)
logo_path = "Logo_Reply.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_reply = base64.b64encode(f.read()).decode()
else:
    logo_reply = ""

# Stili globali
st.markdown(f"""
<style>
    :root {{ color-scheme: dark; }}
    html, body, [class*="css"] {{
        font-family: 'Segoe UI', sans-serif;
        background-color: #0e1117 !important;
        color: #f5f5f5 !important;
    }}
    .header-container {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 1.5rem;
    }}
    .main-title {{ font-size: 2.3em; font-weight: 800; color: #ffffff; margin: 0; }}
    .logo-img {{ height: 60px; margin-left: 20px; }}
    .subheader {{ font-size: 1.2em; color: #cfcfcf; margin-bottom: 1.8em; }}
    .user-msg, .agent-msg {{
        background-color: #1c1c1c; padding: 1.2em; border-radius: 12px;
        margin: 0.6em 0; box-shadow: 0 2px 8px rgba(255,255,255,0.1);
        color: #f1f1f1; font-size: 1.05em;
    }}
    .user-msg {{ border-left: 5px solid #3498db; }}
    .agent-msg {{ border-left: 5px solid #2ecc71; }}
    .download-btn {{
        margin-top: 1em; display: inline-block; background-color: #27ae60;
        color: white; padding: 0.6em 1.5em; text-decoration: none;
        border-radius: 8px; font-weight: 600;
    }}
    .download-btn:hover {{ background-color: #1f8e4d; }}
</style>
<div class="header-container">
    <div class="main-title">🧠 Swarm Multi-Agent – Analisi PA Italiana</div>
    <img class="logo-img" src="data:image/png;base64,{logo_reply}">
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='subheader'>Analizza i dati della PA in linguaggio naturale: <b>Stipendi</b>, <b>Redditi</b>, <b>Accessi</b>, <b>Pendolarismo</b></div>", unsafe_allow_html=True)

if "swarm_agent" not in st.session_state:
    st.session_state.swarm_agent = SwarmAgentSystem()
    st.session_state.chat_history = []

with st.expander("💡 Esempi utili"):
    st.markdown("""
    - "Qual è la media degli accrediti per le donne a Milano?"
    - "Fammi un grafico della distribuzione degli accessi digitali per regione"
    - "Qual è la distribuzione dei dipendenti per fascia d'età e genere?"
    - "Ora genera un barplot con split per genere della distribuzione appena calcolata"
    """)

user_input = st.chat_input("💬 Fai una domanda sui dati...")
if user_input:
    with st.spinner("🤖 Sto elaborando la tua richiesta..."):
        result = st.session_state.swarm_agent.process_query(user_input)

    st.session_state.chat_history.append({
        "user": user_input,
        "response": result["message"],
        "type": result["type"],
        "image": result.get("image_path")
    })

for entry in st.session_state.chat_history:
    with st.chat_message("Utente"):
        st.markdown(f"<div class='user-msg'>{entry['user']}</div>", unsafe_allow_html=True)

    with st.chat_message("Agente"):
        html_response = "<div class='agent-msg'>"
        if entry["type"] == "visualization" and entry.get("image"):
            image_path = entry["image"]
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            html_response += f"<img src='data:image/png;base64,{img_data}' style='width: 100%; border-radius: 6px; margin-bottom: 1em;' />"
        html_response += f"{entry['response']}</div>"
        st.markdown(html_response, unsafe_allow_html=True)

        if entry["type"] == "visualization" and entry.get("image"):
            with open(entry["image"], "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
                href = f'<a class="download-btn" href="data:image/png;base64,{b64}" download="grafico_generato.png">Scarica il grafico</a>'
                st.markdown(f"<div style='text-align: center'>{href}</div>", unsafe_allow_html=True)

st.markdown("""
---
<center><small><i style='color:#888'>Powered by OpenAI · Swarm · LlamaIndex · Streamlit</i></small></center>
""", unsafe_allow_html=True)
