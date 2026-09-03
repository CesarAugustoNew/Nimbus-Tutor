# CCP Tutor Agent

Agente de IA que conversa com você para estudar para a certificação **AWS
Certified Cloud Practitioner (CLF-C02)**: explica conceitos, gera quizzes,
corrige suas respostas e acompanha seu progresso por domínio da prova.

Construído com **Claude (Anthropic API) usando tool use / function calling**,
não apenas um wrapper de chat — o agente decide quando buscar conteúdo,
quando gerar perguntas e quando salvar progresso.

## Por que esse projeto

Feito para demonstrar, de forma enxuta:
- Arquitetura de **agentes de IA** (tool use, não só prompt→resposta)
- Um pipeline de **RAG simplificado** (retrieval de conteúdo antes de responder)
- Backend em camadas (rotas → serviços → agente/dados)
- Persistência de estado (progresso do usuário em SQLite)
- Frontend funcional sem dependências de build

## Arquitetura

```
Usuário → Frontend (HTML/JS) → FastAPI (/chat)
                                   │
                                   ▼
                        Agente (loop de tool use)
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                     ▼
     search_study_material   generate_quiz         save_progress
     (retriever/keyword)     grade_quiz_answer      (SQLite)
```

Veja o fluxo completo em [`docs/architecture.md`](docs/architecture.md).

## Tecnologias

**Backend:** Python, FastAPI, Anthropic SDK (Claude Haiku), SQLAlchemy + SQLite, Pydantic
**Frontend:** HTML/CSS/JS puro (sem build step, roda abrindo o arquivo)
**Padrão de agente:** tool use / function calling com loop de execução

## Como rodar

### 1. Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp ../.env.example ../.env
# edite o .env e cole sua ANTHROPIC_API_KEY
# (crie uma conta gratuita em platform.claude.com — novos usuários
#  recebem um crédito inicial de teste)

uvicorn main:app --reload
```

O backend sobe em `http://127.0.0.1:8000`. Documentação interativa (Swagger)
automática em `http://127.0.0.1:8000/docs`.

### 2. Frontend

Basta abrir `frontend/index.html` no navegador (não precisa de servidor
nem build). Se o backend estiver em outra porta/host, ajuste a constante
`API_URL` no topo do `<script>`.

## Estrutura de pastas

```
backend/
  main.py                  # entrypoint FastAPI
  app/
    agent/                 # o "cérebro": prompt, tools, loop de execução
    rag/                   # retriever de conteúdo de estudo
    data/                  # base de conteúdo AWS CCP (por domínio da prova)
    db/                    # modelos e sessão SQLite
    services/               # lógica de negócio usada pelas rotas
    api/                   # rotas HTTP (/chat, /progress)
    models/                # schemas Pydantic
  tests/
frontend/
  index.html                # chat + seleção de domínios da prova
docs/
  architecture.md
```

