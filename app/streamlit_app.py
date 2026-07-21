"""
Dashboard de monitoramento multimodal de pacientes.

Integra os três módulos do sistema num único fluxo e gera um ALERTA CONSOLIDADO:
    áudio  →  vídeo  →  anomalias em vitais  →  alerta final à equipe

Rodar:
    streamlit run streamlit_app.py

Estado atual dos módulos:
    - Vitais  : funcional (Isolation Forest sobre o CSV do repo).
    - Áudio   : palavras-chave críticas funcionais (string matching);
                transcrição + sentimento ficam como stub até o Azure.
    - Vídeo   : consome um JSON de resultado da análise de pose;
                mostra exemplo enquanto não há vídeo processado.
"""

import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest

# --------------------------------------------------------------------------- #
# Configuração e caminhos
# --------------------------------------------------------------------------- #
st.set_page_config(page_title="Monitoramento Multimodal de Pacientes",
                   page_icon="🏥", layout="wide")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_VITAIS = os.path.join(BASE, "data", "vitals", "vitais_simulados.csv")
JSON_VIDEO = os.path.join(BASE, "data", "video", "resultado_pose.json")
JSON_AUDIO = os.path.join(BASE, "data", "audio", "resultado_audio.json")

FEATURES = ["heart_rate", "spo2", "systolic_bp",
            "diastolic_bp", "temperature", "resp_rate"]

PALAVRAS_CRITICAS = [
    "dor no peito", "falta de ar", "tontura", "desmaio",
    "dormência", "visão turva", "dor de cabeça forte", "formigamento",
]

TEXTO_EXEMPLO = (
    "Doutor, desde ontem estou com uma dor no peito que vai e volta, "
    "e hoje de manhã senti falta de ar ao subir as escadas. "
    "Também tive um pouco de tontura, mas já melhorou."
)


# --------------------------------------------------------------------------- #
# Módulo: vitais
# --------------------------------------------------------------------------- #
@st.cache_data
def carregar_vitais():
    return pd.read_csv(CSV_VITAIS, parse_dates=["timestamp"])


def detectar_anomalias_vitais(df, contamination=0.06):
    iso = IsolationForest(contamination=contamination, random_state=42)
    pred = iso.fit_predict(df[FEATURES])
    out = df.copy()
    out["anomalia"] = (pred == -1).astype(int)
    out["score"] = -iso.score_samples(df[FEATURES])
    return out


# --------------------------------------------------------------------------- #
# Módulo: áudio (palavras-chave críticas — funcional sem Azure)
# --------------------------------------------------------------------------- #
def detectar_palavras_criticas(texto):
    t = (texto or "").lower()
    return [p for p in PALAVRAS_CRITICAS if p in t]


def carregar_audio():
    """Resultado real do Azure, se existir; senão None (stub)."""
    if os.path.exists(JSON_AUDIO):
        with open(JSON_AUDIO, encoding="utf-8") as f:
            return json.load(f)
    return None


# --------------------------------------------------------------------------- #
# Módulo: vídeo (consome JSON de resultado da análise de pose)
# --------------------------------------------------------------------------- #
def carregar_video():
    if os.path.exists(JSON_VIDEO):
        with open(JSON_VIDEO, encoding="utf-8") as f:
            return json.load(f), True
    # exemplo enquanto não há vídeo processado
    exemplo = [
        {"timestamp": "3.20s–4.85s", "tipo": "movimento",
         "articulacao": "joelho_direito",
         "detalhe": "ângulo 42.0–58.0° fora da faixa 70–170°"},
    ]
    return exemplo, False


# --------------------------------------------------------------------------- #
# Interface
# --------------------------------------------------------------------------- #
st.title("🏥 Monitoramento Multimodal de Pacientes")
st.caption("Integração de áudio, vídeo e sinais vitais — alerta consolidado para a equipe de saúde")

with st.sidebar:
    st.header("⚙️ Parâmetros")
    contamination = st.slider("Sensibilidade (contamination) — vitais",
                              0.01, 0.15, 0.06, 0.01)
    st.markdown("---")
    st.caption("Dados simulados / gravados — não são de pacientes reais.")

col_a, col_v, col_s = st.columns(3)

# ---- Áudio ---------------------------------------------------------------- #
with col_a:
    st.subheader("🎙️ Áudio")
    texto = st.text_area("Transcrição do relato do paciente",
                         value=TEXTO_EXEMPLO, height=140)
    criticas = detectar_palavras_criticas(texto)
    audio_real = carregar_audio()
    if criticas:
        st.error("Palavras-chave críticas: " + ", ".join(criticas))
    else:
        st.success("Nenhuma palavra-chave crítica encontrada.")
    if audio_real:
        st.metric("Sentimento (Azure)", audio_real.get("sentimento", "—"))
    else:
        st.info("Transcrição automática e sentimento: **pendente (Azure)**.")

# ---- Vídeo ---------------------------------------------------------------- #
with col_v:
    st.subheader("🎥 Vídeo (pose)")
    alertas_video, video_real = carregar_video()
    if not video_real:
        st.info("Exemplo — aguardando um vídeo processado "
                "(`data/video/resultado_pose.json`).")
    if alertas_video:
        st.warning(f"{len(alertas_video)} anomalia(s) de movimento")
        st.dataframe(pd.DataFrame(alertas_video), hide_index=True,
                     width="stretch")
    else:
        st.success("Nenhuma anomalia de movimento.")

# ---- Vitais --------------------------------------------------------------- #
with col_s:
    st.subheader("📈 Vitais")
    df = carregar_vitais()
    dfa = detectar_anomalias_vitais(df, contamination)
    n_anom = int(dfa["anomalia"].sum())
    st.metric("Anomalias detectadas", n_anom, f"de {len(dfa)} leituras")
    ultimo = dfa.iloc[-1]
    st.caption(f"Última leitura — FC {ultimo.heart_rate:.0f} bpm · "
               f"SpO₂ {ultimo.spo2:.0f}% · PA {ultimo.systolic_bp:.0f}/"
               f"{ultimo.diastolic_bp:.0f}")

# ---- Série temporal dos vitais ------------------------------------------- #
st.markdown("### Sinais vitais ao longo do tempo")
sinal = st.selectbox("Sinal", FEATURES, index=0)
serie = dfa[["timestamp", sinal, "anomalia"]].set_index("timestamp")
st.line_chart(serie[sinal])
anoms = dfa[dfa["anomalia"] == 1][["timestamp", sinal, "score"]]
with st.expander(f"Ver {len(anoms)} leituras anômalas ({sinal})"):
    st.dataframe(anoms, hide_index=True, width="stretch")

# --------------------------------------------------------------------------- #
# Alerta consolidado
# --------------------------------------------------------------------------- #
st.markdown("---")
st.header("🚨 Alerta consolidado")

motivos = []
if criticas:
    motivos.append(f"Áudio: {len(criticas)} palavra(s) crítica(s) — {', '.join(criticas)}")
if alertas_video:
    motivos.append(f"Vídeo: {len(alertas_video)} anomalia(s) de movimento")
if n_anom:
    motivos.append(f"Vitais: {n_anom} leitura(s) anômala(s)")

c1, c2, c3 = st.columns(3)
c1.metric("🎙️ Palavras críticas", len(criticas))
c2.metric("🎥 Anomalias de movimento", len(alertas_video))
c3.metric("📈 Anomalias em vitais", n_anom)

if motivos:
    st.error("**ATENÇÃO DA EQUIPE NECESSÁRIA**\n\n- " + "\n- ".join(motivos))
else:
    st.success("Nenhum alerta — paciente dentro dos parâmetros monitorados.")
