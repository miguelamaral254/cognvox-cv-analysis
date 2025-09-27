-- Arquivo V1__create_initial_tables.sql
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) COLLATE utf8mb4_general_ci NOT NULL UNIQUE,
    descricao TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vagas (
    id SERIAL PRIMARY KEY,
    titulo_vaga VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    modelo_trabalho VARCHAR(20) NOT NULL CHECK (modelo_trabalho IN ('Remoto', 'Híbrido', 'Presencial')),
    area_id INTEGER NOT NULL REFERENCES areas(id) ON DELETE RESTRICT,
    criterios_de_analise JSONB NOT NULL,
    vaga_pcd BOOLEAN NOT NULL DEFAULT FALSE,
    criterios_diferenciais_de_analise JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    finalizada_em TIMESTAMP WITH TIME ZONE
);

CREATE TYPE user_role AS ENUM ('admin', 'user1', 'user2');

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    img_path VARCHAR(255),
    role user_role NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS talentos (
    id SERIAL PRIMARY KEY,
    vaga_id INTEGER NOT NULL REFERENCES vagas(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cidade VARCHAR(100),
    cep VARCHAR(10),
    rua VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    telefone VARCHAR(20),
    sobre_mim TEXT,
    experiencia_profissional JSONB,
    formacao JSONB,
    idiomas JSONB,
    respostas_criterios JSONB,
    respostas_diferenciais JSONB,
    redes_sociais JSONB,
    cursos_extracurriculares JSONB,
    deficiencia BOOLEAN NOT NULL DEFAULT FALSE,
    deficiencia_detalhes JSONB,
    aceita_termos BOOLEAN NOT NULL,
    confirmar_dados_verdadeiros BOOLEAN NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    embedding TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (email, vaga_id)
);

CREATE TABLE IF NOT EXISTS comentarios_talentos (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    talento_id INTEGER NOT NULL REFERENCES talentos(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS top_aplicantes (
    id SERIAL PRIMARY KEY,
    vaga_id INTEGER NOT NULL REFERENCES vagas(id) ON DELETE CASCADE,
    talento_id INTEGER NOT NULL REFERENCES talentos(id) ON DELETE CASCADE,
    score_final FLOAT NOT NULL,
    scores_por_criterio JSONB NOT NULL,
    analisado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(255) PRIMARY KEY
);