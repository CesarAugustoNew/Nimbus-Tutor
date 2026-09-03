"""
Base de conhecimento do AWS Certified Cloud Practitioner (CLF-C02).

Organizada pelos 4 domínios oficiais da prova, com peso aproximado
conforme o exam guide da AWS:
- Cloud Concepts (24%)
- Security and Compliance (30%)
- Cloud Technology and Services (34%)
- Billing, Pricing and Support (12%)

Cada tópico é um "chunk" pequeno, o suficiente para o agente
usar como contexto ao responder ou gerar perguntas de quiz.

Isso funciona como uma versão simplificada de RAG: em vez de
embeddings + vector DB, fazemos busca por palavras-chave. Pode ser
evoluído para ChromaDB/FAISS sem mudar a interface do retriever.
"""

STUDY_CONTENT = [
    {
        "id": "concepts-01",
        "domain": "Cloud Concepts",
        "topic": "O que é computação em nuvem",
        "keywords": ["cloud", "nuvem", "computacao", "definicao", "on-premises"],
        "content": (
            "Computação em nuvem é a entrega sob demanda de recursos de TI "
            "(servidores, armazenamento, banco de dados, rede) pela internet, "
            "com pagamento conforme o uso. Em vez de comprar e manter data "
            "centers físicos (on-premises), a empresa aluga capacidade da AWS "
            "e paga apenas pelo que consome."
        ),
    },
    {
        "id": "concepts-02",
        "domain": "Cloud Concepts",
        "topic": "Os 6 benefícios da nuvem",
        "keywords": ["beneficios", "vantagens", "elasticidade", "capex", "opex"],
        "content": (
            "Os 6 benefícios da AWS Cloud: 1) Trocar CAPEX por OPEX (pagar "
            "conforme o uso, sem investimento inicial pesado); 2) Economia de "
            "escala (custos menores por causa do volume da AWS); 3) Parar de "
            "adivinhar capacidade (escalar conforme a demanda real); 4) Ganhar "
            "velocidade e agilidade; 5) Parar de gastar com manutenção de "
            "data center; 6) Ir global em minutos."
        ),
    },
    {
        "id": "concepts-03",
        "domain": "Cloud Concepts",
        "topic": "Modelos de implantação (deployment models)",
        "keywords": ["deployment", "hibrido", "hybrid", "publica", "privada"],
        "content": (
            "Existem 3 modelos de implantação: Cloud pública (recursos totalmente "
            "na AWS), On-premises/privada (infraestrutura própria) e Híbrida "
            "(combinação dos dois, comum em migrações graduais)."
        ),
    },
    {
        "id": "concepts-04",
        "domain": "Cloud Concepts",
        "topic": "Well-Architected Framework",
        "keywords": ["well-architected", "pilares", "framework"],
        "content": (
            "O AWS Well-Architected Framework tem 6 pilares: Excelência "
            "Operacional, Segurança, Confiabilidade, Eficiência de Performance, "
            "Otimização de Custos e Sustentabilidade. Ele ajuda a avaliar "
            "arquiteturas contra boas práticas."
        ),
    },
    {
        "id": "security-01",
        "domain": "Security and Compliance",
        "topic": "Modelo de responsabilidade compartilhada",
        "keywords": ["responsabilidade", "shared responsibility", "seguranca da nuvem", "seguranca na nuvem"],
        "content": (
            "No modelo de Responsabilidade Compartilhada, a AWS é responsável "
            "pela 'segurança DA nuvem' (hardware, infraestrutura global, "
            "virtualização). O cliente é responsável pela 'segurança NA "
            "nuvem' (configuração de dados, IAM, sistema operacional em EC2, "
            "firewalls/security groups, criptografia)."
        ),
    },
    {
        "id": "security-02",
        "domain": "Security and Compliance",
        "topic": "IAM (Identity and Access Management)",
        "keywords": ["iam", "usuarios", "roles", "politicas", "permissoes", "mfa"],
        "content": (
            "IAM gerencia usuários, grupos, papéis (roles) e políticas de "
            "permissão na AWS. Boas práticas: nunca usar a conta root no dia a "
            "dia, habilitar MFA, seguir o princípio do menor privilégio e usar "
            "roles em vez de compartilhar credenciais."
        ),
    },
    {
        "id": "security-03",
        "domain": "Security and Compliance",
        "topic": "Serviços de segurança",
        "keywords": ["guardduty", "shield", "waf", "inspector", "macie"],
        "content": (
            "Principais serviços de segurança: AWS Shield (proteção contra "
            "DDoS), AWS WAF (firewall de aplicação web), Amazon GuardDuty "
            "(detecção de ameaças com machine learning), Amazon Inspector "
            "(avaliação automática de vulnerabilidades) e Amazon Macie "
            "(descoberta de dados sensíveis)."
        ),
    },
    {
        "id": "tech-01",
        "domain": "Cloud Technology and Services",
        "topic": "EC2 (compute)",
        "keywords": ["ec2", "instancias", "compute", "servidores virtuais"],
        "content": (
            "Amazon EC2 (Elastic Compute Cloud) fornece servidores virtuais "
            "(instâncias) sob demanda. Você escolhe tipo de instância, "
            "sistema operacional e paga por hora/segundo de uso. Modelos de "
            "compra: On-Demand, Reserved Instances, Spot Instances e Savings Plans."
        ),
    },
    {
        "id": "tech-02",
        "domain": "Cloud Technology and Services",
        "topic": "S3 (armazenamento de objetos)",
        "keywords": ["s3", "armazenamento", "storage", "buckets", "objetos"],
        "content": (
            "Amazon S3 é armazenamento de objetos altamente durável (11 noves "
            "de durabilidade). Dados ficam em 'buckets'. Classes de "
            "armazenamento incluem S3 Standard, S3 Intelligent-Tiering, "
            "S3 Glacier (arquivamento de baixo custo) para diferentes padrões "
            "de acesso."
        ),
    },
    {
        "id": "tech-03",
        "domain": "Cloud Technology and Services",
        "topic": "Redes: VPC",
        "keywords": ["vpc", "rede", "subnet", "networking"],
        "content": (
            "Amazon VPC (Virtual Private Cloud) permite criar uma rede "
            "isolada logicamente dentro da AWS, com subnets públicas e "
            "privadas, tabelas de rota, gateways de internet e NAT gateways "
            "para controlar o tráfego de entrada e saída."
        ),
    },
    {
        "id": "tech-04",
        "domain": "Cloud Technology and Services",
        "topic": "Bancos de dados gerenciados",
        "keywords": ["rds", "dynamodb", "banco de dados", "database"],
        "content": (
            "Amazon RDS é um banco de dados relacional gerenciado (MySQL, "
            "PostgreSQL, etc.), cuidando de backups, patches e replicação. "
            "Amazon DynamoDB é um banco NoSQL totalmente gerenciado, "
            "de altíssima performance e escala automática."
        ),
    },
    {
        "id": "tech-05",
        "domain": "Cloud Technology and Services",
        "topic": "Elasticidade e Load Balancing",
        "keywords": ["auto scaling", "elastic load balancing", "elb", "escalabilidade"],
        "content": (
            "Elastic Load Balancing (ELB) distribui tráfego entre múltiplas "
            "instâncias. Auto Scaling ajusta automaticamente o número de "
            "instâncias conforme a demanda, garantindo disponibilidade e "
            "controle de custo."
        ),
    },
    {
        "id": "tech-06",
        "domain": "Cloud Technology and Services",
        "topic": "Regiões, Zonas de Disponibilidade e Edge Locations",
        "keywords": ["regioes", "regions", "availability zone", "az", "edge locations", "cloudfront"],
        "content": (
            "A infraestrutura global da AWS é dividida em Regiões (áreas "
            "geográficas), cada Região com múltiplas Zonas de Disponibilidade "
            "(AZs, data centers isolados fisicamente) para alta "
            "disponibilidade. Edge Locations são usadas pelo CloudFront (CDN) "
            "para entregar conteúdo com baixa latência."
        ),
    },
    {
        "id": "billing-01",
        "domain": "Billing, Pricing and Support",
        "topic": "Modelos de precificação",
        "keywords": ["precos", "pricing", "pague pelo uso", "pay as you go"],
        "content": (
            "A AWS usa o modelo pague-pelo-uso (pay-as-you-go): sem custo "
            "inicial, sem compromisso de longo prazo (exceto se optar por "
            "Reserved/Savings Plans para desconto). Existem calculadoras "
            "oficiais (AWS Pricing Calculator) para estimar custos."
        ),
    },
    {
        "id": "billing-02",
        "domain": "Billing, Pricing and Support",
        "topic": "Planos de suporte",
        "keywords": ["suporte", "support plans", "basic", "developer", "business", "enterprise"],
        "content": (
            "Planos de suporte da AWS: Basic (grátis, só documentação e "
            "fóruns), Developer, Business e Enterprise. Os planos pagos "
            "incluem acesso a engenheiros de suporte, tempos de resposta "
            "garantidos e, no Enterprise, um Technical Account Manager (TAM)."
        ),
    },
    {
        "id": "billing-03",
        "domain": "Billing, Pricing and Support",
        "topic": "AWS Organizations e Consolidated Billing",
        "keywords": ["organizations", "consolidated billing", "multiplas contas", "contas"],
        "content": (
            "AWS Organizations permite gerenciar múltiplas contas AWS "
            "centralizadamente, com Consolidated Billing (fatura única, "
            "descontos por volume agregados) e Service Control Policies (SCPs) "
            "para aplicar restrições em toda a organização."
        ),
    },
    {
        "id": "billing-04",
        "domain": "Billing, Pricing and Support",
        "topic": "Ferramentas de controle de custo",
        "keywords": ["cost explorer", "budgets", "trusted advisor", "custos"],
        "content": (
            "AWS Cost Explorer visualiza e analisa padrões de gasto. AWS "
            "Budgets permite definir alertas de orçamento. AWS Trusted "
            "Advisor dá recomendações automatizadas de custo, performance, "
            "segurança e limites de serviço."
        ),
    },
]


def get_all_domains():
    """Retorna a lista única de domínios da prova."""
    return sorted({item["domain"] for item in STUDY_CONTENT})
