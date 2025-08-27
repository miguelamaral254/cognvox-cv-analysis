
-- Arquivo V2__populate_tables.sql

-- Inserindo dados na tabela 'areas'
INSERT INTO areas (nome, descricao) VALUES
('Tecnologia da Informação', 'Vagas relacionadas a desenvolvimento de software, infraestrutura, cibersegurança, etc.'),
('Recursos Humanos', 'Vagas para recrutamento, departamento pessoal, desenvolvimento organizacional e gestão de pessoas.'),
('Marketing e Vendas', 'Oportunidades para marketing digital, comunicação, vendas B2B/B2C e relacionamento com cliente.'),
('Psicologia', 'Vagas para psicólogos clínicos, organizacionais e outras especialidades da área.')
ON CONFLICT (nome) DO NOTHING;

-- Inserindo dados na tabela 'vagas'
INSERT INTO vagas (titulo_vaga, descricao, cidade, modelo_trabalho, area_id, criterios_de_analise) VALUES
('Desenvolvedor(a) Backend Pleno (Node.js)', 'Estamos à procura de um(a) Desenvolvedor(a) Backend Pleno para integrar nossa equipe em Recife. O candidato ideal deve ter experiência sólida na construção de APIs escaláveis utilizando Node.js e TypeScript.', 'Recife', 'Híbrido', 1,
'{
    "Experiencia_Tecnica": {"descricao": "Domínio em Node.js, TypeScript, SQL e Git.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.7},
    "Habilidades_DevOps": {"descricao": "Conhecimento em Docker, Kubernetes e AWS.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.3}
}'),
('Analista de Recrutamento e Seleção Sênior', 'Buscamos um(a) Analista de Recrutamento e Seleção Sênior para atuar presencialmente em nosso escritório de Recife, com foco em vagas de tecnologia.', 'Recife', 'Presencial', 2,
'{
    "Experiencia_Tecnica_RS": {"descricao": "Experiência comprovada em recrutamento e seleção para posições de tecnologia.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.7},
    "Idiomas_e_Ferramentas": {"descricao": "Inglês avançado e familiaridade com sistemas ATS.", "colunas": ["idiomas", "sobre_mim"], "peso": 0.3}
}'),
('Especialista em Marketing Digital', 'Procuramos um(a) Especialista em Marketing Digital para liderar e executar estratégias de crescimento online em nosso time de Jaboatão.', 'Jaboatão dos Guararapes', 'Presencial', 3,
'{
    "Estrategia_e_Execucao": {"descricao": "Experiência em marketing de conteúdo, SEO e Google Ads.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.8},
    "Analise_de_Dados": {"descricao": "Habilidade para analisar métricas e usar ferramentas de automação.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.2}
}'),
('Psicólogo(a) Clínico', 'Vaga para psicólogo(a) clínico com foco em terapia cognitivo-comportamental. Atuação 100% remota, atendendo pacientes de diversas localidades.', 'N/A', 'Remoto', 4,
'{
    "Formacao_Especializacao": {"descricao": "Pós-graduação ou especialização em Terapia Cognitivo-Comportamental (TCC).", "colunas": ["formacao", "sobre_mim"], "peso": 0.6},
    "Experiencia_Clinica": {"descricao": "Experiência mínima de 3 anos em atendimento clínico.", "colunas": ["experiencia_profissional"], "peso": 0.4}
}'),
('Desenvolvedor(a) Front-end Júnior', 'Oportunidade para desenvolvedor(a) front-end júnior atuar em modelo híbrido em nosso polo de Jaboatão, trabalhando com React e TypeScript.', 'Jaboatão dos Guararapes', 'Híbrido', 1,
'{
    "Conhecimento_Frontend": {"descricao": "Conhecimento em React, HTML5, CSS3 e TypeScript.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.9},
    "Versionamento_Codigo": {"descricao": "Experiência básica com Git.", "colunas": ["sobre_mim"], "peso": 0.1}
}');

-- CORREÇÃO: Inserindo talentos com o campo 'respostas_criterios' preenchido
INSERT INTO talentos (vaga_id, nome, email, cidade, telefone, sobre_mim, experiencia_profissional, formacao, idiomas, respostas_criterios, aceita_termos) VALUES
(1, 'Ana Silva', 'ana.silva@email.com', 'Recife', '+55 81 98765-4321', 'Desenvolvedora backend com foco em APIs RESTful e microserviços.', '[{"empresa": "Tech Solutions", "cargo": "Desenvolvedora Backend Jr", "periodo": "2020-2022"}]', '[{"instituicao": "UFPE", "curso": "Ciência da Computação", "periodo": "2016-2020"}]', '[{"idioma": "Inglês", "nivel": "Avançado"}]', 
'{"Experiencia_Tecnica": "Tenho 2 anos de experiência desenvolvendo APIs com Node.js e SQL.", "Habilidades_DevOps": "Não possuo o critério"}', true),
(1, 'Bruno Costa', 'bruno.costa@email.com', 'Recife', '+55 81 91234-5678', 'Apaixonado por tecnologia e soluções escaláveis na nuvem.', '[{"empresa": "Cloud Experts", "cargo": "Engenheiro DevOps", "periodo": "2021-Presente"}]', '[{"instituicao": "UPE", "curso": "Sistemas de Informação", "periodo": "2015-2019"}]', '[{"idioma": "Inglês", "nivel": "Fluente"}]', 
'{"Experiencia_Tecnica": "Tenho conhecimento básico em Node.js, mas meu forte é infraestrutura.", "Habilidades_DevOps": "Trabalho diariamente com Docker, Kubernetes e AWS há mais de 2 anos."}', true),
(2, 'Carla Dias', 'carla.dias@email.com', 'Jaboatão dos Guararapes', '+55 81 99988-7766', 'Recrutadora com experiência em fechar posições complexas de tecnologia.', '[{"empresa": "Talent Hub", "cargo": "Tech Recruiter Sênior", "periodo": "2021-Presente"}]', '[{"instituicao": "UNICAP", "curso": "Psicologia", "periodo": "2013-2018"}]', '[{"idioma": "Inglês", "nivel": "Avançado"}]', 
'{"Experiencia_Tecnica_RS": "Possuo 5 anos de experiência como Tech Recruiter.", "Idiomas_e_Ferramentas": "Tenho inglês avançado e já utilizei as plataformas Gupy e Greenhouse."}', true),
(4, 'Mariana Lima', 'mariana.lima@email.com', 'Cururipe', '+55 82 98877-1122', 'Psicóloga clínica dedicada ao bem-estar e saúde mental, com especialização em TCC.', '[]', '[{"instituicao": "UFAL", "curso": "Psicologia", "periodo": "2014-2019"}]', '[]', 
'{"Formacao_Especializacao": "Concluí minha pós-graduação em TCC no ano passado.", "Experiencia_Clinica": "Atuo em clínica há 4 anos."}', true),
(5, 'Lucas Pereira', 'lucas.pereira@email.com', 'Jaboatão dos Guararapes', '+55 81 98811-2233', 'Entusiasta de interfaces e experiência do usuário, buscando minha primeira oportunidade em front-end.', '[{"empresa": "Freelance", "cargo": "Web Designer", "periodo": "2023-Presente"}]', '[{"instituicao": "SENAC", "curso": "Análise e Desenv. de Sistemas", "periodo": "2022-2024"}]', '[{"idioma": "Inglês", "nivel": "Intermediário"}]', 
'{"Conhecimento_Frontend": "Desenvolvi diversos projetos pessoais e acadêmicos com React e TypeScript.", "Versionamento_Codigo": "Utilizo Git e GitHub em todos os meus projetos."}', true)
ON CONFLICT (email, vaga_id) DO NOTHING;

-- CORREÇÃO: Inserindo usuários com um HASH VÁLIDO para a senha 'password123'
INSERT INTO users (nome, email, hashed_password, role) VALUES
('Miguel Admin', 'miguel.admin@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 'admin'),
('Usuário Um', 'usuario.um@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 'user1'),
('Usuário Dois', 'usuario.dois@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 'user2')
ON CONFLICT (email) DO NOTHING;

-- Resetando a sequência dos IDs
SELECT setval('areas_id_seq', (SELECT MAX(id) FROM areas), true);
SELECT setval('vagas_id_seq', (SELECT MAX(id) FROM vagas), true);
SELECT setval('talentos_id_seq', (SELECT MAX(id) FROM talentos), true);