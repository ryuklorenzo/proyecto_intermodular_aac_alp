-- create database myapi;
-- use database myapi;

CREATE TABLE USUARIO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    activo TINYINT(1) DEFAULT 1,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE ROOT (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES USUARIO(id) ON DELETE CASCADE
);

-- Personas

CREATE TABLE PROFESOR (
    id INT PRIMARY KEY, 
    FOREIGN KEY (id) REFERENCES USUARIO(id) ON DELETE CASCADE
);

CREATE TABLE DIRECTIVO (
    id INT PRIMARY KEY, 
    cargo VARCHAR(50), 
    FOREIGN KEY (id) REFERENCES PROFESOR(id) ON DELETE CASCADE
);

-- Cosas de clase, cursos

CREATE TABLE HORARIO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    formato VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

CREATE TABLE CURSO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nivel VARCHAR(25) NOT NULL,
    curso VARCHAR(25) NOT NULL,
    modulo VARCHAR(25) NOT NULL,
    id_horario INT,
    FOREIGN KEY (id_horario) REFERENCES HORARIO(id) 
);

CREATE TABLE ALUMNO (
    id INT PRIMARY KEY,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_curso) REFERENCES CURSO(id),
    FOREIGN KEY (id) REFERENCES USUARIO(id) ON DELETE CASCADE
);


CREATE TABLE AULA_CONVIVENCIA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    fecha DATE,
    id_horario INT NOT NULL,
    FOREIGN KEY (id_horario) REFERENCES HORARIO(id)
);


-- crear la tabla m-m que faltaba
CREATE TABLE AULA_CONVIVENCIA_ALUMNO (
    id_aula_convivencia INT,
    id_alumno INT,
    PRIMARY KEY (id_aula_convivencia, id_alumno),
    FOREIGN KEY (id_aula_convivencia) REFERENCES AULA_CONVIVENCIA(id),
    FOREIGN KEY (id_alumno) REFERENCES ALUMNO(id)
);


-- tablas relacionales

CREATE TABLE ACTITUD (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    fecha DATE,
    tipo VARCHAR(20) NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id)
);

CREATE TABLE TAREA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT,
    estado VARCHAR(25) NOT NULL,
    id_profesor INT NOT NULL,
    id_alumno INT NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES PROFESOR(id),
    FOREIGN KEY (id_alumno) REFERENCES ALUMNO(id)
);

-- CREATE TABLE CURSO_ALUMNO (
--     id_curso INT,
--     id_alumno INT,
--     PRIMARY KEY (id_curso, id_alumno),
--     FOREIGN KEY (id_curso) REFERENCES CURSO(id),
--     FOREIGN KEY (id_alumno) REFERENCES ALUMNO(id)
-- );

CREATE TABLE EXPEDIENTE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(50) NOT NULL,
    id_directivo INT NOT NULL, 
    FOREIGN KEY (id_directivo) REFERENCES DIRECTIVO(id)
);

CREATE TABLE PREVI (
    id INT AUTO_INCREMENT PRIMARY KEY,
    detalle TEXT,
    fecha DATE,
    id_directivo INT NOT NULL,
    id_expediente INT,
    FOREIGN KEY (id_directivo) REFERENCES DIRECTIVO(id),
    FOREIGN KEY (id_expediente) REFERENCES EXPEDIENTE(id)
);

-- Cosas a parte

CREATE TABLE AMONESTACION (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nivel VARCHAR(20) NOT NULL,
    id_actitud INT,
    FOREIGN KEY (id_actitud) REFERENCES ACTITUD(id)
);

CREATE TABLE RECONOCIMIENTO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    detalle TEXT,
    id_actitud INT,
    FOREIGN KEY (id_actitud) REFERENCES ACTITUD(id)
);

CREATE TABLE MENCION (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    id_reconocimiento INT,
    FOREIGN KEY (id_reconocimiento) REFERENCES RECONOCIMIENTO(id)
);

CREATE TABLE PROBI (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    id_mencion INT,
    FOREIGN KEY (id_mencion) REFERENCES MENCION(id)
);

-- usuario -> alumno
-- usuario -> profesor 
-- usuario -> profesor -> directivo
-- root
-- usuario -> actitud
-- usuario -> actitud -> amonestacion
-- usuario -> actitud -> reconocimiento
-- usuario -> actitud -> reconocimiento -> mencion
-- usuario -> actitud -> reconocimiento -> mencion -> porbi
-- usuario -> profesor -> directivo -> expediente
-- usuario -> profesor -> directivo & expediente -> previ
-- horario -> curso
-- usuario -> profesor & alumno -> tarea
-- curso & alumno -> curso_alumno 
-- aula-convivencia & alumno -> aula_convivencia_alumno