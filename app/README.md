# 🖥️ Dashboard / Integração

Junta os três módulos num único fluxo e mostra um **alerta consolidado** para a equipe.

## Fluxo
`áudio → vídeo → anomalias em vitais → ALERTA CONSOLIDADO`

Cada módulo expõe uma função que retorna seus alertas em formato padrão; o app agrega tudo.

## Estado atual
- **Vitais** — funcional (Isolation Forest sobre `data/vitals/vitais_simulados.csv`).
- **Áudio** — detecção de palavras-chave críticas funcional (edite a transcrição na tela);
  transcrição automática + sentimento ficam como *stub* até o Azure.
- **Vídeo** — consome `data/video/resultado_pose.json` se existir; senão mostra um exemplo.

## Rodar (Streamlit)
```bash
pip install -r ../requirements.txt
streamlit run streamlit_app.py
```

No Windows, usando o venv do projeto:
```powershell
..\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

O Streamlit ajuda muito na hora de gravar o vídeo de demonstração.
