-- V2__populate_tables.sql

INSERT INTO areas (nome, descricao) VALUES
('Tecnologia da Informação', 'Vagas relacionadas a desenvolvimento de software, infraestrutura, cibersegurança, etc.'),
('Recursos Humanos', 'Vagas para recrutamento, departamento pessoal, desenvolvimento organizacional e gestão de pessoas.'),
('Marketing e Vendas', 'Oportunidades para marketing digital, comunicação, vendas B2B/B2C e relacionamento com cliente.'),
('Psicologia', 'Vagas para psicólogos clínicos, organizacionais e outras especialidades da área.')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO vagas (titulo_vaga, descricao, cidade, modelo_trabalho, area_id, criterios_de_analise, vaga_pcd, criterios_diferenciais_de_analise) VALUES
('Desenvolvedor(a) Backend Pleno (Node.js)', 'Estamos à procura de um(a) Desenvolvedor(a) Backend Pleno para integrar nossa equipe em Recife. O candidato ideal deve ter experiência sólida na construção de APIs escaláveis utilizando Node.js e TypeScript.', 'Recife', 'Híbrido', 1,
'{
    "Experiencia_Tecnica": {"descricao": "Domínio em Node.js, TypeScript, SQL e Git.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.7},
    "Habilidades_DevOps": {"descricao": "Conhecimento em Docker, Kubernetes e AWS.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.3}
}', false, 
'{
    "Certificacao_Cloud": {"descricao": "Possuir certificações em nuvem (AWS, Azure, GCP) será um grande diferencial.", "colunas": ["cursos_extracurriculares"], "peso": 0.2}
}'),
('Analista de Recrutamento e Seleção Sênior', 'Buscamos um(a) Analista de Recrutamento e Seleção Sênior para atuar presencialmente em nosso escritório de Recife, com foco em vagas de tecnologia.', 'Recife', 'Presencial', 2,
'{
    "Experiencia_Tecnica_RS": {"descricao": "Experiência comprovada em recrutamento e seleção para posições de tecnologia.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.7},
    "Idiomas_e_Ferramentas": {"descricao": "Inglês avançado e familiaridade com sistemas ATS.", "colunas": ["idiomas", "sobre_mim"], "peso": 0.3}
}', false, null),
('Especialista em Marketing Digital', 'Procuramos um(a) Especialista em Marketing Digital para liderar e executar estratégias de crescimento online em nosso time de Jaboatão.', 'Jaboatão dos Guararapes', 'Presencial', 3,
'{
    "Estrategia_e_Execucao": {"descricao": "Experiência em marketing de conteúdo, SEO e Google Ads.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.8},
    "Analise_de_Dados": {"descricao": "Habilidade para analisar métricas e usar ferramentas de automação.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.2}
}', false, 
'{
    "Edicao_de_Video": {"descricao": "Conhecimento em Adobe Premiere ou Final Cut será um diferencial.", "colunas": ["cursos_extracurriculares", "sobre_mim"], "peso": 0.15}
}'),
('Psicólogo(a) Clínico', 'Vaga para psicólogo(a) clínico com foco em terapia cognitivo-comportamental. Atuação 100% remota, atendendo pacientes de diversas localidades.', 'N/A', 'Remoto', 4,
'{
    "Formacao_Especializacao": {"descricao": "Pós-graduação ou especialização em Terapia Cognitivo-Comportamental (TCC).", "colunas": ["formacao", "sobre_mim"], "peso": 0.6},
    "Experiencia_Clinica": {"descricao": "Experiência mínima de 3 anos em atendimento clínico.", "colunas": ["experiencia_profissional"], "peso": 0.4}
}', true, null),
('Desenvolvedor(a) Front-end Júnior', 'Oportunidade para desenvolvedor(a) front-end júnior atuar em modelo híbrido em nosso polo de Jaboatão, trabalhando com React e TypeScript.', 'Jaboatão dos Guararapes', 'Híbrido', 1,
'{
    "Conhecimento_Frontend": {"descricao": "Conhecimento em React, HTML5, CSS3 e TypeScript.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.9},
    "Versionamento_Codigo": {"descricao": "Experiência básica com Git.", "colunas": ["sobre_mim"], "peso": 0.1}
}', true, null),
('Desenvolvedor Java Jr', '<p>A <strong>Cognvox</strong> está em constante evolução. Atuamos com projetos desafiadores que exigem alta performance e segurança.</p><p>Todas as nossas oportunidades são inclusivas e abertas para pessoas com deficiência.</p><hr><h2>DESAFIO</h2><p>Estamos em busca de um(a) profissional com conhecimentos em <strong>análise e desenvolvimento de sistemas, lógica de programação e bancos de dados</strong> para atuar <strong>presencialmente em Recife</strong>.</p>', 'Recife', 'Presencial', 1, 
'{
    "Ingles_": {"peso": 0.5, "colunas": ["idiomas"], "descricao": "precisa Ter ingles intermediario(b1-b2) pra mais (avançado c1-c2)"}, 
    "Java/Springboot": {"peso": 0.5, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Linguagem de programação para back-end (Spring Boot, JAVA)"}, 
    "Lógica_de_programação": {"peso": 0.3, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Precisa ter Sólidos conhecimentos em análise e desenvolvimento de sistemas e Lógica de programação"}, 
    "Banco_de_Dados_Relacionais_": {"peso": 0.5, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Precisa ter Banco de Dados (Oracle e/ou SQLServer)"}, 
    "Angular/javascript/typescript": {"peso": 0.3, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Precisa ter Angular/javascript/typescript"}
}', true,
'{
    "Sistemas_Financeiros": {"descricao": "Conhecimento em sistemas financeiros, legislativos ou demandas legais", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.2}
}');
-- V2__populate_tables.sql

INSERT INTO areas (nome, descricao) VALUES
('Tecnologia da Informação', 'Vagas relacionadas a desenvolvimento de software, infraestrutura, cibersegurança, etc.'),
('Recursos Humanos', 'Vagas para recrutamento, departamento pessoal, desenvolvimento organizacional e gestão de pessoas.'),
('Marketing e Vendas', 'Oportunidades para marketing digital, comunicação, vendas B2B/B2C e relacionamento com cliente.'),
('Psicologia', 'Vagas para psicólogos clínicos, organizacionais e outras especialidades da área.')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO vagas (titulo_vaga, descricao, cidade, modelo_trabalho, area_id, criterios_de_analise, vaga_pcd, criterios_diferenciais_de_analise) VALUES
('Desenvolvedor(a) Backend Pleno (Node.js)', 'Estamos à procura de um(a) Desenvolvedor(a) Backend Pleno para integrar nossa equipe em Recife. O candidato ideal deve ter experiência sólida na construção de APIs escaláveis utilizando Node.js e TypeScript.', 'Recife', 'Híbrido', 1,
'{
    "Experiencia_Tecnica": {"descricao": "Domínio em Node.js, TypeScript, SQL e Git.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.7},
    "Habilidades_DevOps": {"descricao": "Conhecimento em Docker, Kubernetes e AWS.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.3}
}', false, 
'{
    "Certificacao_Cloud": {"descricao": "Possuir certificações em nuvem (AWS, Azure, GCP) será um grande diferencial.", "colunas": ["cursos_extracurriculares"], "peso": 0.2}
}'),
('Analista de Recrutamento e Seleção Sênior', 'Buscamos um(a) Analista de Recrutamento e Seleção Sênior para atuar presencialmente em nosso escritório de Recife, com foco em vagas de tecnologia.', 'Recife', 'Presencial', 2,
'{
    "Experiencia_Tecnica_RS": {"descricao": "Experiência comprovada em recrutamento e seleção para posições de tecnologia.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.7},
    "Idiomas_e_Ferramentas": {"descricao": "Inglês avançado e familiaridade com sistemas ATS.", "colunas": ["idiomas", "sobre_mim"], "peso": 0.3}
}', false, null),
('Especialista em Marketing Digital', 'Procuramos um(a) Especialista em Marketing Digital para liderar e executar estratégias de crescimento online em nosso time de Jaboatão.', 'Jaboatão dos Guararapes', 'Presencial', 3,
'{
    "Estrategia_e_Execucao": {"descricao": "Experiência em marketing de conteúdo, SEO e Google Ads.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.8},
    "Analise_de_Dados": {"descricao": "Habilidade para analisar métricas e usar ferramentas de automação.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.2}
}', false, 
'{
    "Edicao_de_Video": {"descricao": "Conhecimento em Adobe Premiere ou Final Cut será um diferencial.", "colunas": ["cursos_extracurriculares", "sobre_mim"], "peso": 0.15}
}'),
('Psicólogo(a) Clínico', 'Vaga para psicólogo(a) clínico com foco em terapia cognitivo-comportamental. Atuação 100% remota, atendendo pacientes de diversas localidades.', 'N/A', 'Remoto', 4,
'{
    "Formacao_Especializacao": {"descricao": "Pós-graduação ou especialização em Terapia Cognitivo-Comportamental (TCC).", "colunas": ["formacao", "sobre_mim"], "peso": 0.6},
    "Experiencia_Clinica": {"descricao": "Experiência mínima de 3 anos em atendimento clínico.", "colunas": ["experiencia_profissional"], "peso": 0.4}
}', true, null),
('Desenvolvedor(a) Front-end Júnior', 'Oportunidade para desenvolvedor(a) front-end júnior atuar em modelo híbrido em nosso polo de Jaboatão, trabalhando com React e TypeScript.', 'Jaboatão dos Guararapes', 'Híbrido', 1,
'{
    "Conhecimento_Frontend": {"descricao": "Conhecimento em React, HTML5, CSS3 e TypeScript.", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.9},
    "Versionamento_Codigo": {"descricao": "Experiência básica com Git.", "colunas": ["sobre_mim"], "peso": 0.1}
}', true, null),
('Desenvolvedor Java Jr', '<p>A <strong>Cognvox</strong> está em constante evolução. Atuamos com projetos desafiadores que exigem alta performance e segurança.</p><p>Todas as nossas oportunidades são inclusivas e abertas para pessoas com deficiência.</p><hr><h2>DESAFIO</h2><p>Estamos em busca de um(a) profissional com conhecimentos em <strong>análise e desenvolvimento de sistemas, lógica de programação e bancos de dados</strong> para atuar <strong>presencialmente em Recife</strong>.</p>', 'Recife', 'Presencial', 1, 
'{
    "Ingles_": {"peso": 0.5, "colunas": ["idiomas"], "descricao": "precisa Ter ingles intermediario(b1-b2) pra mais (avançado c1-c2)"}, 
    "Java/Springboot": {"peso": 0.5, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Linguagem de programação para back-end (Spring Boot, JAVA)"}, 
    "Lógica_de_programação": {"peso": 0.3, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Precisa ter Sólidos conhecimentos em análise e desenvolvimento de sistemas e Lógica de programação"}, 
    "Banco_de_Dados_Relacionais_": {"peso": 0.5, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Precisa ter Banco de Dados (Oracle e/ou SQLServer)"}, 
    "Angular/javascript/typescript": {"peso": 0.3, "colunas": ["sobre_mim", "experiencia_profissional"], "descricao": "Precisa ter Angular/javascript/typescript"}
}', true,
'{
    "Sistemas_Financeiros": {"descricao": "Conhecimento em sistemas financeiros, legislativos ou demandas legais", "colunas": ["sobre_mim", "experiencia_profissional"], "peso": 0.2}
}');

INSERT INTO talentos (
    vaga_id, nome, email, cidade, telefone, sobre_mim, experiencia_profissional, formacao, idiomas, 
    respostas_criterios, respostas_diferenciais, redes_sociais, cursos_extracurriculares, deficiencia, deficiencia_detalhes, 
    aceita_termos, confirmar_dados_verdadeiros
) VALUES
(1, 'Ana Silva', 'ana.silva@email.com', 'Recife', '+55 81 98765-4321', 'Desenvolvedora backend com foco em APIs RESTful e microserviços.', '[{"empresa": "Tech Solutions", "cargo": "Desenvolvedora Backend Jr", "periodo": "2020-2022"}]', '[{"instituicao": "UFPE", "curso": "Ciência da Computação", "periodo": "2016-2020"}]', '[{"idioma": "Inglês", "nivel": "Avançado"}]', '{"Experiencia_Tecnica": "Tenho 2 anos de experiência desenvolvendo APIs com Node.js e SQL.", "Habilidades_DevOps": "Não possuo o critério"}', '{"Certificacao_Cloud": "Ainda não possuo certificações, mas tenho estudado para a AWS Cloud Practitioner."}', '[{"rede": "LinkedIn", "url": "https://linkedin.com/in/anasilva"}]', '[{"curso": "Arquitetura de Microserviços", "instituicao": "Alura"}]', false, null, true, true),
(1, 'Bruno Costa', 'bruno.costa@email.com', 'Recife', '+55 81 91234-5678', 'Apaixonado por tecnologia e soluções escaláveis na nuvem.', '[{"empresa": "Cloud Experts", "cargo": "Engenheiro DevOps", "periodo": "2021-Presente"}]', '[{"instituicao": "UPE", "curso": "Sistemas de Informação", "periodo": "2015-2019"}]', '[{"idioma": "Inglês", "nivel": "Fluente"}]', '{"Experiencia_Tecnica": "Tenho conhecimento básico em Node.js, mas meu forte é infraestrutura.", "Habilidades_DevOps": "Trabalho diariamente com Docker, Kubernetes e AWS há mais de 2 anos."}', '{"Certificacao_Cloud": "Possuo a certificação AWS Solutions Architect - Associate."}', '[{"rede": "LinkedIn", "url": "https://linkedin.com/in/brunocosta"}, {"rede": "GitHub", "url": "https://github.com/brunocosta"}]', '[{"curso": "Certificação AWS Solutions Architect", "instituicao": "AWS"}]', false, null, true, true),
(2, 'Carla Dias', 'carla.dias@email.com', 'Jaboatão dos Guararapes', '+55 81 99988-7766', 'Recrutadora com experiência em fechar posições complexas de tecnologia.', '[{"empresa": "Talent Hub", "cargo": "Tech Recruiter Sênior", "periodo": "2021-Presente"}]', '[{"instituicao": "UNICAP", "curso": "Psicologia", "periodo": "2013-2018"}]', '[{"idioma": "Inglês", "nivel": "Avançado"}]', '{"Experiencia_Tecnica_RS": "Possuo 5 anos de experiência como Tech Recruiter.", "Idiomas_e_Ferramentas": "Tenho inglês avançado e já utilizei as plataformas Gupy e Greenhouse."}', null, '[{"rede": "LinkedIn", "url": "https://linkedin.com/in/carladias"}]', null, true, '[{"tipo": "Auditiva", "descricao": "Utilizo aparelho auditivo e prefiro comunicação por texto ou videochamadas com legenda."}]', true, true),
(4, 'Mariana Lima', 'mariana.lima@email.com', 'Cururipe', '+55 82 98877-1122', 'Psicóloga clínica dedicada ao bem-estar e saúde mental, com especialização em TCC.', '[]', '[{"instituicao": "UFAL", "curso": "Psicologia", "periodo": "2014-2019"}]', '[]', '{"Formacao_Especializacao": "Concluí minha pós-graduação em TCC no ano passado.", "Experiencia_Clinica": "Atuo em clínica há 4 anos."}', null, '[{"rede": "LinkedIn", "url": "https://linkedin.com/in/marianalima"}]', '[{"curso": "Mindfulness para Terapeutas", "instituicao": "Instituto Cognitivo"}]', false, null, true, true),
(5, 'Lucas Pereira', 'lucas.pereira@email.com', 'Jaboatão dos Guararapes', '+55 81 98811-2233', 'Entusiasta de interfaces e experiência do usuário, buscando minha primeira oportunidade em front-end.', '[{"empresa": "Freelance", "cargo": "Web Designer", "periodo": "2023-Presente"}]', '[{"instituicao": "SENAC", "curso": "Análise e Desenv. de Sistemas", "periodo": "2022-2024"}]', '[{"idioma": "Inglês", "nivel": "Intermediário"}]', '{"Conhecimento_Frontend": "Desenvolvi diversos projetos pessoais e acadêmicos com React e TypeScript.", "Versionamento_Codigo": "Utilizo Git e GitHub em todos os meus projetos."}', null, '[{"rede": "GitHub", "url": "https://github.com/lucaspereira"}]', null, false, null, true, true),
(6, 'Miguel Augusto Sales do Amaral', 'miguel.amaral.sales@gmail.com', 'Recife', '+55 (81) 99637-9353', 'Desenvolvedor Backend com sólida experiência em Java e Springboot.', '[{"cargo": "Desenvolvedor Fullstack", "empresa": "Incubadora i.de.i.a.S", "periodo": "2023-10 - 2025-03", "descricao": "Garanti a escalabilidade e o desempenho da aplicação."}, {"cargo": "Desenvolvedor Fullstack", "empresa": "Senac/Fecomércio-PE", "periodo": "2025-01 - 2025-07", "descricao": "Assumi a liderança de um projeto crítico para a Missão NRF 2025."}]', '[{"curso": "Análise e Desenvolvimento de Sistemas", "cursando": true, "data_fim": "", "data_inicio": "2024-08-28", "instituicao": "Faculdade Senac PE", "periodo_atual": "5"}]', '[{"nivel": "C1 - Avançado", "idioma": "Inglês"}, {"nivel": "B1 - Intermediário", "idioma": "Espanhol"}]', '{"Ingles_": "Fui responsável por suporte e manutenção de sistemas para clientes globais.", "Java/Springboot": "Possuo 3 anos de experiencia ultilizando Java com springboot.", "Lógica_de_programação": "Possuo um bom dominio de logica de programação.", "Banco_de_Dados_Relacionais_": "Tenho 3 anos de experiencia ultilizando bancos de dados dos mais diversos.", "Angular/javascript/typescript": "Possuo 2 anos de experiência ultilziando Angular."}', '{"Sistemas_Financeiros": "Tenho experiência com desenvolvimento de integrações para sistemas de pagamento."}', '[{"rede": "LinkedIn", "url": "https://linkedin.com/in/miguel-amaral-sales"}, {"rede": "GitHub", "url": "https://github.com/Miguel-Amaral-Sales"}]', '[{"curso": "Imersão Java", "instituicao": "Alura"}]', false, null, true, true)
ON CONFLICT (email, vaga_id) DO NOTHING;

INSERT INTO users (nome, email, hashed_password, role) VALUES
('Miguel Admin', 'miguel.admin@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 'admin'),
('Usuário Um', 'usuario.um@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 'user1'),
('Usuário Dois', 'usuario.dois@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 'user2')
ON CONFLICT (email) DO NOTHING;

SELECT setval('areas_id_seq', (SELECT MAX(id) FROM areas), true);
SELECT setval('vagas_id_seq', (SELECT MAX(id) FROM vagas), true);
SELECT setval('talentos_id_seq', (SELECT MAX(id) FROM talentos), true);