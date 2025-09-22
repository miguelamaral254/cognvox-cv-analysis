-- V2__populate_tables.sql

INSERT IGNORE INTO areas (nome, descricao) VALUES
('Tecnologia da Informação', 'Vagas relacionadas a desenvolvimento de software, infraestrutura, cibersegurança, etc.'),
('Recursos Humanos', 'Vagas para recrutamento, departamento pessoal, desenvolvimento organizacional e gestão de pessoas.'),
('Marketing e Vendas', 'Oportunidades para marketing digital, comunicação, vendas B2B/B2C e relacionamento com cliente.'),
('Psicologia', 'Vagas para psicólogos clínicos, organizacionais e outras especialidades da área.');

INSERT IGNORE INTO users (nome, email, hashed_password, is_active, user_role_id) VALUES
('Miguel Admin', 'miguel.admin@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 1, 1),
('Usuário Um', 'usuario.um@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 1, 2),
('Usuário Dois', 'usuario.dois@example.com', '$2b$12$kODB6/ASOEVpcQB742v4qehmqqy8z44txJVpOAFpXpy5qrS/uOqYq', 1, 3);

SELECT setval('areas_id_seq', (SELECT MAX(id) FROM areas), true);
SELECT setval('vagas_id_seq', (SELECT MAX(id) FROM vagas), true);
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users), true);
SELECT setval('talentos_id_seq', (SELECT MAX(id) FROM talentos), true);
SELECT setval('comentarios_talentos_id_seq', (SELECT MAX(id) FROM comentarios_talentos), true);