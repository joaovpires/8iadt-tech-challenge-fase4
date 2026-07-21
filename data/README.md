# Dados de exemplo

> **Limitação assumida e aceita:** não usamos dados reais de pacientes por questões
> éticas e de privacidade. Todos os dados aqui são simulados ou gravados por nós.
> Deixar isso explícito no relatório técnico.

## `vitals/` — sinais vitais simulados

- **`vitais_simulados.csv`** — 720 leituras (1/min ≈ 12h) de um paciente, com colunas:
  `timestamp, heart_rate, spo2, systolic_bp, diastolic_bp, temperature, resp_rate, anomalia_esperada`.
- A coluna `anomalia_esperada` (0/1) marca as janelas anômalas injetadas de propósito
  (taquicardia, hipóxia, hipertensão) — serve de *ground truth* para avaliar a detecção de anomalias.
- **`gerar_vitais.js`** — script Node que regenera o CSV: `node gerar_vitais.js`.
  (Alternativa: também dá pra usar bases do PhysioNet, ex. MIT-BIH.)

## `video/` — vídeo de fisioterapia

Coloque aqui **um vídeo curto** (ex: agachamento ou elevação de braço), gravado por
você ou baixado com licença livre. Sugestão: 10–30 s, bem iluminado, corpo inteiro visível.
Arquivos `.mp4/.mov` são ignorados pelo git (ver `.gitignore`) — versione só se for amostra pequena.

## `audio/` — relato do paciente

Coloque aqui **um áudio curto** com um "script de paciente" fictício (leia você mesmo
ou gere por texto-para-fala). Inclua de propósito alguma frase crítica
(ex: *"estou com dor no peito e falta de ar"*) para testar o alerta da análise de áudio.
Arquivos de áudio são ignorados pelo git por padrão.
