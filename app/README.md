# 🖥️ Dashboard / Integração — Dia 5

Junta os três módulos num único fluxo e mostra um **alerta consolidado** para a equipe.

## Fluxo
`áudio → vídeo → anomalias em vitais → ALERTA CONSOLIDADO`

Cada módulo expõe uma função que retorna seus alertas em formato padrão; o app agrega tudo.

## Rodar (Streamlit)
```bash
pip install -r ../requirements.txt
streamlit run streamlit_app.py
```

O Streamlit ajuda muito na hora de gravar o vídeo de demonstração (Dias 6-7).
