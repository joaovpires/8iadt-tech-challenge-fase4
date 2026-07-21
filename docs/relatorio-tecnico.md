# Relatório Técnico — Tech Challenge Fase 4

> Esqueleto — preencher ao longo do desenvolvimento.

## 1. Visão geral
Sistema multimodal de monitoramento de pacientes que integra vídeo, áudio e sinais
vitais para gerar um alerta consolidado à equipe de saúde.

## 2. Arquitetura / fluxo multimodal
_(Diagrama: áudio → vídeo → vitais → alerta consolidado. Descrever a integração dos módulos.)_

## 3. Módulos

### 3.1 Áudio
- Modelo/serviço: Azure Speech-to-Text + Azure AI Language.
- O que detecta: sentimento, entidades, palavras-chave críticas.
- Exemplos de saída / anomalias detectadas: _(preencher)_

### 3.2 Vídeo
- Modelo: MediaPipe Pose / YOLOv8-pose.
- Regra de anomalia: _(preencher — ex: ângulo do joelho > X° por Y frames)._
- Exemplos com timestamps: _(preencher)_

### 3.3 Anomalias em vitais
- Método: Isolation Forest / z-score.
- Regra de evolução de prescrição: _(preencher)_
- Avaliação contra `anomalia_esperada`: _(preencher — precisão/recall)._

## 4. Integração
Como os três resultados são combinados no dashboard e como o alerta consolidado é formado.

## 5. Limitações e considerações éticas
- Dados não reais (simulados/gravados) por privacidade — decisão consciente.
- _(outras limitações)_

## 6. Como reproduzir
Passos para rodar cada notebook no Colab e o dashboard Streamlit.

## 7. Links
- Repositório: https://github.com/joaovpires/8iadt-tech-challenge-fase4
- Vídeo de demonstração: _(link YouTube/Vimeo não listado)_
