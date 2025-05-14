import streamlit as st
import os
import base64
from swarm_interface import SwarmAgentSystem

st.set_page_config(page_title="(Demo) Multi-Agent NoiPA", layout="wide", page_icon="📊")

# Logo opzionale
logo_path = "Logo_Reply.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_reply = base64.b64encode(f.read()).decode()
else:
    logo_reply = ""

# Lingua UI
if "ui_language" not in st.session_state:
    st.session_state.ui_language = "it"

col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown(f"""
    <div class="main-title">TriplePA – Multi-Agent System for Data Analysis in NoiPA</div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("**Seleziona Lingua / Select Language**", unsafe_allow_html=True)
    lang_choice = st.radio("", ["🇮🇹", "🇬🇧"], horizontal=True, label_visibility="collapsed")
    st.session_state.ui_language = "it" if lang_choice == "🇮🇹" else "en"

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
    <img class="logo-img" src="data:image/png;base64,{logo_reply}">
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subheader'>Multi-Agent System capable of analyzing Public Administration data in natural language: <b>Salaries</b>, <b>Income</b>, <b>Accesses</b>, <b>Commuting</b></div>
""", unsafe_allow_html=True)

# Inizializzazione sistema agenti e stato memoria
if "swarm_agent" not in st.session_state:
    st.session_state.swarm_agent = SwarmAgentSystem()
    st.session_state.chat_history = []
    st.session_state.last_semantic_prompt = None

# Esempi suggeriti
with st.expander("💡 Examples"):
    if st.session_state.ui_language == "it":
        st.markdown("""
        - "Qual è la media degli accrediti per le donne a Milano?"
        - "E per gli uomini?"
        - "Fammi un grafico della distribuzione degli accessi digitali al portale NoiPA diviso per regione"
        - "Qual è la distribuzione dei dipendenti per fascia d'età e genere?"
        - "Ora genera un barplot con split per genere della distribuzione appena calcolata"
        - "Qual è la percentuale di uomini e donne per ogni fascia di reddito?"
        - "Calcola la distribuzione percentuale delle modalità di accesso al portale NoiPA tra gli utenti di età compresa tra i 18 e i 30 anni rispetto a quelli di età superiore ai 50 anni, suddivisa per regione di residenza"
        - "Identifica il metodo di pagamento più utilizzato per ciascuna fascia d'età e genera un grafico che mostri se esistono correlazioni tra genere e preferenza del metodo di pagamento"
        - "Analizza i dati sui pendolari per identificare quali amministrazioni hanno la percentuale più alta di dipendenti che percorrono più di 20 miglia per recarsi al lavoro"
        - "Confronta la distribuzione di genere del personale tra i cinque comuni con il maggior numero di dipendenti, evidenziando eventuali differenze significative nella rappresentanza per fascia d'età"
        - "Determina se esiste una correlazione tra la modalità di accesso al portale e la distanza media percorsa per il tragitto casa-lavoro per ciascuna amministrazione"
        """)
    else:
        st.markdown("""
        - "What is the average number of credits for women in Milan?"
        - "And for men?"
        - "Create a chart showing the distribution of digital accesses to the NoiPA portal by region"
        - "What is the distribution of employees by age group and gender?"
        - "Now generate a barplot split by gender for the distribution just calculated"
        - "What is the percentage of men and women in each income bracket?"
        - "Calculate the percentage distribution of portal access methods among users aged 18–30 compared to those over 50, by region of residence"
        - "Identify the most used payment method for each age group and generate a chart showing correlations between gender and payment preference"
        - "Analyze commuter data to identify which administrations have the highest percentage of employees commuting more than 20 miles to work"
        - "Compare the gender distribution of staff in the five municipalities with the highest number of employees, highlighting significant differences by age group"
        - "Determine whether there is a correlation between portal access mode and average commuting distance by administration"
        """)

# Footer
st.markdown("""
---
<center><small><i style='color:#888'>Powered by OpenAI · Swarm · LlamaIndex · Streamlit</i></small></center>
""", unsafe_allow_html=True)

