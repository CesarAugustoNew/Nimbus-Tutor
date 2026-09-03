"""
Definição das tools do agente, no formato esperado pela Anthropic API
(tool use / function calling).
"""

TOOLS = [
    {
        "name": "search_study_material",
        "description": (
            "Busca conteúdo de estudo oficial sobre um tópico do AWS "
            "Cloud Practitioner. Use SEMPRE antes de explicar um conceito "
            "técnico da AWS, para basear a resposta em conteúdo real."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Termo ou conceito a buscar, ex: 'IAM', 'S3', 'responsabilidade compartilhada'.",
                },
                "domain": {
                    "type": "string",
                    "description": (
                        "Domínio da prova para filtrar (opcional). Um de: "
                        "'Cloud Concepts', 'Security and Compliance', "
                        "'Cloud Technology and Services', "
                        "'Billing, Pricing and Support'."
                    ),
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "generate_quiz",
        "description": (
            "Gera perguntas de múltipla escolha sobre um domínio/tópico "
            "específico para testar o conhecimento do usuário."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Tópico ou domínio sobre o qual gerar as perguntas.",
                },
                "num_questions": {
                    "type": "integer",
                    "description": "Quantidade de perguntas a gerar (padrão 3).",
                },
            },
            "required": ["topic"],
        },
    },
    {
        "name": "grade_quiz_answer",
        "description": (
            "Avalia a resposta do usuário para uma pergunta de quiz e "
            "retorna se está correta, com explicação."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "correct_answer": {"type": "string"},
                "user_answer": {"type": "string"},
            },
            "required": ["question", "correct_answer", "user_answer"],
        },
    },
    {
        "name": "save_progress",
        "description": (
            "Salva o progresso de estudo do usuário: tópico estudado e, "
            "se aplicável, resultado de quiz (acertos/total). Use isso ao "
            "final de cada tópico estudado ou quiz respondido."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "topic": {"type": "string"},
                "domain": {"type": "string"},
                "quiz_score": {
                    "type": "string",
                    "description": "Ex: '2/3'. Deixe vazio se não houve quiz.",
                },
            },
            "required": ["user_id", "topic"],
        },
    },
]
