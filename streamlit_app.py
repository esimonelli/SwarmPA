import streamlit as st
import os
import base64
from swarm_interface import SwarmAgentSystem

st.set_page_config(page_title="(Demo) Multi-Agent NoiPA", layout="wide", page_icon="📊")

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
    html, body, [class*="css"] {{
        font-family: 'Segoe UI', sans-serif;
        background-color: #f0f0f0 !important;
        color: #111111 !important;
    }}
    .header-container {{
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 1.5rem;
    }}
    .main-title {{ font-size: 3em; font-weight: 800; color: #3498db; margin: 0; }}
    .logo-img {{ height: 60px; margin-left: 20px; }}
    .subheader {{ font-size: 1.4em; color: #3498db; margin-bottom: 1.8em; }}
    .user-msg, .agent-msg {{
        background-color: #ffffff; padding: 1.2em; border-radius: 12px;
        margin: 0.6em 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #111111; font-size: 1.05em;
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
    <div class="main-title">Multi-Agent System Data Analysis in NoiPA</div>
    <img class="logo-img" src="data:image/png;base64,{logo_reply}">
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='subheader'>AI based System capable of analyzing Public Administration data in natural language: <b>Salaries</b>, <b>Income</b>, <b>Accesses</b>, <b>Commuting</b></div>", unsafe_allow_html=True)

# Inizializzazione sistema agenti e stato memoria
if "swarm_agent" not in st.session_state:
    st.session_state.swarm_agent = SwarmAgentSystem()
    st.session_state.chat_history = []
    st.session_state.last_semantic_prompt = None

# Esempi suggeriti con selezione lingua
with st.expander("Choose the language and see some examples 💡"):
    lingua = st.selectbox("Lingua degli esempi", ["Italiano", "English"], index=0, key="lingua_selector")

    esempi = {
        "Italiano": [
            "Qual è la media degli accrediti per le donne a Milano?",
            "E per gli uomini?",
            "Fammi un grafico della distribuzione degli accessi digitali al portale NoiPA diviso per regione",
            "Qual è la distribuzione dei dipendenti per fascia d'età e genere?",
            "Ora genera un barplot con split per genere della distribuzione appena calcolata",
            "Qual è la percentuale di uomini e donne per ogni fascia di reddito?",
            "Calcola la distribuzione percentuale delle modalità di accesso al portale NoiPA tra gli utenti di età compresa tra i 18 e i 30 anni rispetto a quelli di età superiore ai 50 anni, suddivisa per regione di residenza",
            "Identifica il metodo di pagamento più utilizzato per ciascuna fascia d'età e genera un grafico che mostri se esistono correlazioni tra genere e preferenza del metodo di pagamento",
            "Analizza i dati sui pendolari per identificare quali amministrazioni hanno la percentuale più alta di dipendenti che percorrono più di 20 miglia per recarsi al lavoro",
            "Confronta la distribuzione di genere del personale tra i cinque comuni con il maggior numero di dipendenti, evidenziando eventuali differenze significative nella rappresentanza per fascia d'età",
            "Determina se esiste una correlazione tra la modalità di accesso al portale e la distanza media percorsa per il tragitto casa-lavoro per ciascuna amministrazione"
        ],
        "English": [
            "What is the average salary payment for women in Milan?",
            "And for men?",
            "Show me a bar chart of digital access to the NoiPA portal broken down by region",
            "What is the employee distribution by age group and gender?",
            "Now generate a barplot split by gender for the previous distribution",
            "What is the percentage of men and women in each income bracket?",
            "Calculate the percentage distribution of access methods to the NoiPA portal among users aged 18–30 versus those over 50, split by region of residence",
            "Identify the most used payment method for each age group and generate a graph showing correlations between gender and payment preference",
            "Analyze commuter data to identify which administrations have the highest percentage of employees traveling more than 20 miles to work",
            "Compare gender distribution of staff among the top five municipalities with the highest number of employees, highlighting any significant differences by age group",
            "Determine whether there's a correlation between access method and average commuting distance for each administration"
        ]
    }

    for esempio in esempi[lingua]:
        st.markdown(f"- \"{esempio}\"")

# Input utente
user_input = st.chat_input("💬 Fai una domanda sui dati/ ask something...")
if user_input:
    with st.spinner("🤖 Sto elaborando la tua richiesta..."):
        result = st.session_state.swarm_agent.process_query(
            user_input,
            previous_prompt=st.session_state.last_semantic_prompt
        )

    st.session_state.last_semantic_prompt = user_input
    st.session_state.chat_history.append({
        "user": user_input,
        "response": result["message"],
        "type": result["type"],
        "image": result.get("image_path")
    })

# Visualizzazione chat
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
                href = f'<a class="download-btn" style="color: black;" href="data:image/png;base64,{b64}" download="grafico_generato.png">Scarica il grafico</a>'
                st.markdown(f"<div style='text-align: center'>{href}</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
---
<center><small><i style='color:#888'>Powered by OpenAI · Swarm · LlamaIndex · Streamlit</i></small></center>
""", unsafe_allow_html=True)
