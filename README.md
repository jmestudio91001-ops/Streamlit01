📑 Documentación Técnica: Salud Mental en Estudiantes de Medicina

Estudiante: Julio Molinares

Bootcamp: Talento Tech - Nivel Integrador

Dataset: Medical Student Mental Health (Kaggle)

1. Modelo Entidad-Relación (MER)

Para este dataset, la normalización se enfoca en separar los datos demográficos de los resultados de salud mental y el contexto académico para asegurar la integridad de la información y evitar redundancias.

Estudiante: Entidad principal que almacena información básica del individuo (Edad, Género).

Contexto_Academico: Almacena el año de estudio y la percepción de presión académica.

Evaluacion_Psicologica: Contiene los resultados de las escalas clínicas (PHQ-9 para depresión, GAD-7 para ansiedad) y métricas de hábitos (Calidad de Sueño).

2. Modelo Relacional

La estructura de tablas definida para la base de datos es la siguiente:

Estudiantes (id_estudiante PK, edad, genero)

Academico (id_academico PK, id_estudiante FK, año_estudio, presion_academica)

Salud_Mental (id_salud PK, id_estudiante FK, score_depresion, score_ansiedad, calidad_sueño, nivel_estres)

3. Scripts SQL (DDL)

Estos scripts definen la estructura de la base de datos en SQLite. Se han incluido restricciones de llaves foráneas para mantener la integridad referencial.

-- Tabla de Estudiantes
CREATE TABLE IF NOT EXISTS Estudiantes (
    id_estudiante INTEGER PRIMARY KEY AUTOINCREMENT,
    genero TEXT NOT NULL,
    edad INTEGER CHECK(edad > 0)
);

-- Tabla de Contexto Académico
CREATE TABLE IF NOT EXISTS Academico (
    id_academico INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER,
    año_estudio TEXT,
    presion_academica INTEGER,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante)
);

-- Tabla de Salud Mental y Evaluación
CREATE TABLE IF NOT EXISTS Salud_Mental (
    id_salud INTEGER PRIMARY KEY AUTOINCREMENT,
    id_estudiante INTEGER,
    score_depresion INTEGER, -- Escala PHQ-9
    score_ansiedad INTEGER,   -- Escala GAD-7
    calidad_sueño INTEGER,
    nivel_estres INTEGER,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante)
);


4. Consultas Analíticas (DML)

A continuación, se presentan las consultas SQL diseñadas para extraer los KPIs (Indicadores Clave de Desempeño) que se mostrarán en el dashboard:

Promedio de Ansiedad (GAD-7) por Género:

SELECT e.genero, AVG(s.score_ansiedad) as Promedio_Ansiedad
FROM Estudiantes e
JOIN Salud_Mental s ON e.id_estudiante = s.id_estudiante
GROUP BY e.genero;


Relación entre Calidad de Sueño y Niveles de Estrés:

SELECT calidad_sueño, AVG(nivel_estres) as Promedio_Estres
FROM Salud_Mental
GROUP BY calidad_sueño
ORDER BY calidad_sueño DESC;


Distribución de Depresión por Año de Estudio:

SELECT a.año_estudio, AVG(s.score_depresion) as Promedio_Depresion
FROM Academico a
JOIN Salud_Mental s ON a.id_estudiante = s.id_estudiante
GROUP BY a.año_estudio;


Este diseño de base de datos y lógica de consultas garantiza un análisis robusto y escalable para el entorno de Talento Tech.
