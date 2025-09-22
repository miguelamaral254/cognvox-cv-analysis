# API de Análise de Talentos com IA

Este projeto é uma API RESTful construída com FastAPI para gerenciar vagas de emprego e analisar perfis de talentos (candidatos) utilizando um modelo de Inteligência Artificial para ranqueá-los com base em critérios customizáveis.

## Tecnologias Utilizadas
- **Backend:** FastAPI
- **Validação de Dados:** Pydantic
- **Inteligência Artificial:** Sentence-Transformersw
- **Banco de Dados:** PostgreSQL (com Psycopg2)
- **Servidor ASGI:** Uvicorn

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone <https://github.com/miguelamaral254/cognvox-cv-analysis.git>
    cd <cognvox-cv-analysis
>

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Certifique-se de ter um arquivo `requirements.txt` com FastAPI, Uvicorn, Pydantic, Sentence-Transformers, Psycopg2-binary, python-dotenv, etc.)*

3.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione as credenciais do seu banco de dados PostgreSQL.

    **Exemplo de `.env`:**
    ```env
    DB_HOST=localhost
    DB_NAME=sua_base_de_dados
    DB_USER=seu_usuario
    DB_PASS=sua_senha
    DB_PORT=5432
    ```

4.  **Execute a aplicação:**
    ```bash
    uvicorn app.main:app --reload
    ```
    A API estará disponível em `http://127.0.0.1:8000`.

---

## Documentação da IA

A inteligência artificial é o núcleo do sistema de análise e ranqueamento. Sua função é entender o significado semântico dos textos (como "Sobre mim" e "Experiência Profissional") em vez de apenas comparar palavras-chave.

### Modelo Utilizado
- **Nome:** `paraphrase-multilingual-MiniLM-L12-v2`
- **Biblioteca:** `Sentence-Transformers`

Este modelo foi escolhido por ser leve, multilíngue (entende português e outras línguas) e altamente eficaz em tarefas de **similaridade semântica**. Ele transforma textos em vetores numéricos de alta dimensão, conhecidos como **embeddings**.

### Funcionamento

O processo de IA ocorre em dois momentos principais:

1.  **Inscrição do Talento (Geração de Embedding):**
    - Quando um novo talento se inscreve para uma vaga, seus dados textuais (`sobre_mim`, `formacao`, `experiencia_profissional`) são concatenados em um único documento de texto.
    - O modelo de IA processa esse documento e o converte em um **vetor (embedding)**.
    - Esse embedding, que é uma representação numérica do perfil completo do candidato, é salvo no banco de dados junto com seus outros dados.

2.  **Análise da Vaga (Cálculo de Similaridade):**
    - Ao acionar a rota de análise de uma vaga, o sistema pega a descrição de cada critério definido na vaga (ex: "Experiência com FastAPI e Pydantic").
    - O modelo de IA transforma a descrição de cada critério em um embedding "alvo".
    - Em seguida, ele calcula a **Similaridade de Cosseno** entre o embedding de cada critério e o embedding do perfil de cada candidato.
    - O resultado é um score (de 0 a 1) que indica o quão "próximo" em significado o perfil do candidato está daquele critério específico.
    - O **score final** do candidato é uma soma ponderada dos scores de similaridade de todos os critérios, permitindo que certos requisitos tenham mais peso que outros.

---

## Documentação da API (Endpoints)

### Vagas e Análise

#### 1. Criar uma Nova Vaga
- **Endpoint:** `POST /vagas`
- **Descrição:** Cria uma nova vaga no sistema com critérios de análise customizados.
- **Payload (Corpo da Requisição):**
  ```json
  {
    "titulo_vaga": "Desenvolvedor Python Sênior",
    "criterios_de_analise": {
      "Experiencia_Backend": {
        "descricao": "Experiência sólida com desenvolvimento backend usando FastAPI, Pydantic e SQLAlchemy. Conhecimento em arquitetura de microsserviços.",
        "colunas": ["sobre_mim", "experiencia_formatada"],
        "peso": 0.6
      },
      "Cloud_e_DevOps": {
        "descricao": "Conhecimento em Docker, CI/CD com GitHub Actions e deploy em AWS.",
        "colunas": ["sobre_mim", "experiencia_formatada"],
        "peso": 0.4
      }
    },
    "top_x_candidatos": 5
  }


- **Exemplo de Resposta (201 Created):**
    ```json
    {
      "titulo_vaga": "Desenvolvedor Python Sênior",
      "criterios_de_analise": {
          "Experiencia_Backend": { "..."},
          "Cloud_e_DevOps": { "..."}
      },
      "top_x_candidatos": 5,
      "id": 1,
      "criado_em": "2025-08-19T20:30:00.123456",
      "finalizada_em": null
    }
    ```

#### 2\. Listar Vagas Abertas

  - **Endpoint:** `GET /vagas`
  - **Descrição:** Retorna uma lista com todas as vagas que ainda não foram finalizadas.
  - **Payload:** Nenhum.
  - **Exemplo de Resposta (200 OK):**
    ```json
    [
      {
        "id": 1,
        "titulo_vaga": "Desenvolvedor Python Sênior",
        "criado_em": "2025-08-19T20:30:00.123456",
        "finalizada_em": null
      }
    ]
    ```

#### 3\. Analisar Candidatos de uma Vaga

  - **Endpoint:** `POST /vagas/{vaga_id}/analisar`
  - **Descrição:** Inicia o processo de análise de IA para todos os candidatos inscritos na vaga especificada e retorna o ranking dos melhores.
  - **Payload:** Nenhum.
  - **Exemplo de Resposta (200 OK):**
    ```json
    {
      "titulo_vaga": "Desenvolvedor Python Sênior",
      "ranking": [
        {
          "id_talento": 101,
          "nome": "Ana Oliveira",
          "email": "ana.oliveira@example.com",
          "score_final": 85.75,
          "scores_por_criterio": {
            "Experiencia_Backend": 90.50,
            "Cloud_e_DevOps": 78.90
          }
        },
        {
          "id_talento": 105,
          "nome": "Carlos Souza",
          "email": "carlos.souza@example.com",
          "score_final": 79.20,
          "scores_por_criterio": {
            "Experiencia_Backend": 85.00,
            "Cloud_e_DevOps": 71.00
          }
        }
      ]
    }
    ```

*(Outras rotas de vagas como `GET /{vaga_id}`, `PUT /{vaga_id}` e `POST /{vaga_id}/finalizar` também estão disponíveis para gerenciamento completo.)*

### Talentos

#### 1\. Inscrever um Novo Talento

  - **Endpoint:** `POST /talentos`
  - **Descrição:** Cadastra um novo talento (candidato) e o associa a uma vaga.
  - **Payload (Corpo da Requisição):**
    ```json
    {
      "nome": "Ana Oliveira",
      "email": "ana.oliveira@example.com",
      "sobre_mim": "Sou uma desenvolvedora backend com mais de 5 anos de experiência, focada em criar APIs eficientes e escaláveis com FastAPI. Tenho grande interesse em soluções cloud e automação de processos com CI/CD.",
      "experiencia_profissional": [
        {
          "cargo": "Desenvolvedora Backend Sênior",
          "empresa": "Tech Solutions",
          "descricao": "Liderei o desenvolvimento de um sistema de microsserviços para pagamentos usando FastAPI e Docker. Automatizei o pipeline de deploy para a AWS com GitHub Actions."
        },
        {
          "cargo": "Desenvolvedora Pleno",
          "empresa": "Inova Web",
          "descricao": "Trabalhei na manutenção e criação de novas features para uma API monolítica em Django."
        }
      ],
      "formacao": "Mestrado em Ciência da Computação - UFPE",
      "aceita_termos": true,
      "vaga_id": 1
    }
    ```
  - **Exemplo de Resposta (201 Created):**
    ```json
    {
      "nome": "Ana Oliveira",
      "email": "ana.oliveira@example.com",
      "sobre_mim": "...",
      "experiencia_profissional": [
        { "..."},
        { "..."}
      ],
      "formacao": "Mestrado em Ciência da Computação - UFPE",
      "aceita_termos": true,
      "id": 101,
      "vaga_id": 1,
      "criado_em": "2025-08-19T20:35:00.543210"
    }
    ```

#### 2\. Listar todos os Talentos

  - **Endpoint:** `GET /talentos`
  - **Descrição:** Retorna uma lista simplificada de todos os talentos cadastrados no sistema.
  - **Payload:** Nenhum.
  - **Exemplo de Resposta (200 OK):**
    ```json
    [
      {
        "id": 101,
        "nome": "Ana Oliveira",
        "email": "ana.oliveira@example.com",
        "vaga_id": 1
      },
      {
        "id": 102,
        "nome": "Bruno Costa",
        "email": "bruno.costa@example.com",
        "vaga_id": 1
      }
    ]
    ```
