# Relatório Técnico — Sistema de Monitoramento Multimodal de Pacientes

**8IADT — Tech Challenge Fase 4**
Repositório: https://github.com/joaovpires/8iadt-tech-challenge-fase4

> Documento vivo — as seções de áudio serão completadas quando o serviço Azure for integrado.

## 1. Objetivo
Construir um sistema que integra **três fontes de dados** (áudio, vídeo e sinais vitais)
para detectar situações de risco em pacientes e emitir um **alerta consolidado** para a
equipe de saúde. Cada modalidade é processada por uma técnica própria e os resultados
convergem num painel único.

## 2. Arquitetura multimodal
Fluxo: **áudio → vídeo → sinais vitais → alerta consolidado**.

Cada módulo expõe uma função que devolve seus alertas num **formato padronizado**
(`{timestamp, tipo, detalhe...}`), e o dashboard agrega os três. Estrutura do repositório:

```
audio/     análise de fala (palavras-chave + Azure)
video/     análise de pose (MediaPipe)
anomaly/   detecção de anomalias em vitais
app/       dashboard Streamlit (integração)
data/      dados de exemplo (vitais, vídeo, áudio)
docs/      este relatório
```

## 3. Dados utilizados
> **Decisão ética:** não há dados reais de pacientes (privacidade). Vitais são simulados,
> o vídeo é de banco livre e o áudio será fictício. Limitação assumida e aceita.

- **Vitais** — série sintética `vitais_simulados.csv`: **720 leituras** (1/min ≈ 12h),
  colunas `heart_rate, spo2, systolic_bp, diastolic_bp, temperature, resp_rate`. Geração por
  distribuição gaussiana (Box-Muller) com valores basais fisiológicos (FC 75±4, SpO₂ 98±0,6,
  PA 118/78, Temp 36,6, FR 15). Contém **43 anomalias (5,97%)** injetadas de propósito em 3
  janelas, com coluna `anomalia_esperada` como *ground truth*:
  - **Taquicardia** (FC ~145, FR ~24)
  - **Hipóxia** (SpO₂ ~86, FC ~105)
  - **Hipertensão** (PA ~165/102)
- **Vídeo** — clipe de agachamento do **Pexels** (id 5025965, licença Pexels livre),
  1080×1920, 25 fps, **15,8 s (395 frames)**. Fonte/licença registradas por transparência.
- **Áudio** — pendente (será gravado/TTS quando o módulo Azure estiver ativo).

## 4. Módulo de sinais vitais (anomalias)
**Notebook:** `anomaly/deteccao_anomalias.ipynb` · **Status: pronto e executado.**

**Métodos:**
- **z-score** (baseline univariado): anômalo se algum sinal está a > 3 desvios-padrão da média.
- **Isolation Forest** (multivariado, scikit-learn), `contamination=0.06` (calibrado na taxa
  real de 5,97%).

**Resultados medidos (contra o ground truth de 43 anomalias):**

| Modelo | Detectadas | Matriz de confusão | Precision | Recall | F1 |
|---|---|---|---|---|---|
| z-score | 46 | TN 674 · FP 3 · FN 0 · TP 43 | 0,935 | 1,000 | 0,966 |
| **Isolation Forest** | 44 | TN 676 · FP 1 · FN 0 · TP 43 | **0,977** | **1,000** | **0,989** |

O Isolation Forest capturou **todas as 43 anomalias** com apenas 1 falso positivo.

**Regra de evolução de prescrição:** sobre um histórico fictício (Losartana 50→50→100→160 mg),
alerta quando a dose varia mais que **50%** entre consultas → disparou em **+100%** e **+60%**
(2 alertas).

**Saída padronizada:** a função `anomalias_vitais()` devolve **46 alertas** (44 de vitais +
2 de prescrição) no formato consumido pelo dashboard.

## 5. Módulo de vídeo (pose)
**Notebook:** `video/analise_pose.ipynb` · **Status: pronto e executado no vídeo real.**

**Método:**
- Estimativa de pose frame-a-frame com **MediaPipe — API Tasks (`PoseLandmarker`)**, modelo
  `pose_landmarker_lite` (float16, 5,8 MB, baixado automaticamente).
- Cálculo do **ângulo do joelho direito** (landmarks quadril=24, joelho=26, tornozelo=28)
  via produto vetorial → `arccos`.
- **Regra de anomalia:** ângulo fora da faixa esperada **[70°, 170°]** por **≥ 5 frames
  consecutivos** (o mínimo de frames evita disparo por ruído de um frame isolado).

> **Nota técnica:** o MediaPipe recente removeu a API legada `solutions`; o notebook foi
> implementado na **API Tasks**, atual e compatível com o Colab e versões recentes.

**Resultados medidos:**
- Pose detectada em **395/395 frames (100%)**.
- Ângulo do joelho: **mín 34,3° · máx 175,8° · média 94,6°**.
- **8 janelas de anomalia** detectadas com timestamps — correspondem às **8 repetições** do
  agachamento (o joelho flexiona até ~35°, ultrapassando o limite inferior de 70°):

| # | Intervalo | Ângulo mínimo |
|---|---|---|
| 1 | 0,56–1,36 s | 37,6° |
| 2 | 2,48–3,32 s | 35,8° |
| 3 | 4,48–5,24 s | 35,8° |
| 4 | 6,44–7,28 s | 36,1° |
| 5 | 8,44–9,28 s | 35,7° |
| 6 | 10,40–11,16 s | 36,7° |
| 7 | 12,44–13,24 s | 34,3° |
| 8 | 14,40–15,12 s | 35,9° |

O resultado é exportado para `data/video/resultado_pose.json`. **Interpretação honesta:**
neste vídeo a regra sinaliza a fase de **flexão profunda** de cada repetição; num uso clínico
os limiares seriam calibrados para separar execução correta de incorreta.

## 6. Módulo de áudio
**Status: parcial.**

- ✅ **Detecção de palavras-chave críticas** — funcional, sem dependência externa (string
  matching sobre lista: *dor no peito, falta de ar, tontura, desmaio, dormência, visão turva,
  dor de cabeça forte, formigamento*). No texto de exemplo disparou **3 alertas**.
- 🟡 **Pendente (Azure):** transcrição automática (**Speech-to-Text**) e análise de
  **sentimento/entidades** (**Text Analytics**). A arquitetura já prevê o consumo de
  `data/audio/resultado_audio.json`.

## 7. Integração — dashboard
**Arquivo:** `app/streamlit_app.py` · **Status: pronto e validado no navegador.**

Painel único em Streamlit que roda os três módulos e monta o **alerta consolidado**.
Validação executada com dados reais:

| Modalidade | Resultado no painel |
|---|---|
| 🎙️ Áudio | 3 palavras-chave críticas |
| 🎥 Vídeo | 8 anomalias de movimento (do `resultado_pose.json` real) |
| 📈 Vitais | 44 anomalias (Isolation Forest ao vivo, com slider de sensibilidade) |
| 🚨 **Consolidado** | banner **"ATENÇÃO DA EQUIPE NECESSÁRIA"** listando os 3 motivos |

## 8. Stack técnica (reprodutibilidade)
Python 3.12 · pandas · numpy · **scikit-learn** (Isolation Forest) · **mediapipe**
(PoseLandmarker) · opencv · matplotlib · **streamlit**. Dependências em `requirements.txt`;
roda tanto no **Google Colab** quanto localmente.

## 9. Limitações e considerações éticas
- Dados **não reais** (vitais simulados, vídeo de banco livre, áudio fictício) — decisão
  consciente de privacidade.
- Regras de anomalia (faixas de ângulo, limiar de prescrição, `contamination`) são
  **heurísticas ajustáveis**, não validadas clinicamente.
- Áudio depende de serviço externo (Azure) ainda não integrado.

## 10. Status e próximos passos
| Item | Status |
|---|---|
| Vitais (anomalias) | ✅ pronto e testado (F1 0,989) |
| Vídeo (pose) | ✅ pronto, rodado no vídeo real (8 detecções) |
| Dashboard (integração) | ✅ pronto, 3 módulos com dados reais |
| Áudio (transcrição + sentimento) | 🟡 falta — depende do Azure |
| Relatório técnico (versão final) | 🟡 em preenchimento |
| Vídeo de demonstração | ⬜ etapa futura |
