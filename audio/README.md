# 🎙️ Áudio

Transcrever o relato do paciente e extrair sinais de risco.

## Pipeline
1. **Azure Speech-to-Text** — transcreve `data/audio/*.wav` para texto.
2. **Azure AI Language (Text Analytics)** — sobre o texto transcrito:
   - análise de **sentimento** (positivo/neutro/negativo);
   - **key phrases** e **entidades** (ex: sintomas, partes do corpo).
3. **Palavras-chave críticas** — lista simples (ex: `"dor no peito"`, `"falta de ar"`,
   `"tontura"`, `"desmaio"`) que dispara um **ALERTA** se aparecer na transcrição.

## Saída esperada
Um dict/JSON com: `transcricao`, `sentimento`, `key_phrases`, `entidades`,
`alertas_criticos` (lista) — consumido pelo dashboard de integração.

## Config
Chaves em `.env` (`AZURE_SPEECH_KEY`, `AZURE_LANGUAGE_KEY`, ...). Ver `.env.example`.
