-- ===============================
-- Banco de dados CadastroUsuarios
-- ===============================

-- Criação do banco, se não existir
IF DB_ID('CadastroUsuarios') IS NULL
BEGIN
    CREATE DATABASE CadastroUsuarios;
    PRINT 'Banco CadastroUsuarios criado!';
END
GO

-- Selecionar o banco
USE CadastroUsuarios;
GO

-- ===============================
-- Tabela de Usuários
-- ===============================
CREATE TABLE Usuarios (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    NOME VARCHAR(100) NOT NULL,
    CPF CHAR(11) NOT NULL UNIQUE,
    TELEFONE VARCHAR(15),
    EMAIL VARCHAR(100) UNIQUE,
    SENHA VARCHAR(255) NOT NULL,
    NIVEL VARCHAR(20) NOT NULL DEFAULT 'cliente',
    FOTO VARCHAR(255) NOT NULL DEFAULT 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3lUXoW_2yUPKkKpFEVGM04gsRowd0vCyXew&s'
);
GO

-- ===============================
-- Tabela de Propriedades
-- ===============================
CREATE TABLE Propriedades (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    LOCAL VARCHAR(100) NOT NULL,
    PRECO DECIMAL(12,2) NOT NULL,
    QUARTOS INT NOT NULL,
    TAMANHO DECIMAL(10,2) NOT NULL,
    IMAGEM VARCHAR(1000) NOT NULL,
    USUARIO_ID INT NOT NULL,
    CONSTRAINT FK_Propriedades_Usuario FOREIGN KEY (USUARIO_ID)
        REFERENCES Usuarios(ID) ON DELETE NO ACTION
);
GO

-- ===============================
-- Tabela de Reservas
-- ===============================
CREATE TABLE Reservas (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    USUARIO_ID INT NOT NULL,
    PROPRIEDADE_ID INT NOT NULL,
    PRECO DECIMAL(12,2) NOT NULL,
    DATA_RESERVA DATE NOT NULL,
    FIM_RESERVA DATE NULL,
    CONSTRAINT FK_Reserva_Usuario FOREIGN KEY (USUARIO_ID)
        REFERENCES Usuarios(ID) ON DELETE NO ACTION,
    CONSTRAINT FK_Reserva_Propriedade FOREIGN KEY (PROPRIEDADE_ID)
        REFERENCES Propriedades(ID) ON DELETE NO ACTION
);
GO

-- ===============================
-- Teste de Inserção
-- ===============================
INSERT INTO Usuarios (NOME, CPF, TELEFONE, EMAIL, SENHA, NIVEL, FOTO)
VALUES
('Enzo Brabo', '12345678900', '119999992769', 'enzo.brabo@email.com', '123456', 'adm', 'https://i.pinimg.com/736x/1f/23/2c/1f232c997c78b91b738e1e4ac0896b9d.jpg');

INSERT INTO Propriedades (LOCAL, IMAGEM, PRECO, QUARTOS, TAMANHO, USUARIO_ID)
VALUES
('Rua das Flores, 123', 'https://news.airbnb.com/wp-content/uploads/sites/4/2020/05/Governador-Celso-Ramos-Santa-Catarina-Brazil-156247-1.jpg', 250000.00, 3, 120.50, 1);

INSERT INTO Reservas (USUARIO_ID, PROPRIEDADE_ID, PRECO, DATA_RESERVA, FIM_RESERVA)
VALUES
(1, 1, 350000.00, '2025-11-01', '2025-11-10');

-- ===============================
-- Visualização
-- ===============================
SELECT * FROM Usuarios;
SELECT * FROM Propriedades;
SELECT * FROM Reservas;


DROP TABLE Reservas;
DROP TABLE Propriedades;
DROP TABLE Usuarios;


USE CadastroUsuarios;
GO

DROP TABLE IF EXISTS Reservas;
DROP TABLE IF EXISTS Propriedades;
DROP TABLE IF EXISTS Usuarios;
GO
