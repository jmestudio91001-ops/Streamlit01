📑 Documentación de Datos: Salud Mental en Estudiantes de Medicina

Estudiante: Julio Molinares

Bootcamp: Talento Tech - Nivel Integrador

Este documento detalla la arquitectura de datos diseñada para transformar el dataset crudo en una base de datos relacional estructurada.

1. Modelo Entidad-Relación (MER)

El modelo se basa en tres entidades principales que capturan la información demográfica, el entorno académico y los indicadores clínicos de salud mental.

erDiagram
    ESTUDIANTE ||--|| ACADEMICO : cursa
    ESTUDIANTE ||--|| SALUD_MENTAL : presenta
    
    ESTUDIANTE {
        int id_estudiante PK
        string genero
        int edad
    }
    
    ACADEMICO {
        int id_academico PK
        int id_estudiante FK
        string año_estudio
        int presion_academica
    }
    
    SALUD_MENTAL {
        int id_salud PK
        int id_estudiante FK
        int score_depresion
        int score_ansiedad
        int calidad_sueño
        int nivel_estres
    }


2. Modelo Relacional

La estructura de tablas sigue las reglas de normalización para evitar la redundancia de datos.

Tabla: Estudiantes

Campo

Tipo

Descripción

id_estudiante

INTEGER (PK)

Identificador único del estudiante.

genero

VARCHAR

Identidad de género del encuestado.

edad

INTEGER

Edad cronológica.

Tabla: Academico

Campo

Tipo

Descripción

id_academico

INTEGER (PK)

Identificador del registro académico.

id_estudiante

INTEGER (FK)

Referencia a la tabla Estudiantes.

año_estudio

VARCHAR

Año actual de la carrera médica.

presion_academica

INTEGER

Nivel de presión percibida (Escala 1-5).

Tabla: Salud_Mental

Campo

Tipo

Descripción

id_salud

INTEGER (PK)

Identificador del registro de salud.

id_estudiante

INTEGER (FK)

Referencia a la tabla Estudiantes.

score_depresion

INTEGER

Puntaje obtenido en la escala PHQ-9.

score_ansiedad

INTEGER

Puntaje obtenido en la escala GAD-7.

calidad_sueño

INTEGER

Autoevaluación de la calidad del sueño.

nivel_estres

INTEGER

Nivel de estrés reportado.

3. Justificación del Modelo

Normalización: Se separaron los datos en tres tablas para facilitar consultas específicas sin procesar columnas innecesarias (ej. consultar salud mental sin cargar datos académicos).

Integridad: Se utilizan Llaves Primarias (PK) y Foráneas (FK) para asegurar que cada evaluación psicológica pertenezca a un estudiante existente.

Escalabilidad: Este diseño permite agregar nuevas encuestas en el futuro simplemente añadiendo registros a las tablas de hechos (Salud_Mental).

Realizado por: Julio Molinares

Institución: Talento Tech
