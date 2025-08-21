-- Inserindo dados na tabela 'areas', ignorando duplicados pelo nome
INSERT INTO areas (nome, descricao) VALUES
('Tecnologia da Informação', 'Vagas relacionadas a desenvolvimento de software, infraestrutura, cibersegurança, etc.'),
('Recursos Humanos', 'Vagas para recrutamento, departamento pessoal, desenvolvimento organizacional e gestão de pessoas.'),
('Marketing e Vendas', 'Oportunidades para marketing digital, comunicação, vendas B2B/B2C e relacionamento com cliente.'),
('Psicologia', 'Vagas para psicólogos clínicos, organizacionais e outras especialidades da área.')
ON CONFLICT (nome) DO NOTHING;

-- Inserindo dados na tabela 'vagas'
-- NOTA: Para tornar esta parte idempotente, seria necessário adicionar uma constraint UNIQUE
-- em uma combinação de colunas (ex: titulo_vaga e area_id). Por enquanto, focamos em resolver o erro.
INSERT INTO vagas (titulo_vaga, area_id, criterios_de_analise) VALUES
('Desenvolvedor(a) Backend Pleno (Node.js)', 1, '{
    "requisitos_obrigatorios": ["Node.js", "TypeScript", "SQL", "Git"],
    "requisitos_desejaveis": ["Docker", "Kubernetes", "AWS"],
    "anos_de_experiencia": 3
}'),
('Analista de Recrutamento e Seleção Sênior', 2, '{
    "requisitos_obrigatorios": ["Experiência com vagas de tecnologia", "Entrevistas por competências"],
    "requisitos_desejaveis": ["Inglês avançado", "Conhecimento em ATS"],
    "anos_de_experiencia": 5
}'),
('Especialista em Marketing Digital', 3, '{
    "requisitos_obrigatorios": ["Google Ads", "SEO", "Marketing de Conteúdo"],
    "requisitos_desejaveis": ["Ferramentas de automação", "Análise de métricas"],
    "anos_de_experiencia": 4
}')
ON CONFLICT (id) DO NOTHING; -- Adicionado para evitar erro se os IDs já existirem

-- Inserindo dados na tabela 'talentos', ignorando duplicados pela chave (email, vaga_id)
INSERT INTO talentos (vaga_id, nome, email, telefone, sobre_mim, experiencia_profissional, formacao, idiomas, aceita_termos) VALUES
(1, 'Ana Silva', 'ana.silva@email.com', '+55 11 98765-4321', 'Desenvolvedora backend com foco em APIs RESTful e microserviços.', '[
    {"empresa": "Tech Solutions", "cargo": "Desenvolvedora Backend Jr", "periodo": "2020-2022"},
    {"empresa": "Inova Code", "cargo": "Desenvolvedora Backend Pl", "periodo": "2022-Presente"}
]', '[
    {"instituicao": "Universidade X", "curso": "Ciência da Computação", "periodo": "2016-2020"}
]', '[
    {"idioma": "Inglês", "nivel": "Avançado"},
    {"idioma": "Espanhol", "nivel": "Básico"}
]', true),
(1, 'Bruno Costa', 'bruno.costa@email.com', '+55 21 91234-5678', 'Apaixonado por tecnologia e soluções escaláveis na nuvem.', '[
    {"empresa": "Cloud Experts", "cargo": "Analista de Infraestrutura", "periodo": "2019-2021"},
    {"empresa": "Web Services Inc.", "cargo": "Engenheiro DevOps", "periodo": "2021-Presente"}
]', '[
    {"instituicao": "Faculdade Y", "curso": "Sistemas de Informação", "periodo": "2015-2019"}
]', '[
    {"idioma": "Inglês", "nivel": "Fluente"}
]', true),
(2, 'Carla Dias', 'carla.dias@email.com', '+55 31 99988-7766', 'Recrutadora com experiência em fechar posições complexas de tecnologia.', '[
    {"empresa": "RH Tech", "cargo": "Analista de R&S", "periodo": "2018-2021"},
    {"empresa": "Talent Hub", "cargo": "Tech Recruiter Sênior", "periodo": "2021-Presente"}
]', '[
    {"instituicao": "Universidade Z", "curso": "Psicologia", "periodo": "2013-2018"}
]', '[
    {"idioma": "Inglês", "nivel": "Avançado"}
]', true)
ON CONFLICT (email, vaga_id) DO NOTHING;

-- Resetando a sequência dos IDs para evitar conflitos em futuras inserções manuais
-- Esta parte pode causar problemas se executada repetidamente sem controle, mas é mantida por enquanto.
-- Em um ambiente de produção, o gerenciamento de migrações seria mais robusto.
SELECT setval('areas_id_seq', (SELECT MAX(id) FROM areas), true);
SELECT setval('vagas_id_seq', (SELECT MAX(id) FROM vagas), true);
SELECT setval('talentos_id_seq', (SELECT MAX(id) FROM talentos), true);
