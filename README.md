# 8IADT — Tech Challenge Fase 4

Sistema de **monitoramento multimodal de pacientes** que combina três fontes de dados
para gerar um **alerta consolidado** para a equipe de saúde:

| Modal | Entrada | Técnica | Pasta |
|-------|---------|---------|-------|
| 🎥 **Vídeo** | Exercício de fisioterapia | Estimativa de pose (MediaPipe / YOLOv8) → regra de ângulo anômalo | [`/video`](video) |
| 🎙️ **Áudio** | Relato do paciente | Azure Speech-to-Text → Text Analytics (sentimento + entidades) + palavras-chave críticas | [`/audio`](audio) |
| 📈 **Vitais** | Série temporal (HR, SpO₂, PA…) | Detecção de anomalias (Isolation Forest / z-score) | [`/anomaly`](anomaly) |

A integração final junta os três num **dashboard Streamlit** ([`/app`](app)).

> ⚠️ **Dados**: não usamos dados reais de pacientes (questões éticas/privacidade).
> Vitais são simulados, vídeo e áudio são gravados por nós ou de fontes livres.
> Ver [`data/README.md`](data/README.md).

## Estrutura

```
├── video/      # análise de pose frame-a-frame
├── audio/      # transcrição + análise de sentimento
├── anomaly/    # detecção de anomalias em vitais
├── app/        # dashboard Streamlit (integração)
├── data/       # dados de exemplo (vídeo, áudio, vitais)
│   └── vitals/ # vitais_simulados.csv + gerador
└── docs/       # relatório técnico
```

## Como rodar (Google Colab)

Não é preciso instalar nada localmente. Cada notebook em `video/`, `audio/` e
`anomaly/` abre no Colab e instala suas dependências na primeira célula.

Para rodar localmente (opcional), veja [`requirements.txt`](requirements.txt).

## Configuração do Azure

Copie `.env.example` para `.env` e preencha com as chaves dos recursos
**Azure AI Speech** e **Azure AI Language (Text Analytics)**. O `.env` está no
`.gitignore` — **nunca** faça commit das chaves.

## Entregáveis

- Repositório no GitHub
- Relatório técnico ([`docs/relatorio-tecnico.md`](docs/relatorio-tecnico.md))
- Vídeo de demonstração (YouTube/Vimeo não listado)
