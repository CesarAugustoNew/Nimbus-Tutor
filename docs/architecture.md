# Arquitetura do agente

## Fluxo de uma mensagem

1. Usuário envia mensagem pelo frontend → `POST /chat`
2. `chat_service.send_message` recupera o histórico da conversa (em
   memória, por `user_id`) e chama `agent/client.run_agent`
3. `run_agent` chama a Claude API com: system prompt, histórico e a
   lista de **tools** disponíveis
4. Se o modelo decidir usar uma tool (ex: `search_study_material`),
   o backend executa a função Python correspondente
   (`tool_handlers.py`) e devolve o resultado ao modelo
5. O loop se repete até o modelo responder só com texto (sem mais tool
   calls) — essa resposta final volta para o usuário

Esse é o padrão clássico de **agentic tool use**: o modelo raciocina
sobre *quando* e *quais* ferramentas usar, em vez de o desenvolvedor
decidir isso via regras fixas de código.

## Tools disponíveis

| Tool | O que faz | Quando o agente usa |
|---|---|---|
| `search_study_material` | Busca conteúdo relevante na base de estudo (retriever por keyword) | Antes de explicar qualquer conceito técnico de AWS |
| `generate_quiz` | Traz contexto de referência para o modelo formular perguntas | Quando o usuário pede para ser testado |
| `grade_quiz_answer` | Compara resposta do usuário com o gabarito | Depois que o usuário responde uma pergunta do quiz |
| `save_progress` | Persiste no SQLite o que foi estudado / resultado do quiz | Ao final de um tópico ou quiz |

## Por que "RAG simplificado"

Em vez de embeddings + vector DB desde o início, o `retriever.py`
faz busca por interseção de palavras-chave sobre uma base de conteúdo
curada localmente (`data/study_content.py`), organizada pelos 4
domínios oficiais do exame CLF-C02.

A interface pública (`retrieve(query, domain, top_k)`) é a mesma que
seria usada com um vector store real — então é possível evoluir para
Chroma/FAISS + embeddings sem alterar o restante do agente, apenas o
retriever.

## Por que tool use em vez de só prompt engineering

Sem tools, o modelo poderia "alucinar" conteúdo de prova ou perder o
controle de estado (o que já foi estudado, o placar do quiz). Com
tools, o comportamento fica auditável: cada ação relevante (buscar
conteúdo, salvar progresso) é uma chamada de função rastreável no
backend, não apenas texto livre gerado pelo modelo.
