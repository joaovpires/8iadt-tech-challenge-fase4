# 📈 Anomalias em vitais — Dia 4

Detectar leituras fora do padrão na série temporal de sinais vitais.

## Dados
`data/vitals/vitais_simulados.csv` (720 leituras, com `anomalia_esperada` como ground truth).

## Pipeline
1. Carregar a série (pandas).
2. Detectar anomalias com **Isolation Forest** (scikit-learn) **ou z-score** simples.
   - Comparar as anomalias detectadas contra a coluna `anomalia_esperada` (precisão/recall).
3. **Regra de evolução de prescrição** — se a dosagem mudar mais que **X%** de uma
   consulta para outra, dispara alerta (usar um CSV de prescrições fictício).

## Saída esperada
Lista de `{timestamp, sinal, valor, score}` das anomalias + alertas de prescrição — consumida no Dia 5.
