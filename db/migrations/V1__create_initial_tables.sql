CREATE TABLE IF NOT EXISTS areas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
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
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    finalizada_em TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS talentos (
    id SERIAL PRIMARY KEY,
    vaga_id INTEGER NOT NULL REFERENCES vagas(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cidade VARCHAR(100),
    telefone VARCHAR(20),
    sobre_mim TEXT,
    experiencia_profissional JSONB,
    formacao JSONB,
    idiomas JSONB,
    respostas_criterios JSONB,
    aceita_termos BOOLEAN NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    embedding TEXT,
    UNIQUE (email, vaga_id)
);

CREATE TABLE IF NOT EXISTS top_aplicantes (
    id SERIAL PRIMARY KEY,
    vaga_id INTEGER NOT NULL REFERENCES vagas(id) ON DELETE CASCADE,
    talento_id INTEGER NOT NULL REFERENCES talentos(id) ON DELETE CASCADE,
    score_final FLOAT NOT NULL,
    scores_por_criterio JSONB NOT NULL,
    analisado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);