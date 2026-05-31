-- ========================================================
-- DATOS DE PRUEBA (DML)
-- ========================================================

-- Creamos un Horario para poder asignarlo a un Curso
INSERT INTO HORARIO (id, formato, hora_inicio, hora_fin) 
VALUES (1, 'Presencial', '08:00:00', '14:30:00');

-- Creamos un Curso para poder matricular al Alumno y Profesor
INSERT INTO CURSO (id, nivel, curso, modulo, id_horario) 
VALUES (1, 'Secundaria', '3º ESO', 'Matemáticas', 1);

-- CREACIÓN DE LOS USUARIOS BASE
INSERT INTO USUARIO (id, nombre, apellidos, activo, password) VALUES 
(1, 'Admin', 'Sistema', 1, 'hash_pass_root_123'),
(2, 'Laura', 'Martínez', 1, 'hash_pass_profe_123'),
(3, 'Carlos', 'Gómez', 1, 'hash_pass_direc_123'),
(4, 'Lucía', 'Pérez', 1, 'hash_pass_alum_123'),
(5, 'Pablo', 'Ruiz', 1, 'hash_pass_alum2_123');

-- ROLES
-- ROOT 
INSERT INTO ROOT (id) 
VALUES (1);

-- PROFESOR 
INSERT INTO PROFESOR (id, id_curso) 
VALUES (2, 1);

-- DIRECTIVO 
-- El Usuario 3 TIENE que ser insertado en Profesor primero
INSERT INTO PROFESOR (id, id_curso) 
VALUES (3, 1);

INSERT INTO DIRECTIVO (id, cargo) 
VALUES (3, 'Jefe de Estudios');

-- ALUMNO (Enlazados a los Usuarios 4 y 5 y al Curso 1)
INSERT INTO ALUMNO (id, id_curso) 
VALUES (4, 1), (5, 1);


-- 4. CADENA DE RECONOCIMIENTOS Y PROBIS
-- Registramos una actitud (del Alumno con ID 4)
INSERT INTO ACTITUD (id, descripcion, fecha, tipo, id_usuario) 
VALUES (1, 'Colaboración excepcional en un proyecto de ciencias', CURDATE(), 'Positiva', 4);

-- El profesor (ID 2) crea un reconocimiento basado en esa actitud
INSERT INTO RECONOCIMIENTO (id, detalle, id_actitud, id_profesor) 
VALUES (1, 'Reconocimiento en el tablón de la clase', 1, 2);

-- Generamos la mención a partir de ese reconocimiento
INSERT INTO MENCION (id, fecha, id_reconocimiento) 
VALUES (1, CURDATE(), 1);

-- Creamos el PROBI asociado a esa mención
INSERT INTO PROBI (id, fecha, id_mencion) 
VALUES (1, CURDATE(), 1);


-- 5. CADENA DE EXPEDIENTES Y PREVIS
-- Ejemplo: El directivo (ID 3) abre un expediente al alumno (ID 4)
INSERT INTO EXPEDIENTE (id, estado, id_alumno, id_directivo) 
VALUES (1, 'En trámite', 4, 3);

-- El directivo añade una acción previa (PREVI) a ese expediente
INSERT INTO PREVI (id, detalle, fecha, id_directivo, id_expediente) 
VALUES (1, 'Entrevista preliminar con la familia del alumno', CURDATE(), 3, 1);


-- 6. INSERCIÓN DE TAREAS
-- id_profesor = 2 (Laura), id_alumno = 4 (Lucía)
INSERT INTO TAREA (descripcion, estado, id_profesor, id_alumno) 
VALUES ('Hacer los ejercicios del 1 al 5 de la página 34 de Matemáticas', 'PENDIENTE', 2, 4);

INSERT INTO TAREA (descripcion, estado, id_profesor, id_alumno) 
VALUES ('Redacción sobre la Revolución Francesa', 'COMPLETADA', 2, 4);


-- 7. INSERCIÓN DE ACTITUDES Y AMONESTACIONES
-- Actitud generará el id=2 (porque el 1 se usó en el paso 4)
INSERT INTO ACTITUD (id, descripcion, fecha, tipo, id_usuario) 
VALUES (2, 'Falta de respeto continuada durante la clase de historia', '2024-05-20', 'NEGATIVA', 4);

-- Amonestación para la actitud 2, puesta por el profesor 2
INSERT INTO AMONESTACION (nivel, id_actitud, id_profesor) 
VALUES ('GRAVE', 2, 2);

-- Otro ejemplo: Actitud generará id=3
INSERT INTO ACTITUD (id, descripcion, fecha, tipo, id_usuario) 
VALUES (3, 'Uso del teléfono móvil en clase', '2024-05-21', 'NEGATIVA', 4);

-- Amonestación para la actitud 3
INSERT INTO AMONESTACION (nivel, id_actitud, id_profesor) 
VALUES ('LEVE', 3, 2);


-- 8. AULA DE CONVIVENCIA
-- Crear el registro del aula de convivencia para un día concreto
INSERT INTO AULA_CONVIVENCIA (id, nombre, fecha, id_horario) 
VALUES (1, 'Aula de Convivencia Castigo Recreo', '2024-05-28', 1);

-- Meter alumnos dentro de ese aula de convivencia 
-- Usamos los únicos alumnos válidos: 4 (Lucía) y 5 (Pablo)
INSERT INTO AULA_CONVIVENCIA_ALUMNO (id_aula_convivencia, id_alumno) VALUES (1, 4);
INSERT INTO AULA_CONVIVENCIA_ALUMNO (id_aula_convivencia, id_alumno) VALUES (1, 5);