# 🎥 Vídeo — Dia 3

Analisar o movimento do paciente e sinalizar posturas anômalas.

## Pipeline
1. **Estimativa de pose frame-a-frame** com **MediaPipe Pose** (recomendado; mais simples)
   ou **YOLOv8-pose** (`ultralytics`).
2. **Regra de anomalia simples** — ex: ângulo de uma articulação (cotovelo/joelho)
   fora de uma faixa esperada por **X frames seguidos**.
3. **Relatório** — `.txt`/`.pdf` (ou print) com os **timestamps** das anomalias detectadas.

## Cálculo de ângulo (referência)
Ângulo em B formado por três pontos A–B–C:
`ang = atan2(Cy-By, Cx-Bx) - atan2(Ay-By, Ax-Bx)` (normalizar para 0–180°).

## Saída esperada
Lista de `{timestamp, articulacao, angulo, descricao}` das anomalias — consumida no Dia 5.
