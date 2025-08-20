-- Tabela para armazenar as informações das Vagas
CREATE TABLE IF NOT EXISTS vagas (
    id SERIAL PRIMARY KEY,
    titulo_vaga VARCHAR(255) NOT NULL,
    criterios_de_analise JSONB NOT NULL,
    top_x_candidatos INTEGER NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    finalizada_em TIMESTAMP WITH TIME ZONE
);

-- Tabela para armazenar os dados dos Talentos (candidatos)
CREATE TABLE IF NOT EXISTS talentos (
    id SERIAL PRIMARY KEY,
    vaga_id INTEGER NOT NULL REFERENCES vagas(id) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    sobre_mim TEXT,
    experiencia_profissional JSONB,
    formacao TEXT,
    aceita_termos BOOLEAN NOT NULL,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    embedding TEXT,
    UNIQUE (email, vaga_id)
);

-- Tabela para armazenar o resultado do ranking após uma análise
CREATE TABLE IF NOT EXISTS top_aplicantes (
    id SERIAL PRIMARY KEY,
    vaga_id INTEGER NOT NULL REFERENCES vagas(id) ON DELETE CASCADE,
    talento_id INTEGER NOT NULL REFERENCES talentos(id) ON DELETE CASCADE,
    score_final FLOAT NOT NULL,
    scores_por_criterio JSONB NOT NULL,
    analisado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);