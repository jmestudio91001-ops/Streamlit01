import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import sqlite3
import os

# --- CONFIGURACIÓN DE LA PÁGINA ---
# Establecemos el título de la pestaña y el layout ancho para mejor visualización de tablas
st.set_page_config(
    page_title="Bienestar Estudiantil - Julio Molinares",
    page_icon="🧠",
    layout="wide"
)

# Aplicar estilo de Seaborn para gráficos profesionales
sns.set_theme(style="whitegrid", palette="viridis")

# --- LÓGICA DE DATOS (Kaggle + SQL) ---
@st.cache_data(show_spinner=False)
def load_data():
    """
    Descarga el dataset desde Kaggle y lo prepara.
    Incluye corrección para errores de delimitadores (sep=None) y líneas mal formadas.
    """
    try:
        # Descarga automática usando kagglehub
        path = kagglehub.dataset_download("thedevastator/medical-student-mental-health")
        
        # Buscamos archivos CSV en la carpeta descargada
        files = [f for f in os.listdir(path) if f.endswith('.csv') and not f.startswith('.')]
        
        if not files:
            st.error("No se encontraron archivos de datos en el repositorio de Kaggle.")
            return pd.DataFrame()
            
        # Seleccionamos el archivo más grande (dataset principal)
        main_file = max(files, key=lambda f: os.path.getsize(os.path.join(path, f)))
        full_path = os.path.join(path, main_file)
        
        # Lectura robusta para evitar errores de 'Expected 1 fields, saw 2'
        df = pd.read_csv(
            full_path, 
            sep=None,            # Detecta automáticamente si usa , o ;
            engine='python',     # Necesario para la detección automática
            on_bad_lines='skip', # Ignora filas con errores en lugar de detener la app
            encoding='utf-8'
        )
        
        # Normalizamos nombres de columnas para que sean compatibles con SQL (sin espacios ni caracteres raros)
        df.columns = [c.strip().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace('/', '_') for c in df.columns]
        
        return df
    except Exception as e:
        st.error(f"Error técnico al procesar el dataset: {e}")
        return pd.DataFrame()

def run_query(query, df):
    """
    Ejecuta consultas SQL sobre los datos cargados.
    Crea una tabla temporal en memoria llamada 'salud_mental'.
    """
    conn = sqlite3.connect(':memory:')
    df.to_sql('salud_mental', conn, index=False, if_exists='replace')
    return pd.read_sql_query(query, conn)

# --- SISTEMA DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def set_page(page_name):
    st.session_state.page = page_name

# --- INTERFAZ DE USUARIO (UI) ---

# 1. LANDING PAGE
if st.session_state.page == 'landing':
    st.title("🛡️ Análisis de Salud Mental en Estudiantes de Medicina")
    st.subheader("Proyecto Integrador - Talento Tech | Julio Molinares")
    
    col_text, col_img = st.columns([1, 1], gap="large")
    
    with col_text:
        st.markdown(f"""
        ### Bienvenido al Panel Analítico
        **Analista:** Julio Molinares
        
        Este proyecto es la culminación del curso nivel integrador. Aquí aplicamos:
        - **Modelado de Datos:** Estructura relacional eficiente.
        - **SQL:** Consultas dinámicas sobre datos reales.
        - **Visualización:** Gráficos estadísticos con Seaborn.
        
        *Haz clic en el botón para iniciar el análisis y cargar el dataset desde Kaggle.*
        """)
        if st.button("Explorar Panel de Trabajo 📊", use_container_width=True, type="primary"):
            set_page('dashboard')
            st.rerun()
            
    with col_img:
        st.image("https://images.unsplash.com/photo-1576091160550-2173dba999ef?auto=format&fit=crop&q=80&w=800", 
                 caption="Gestión de Datos y Salud Mental")

    st.divider()
    st.info("Desarrollado con Python, SQL, Pandas y Seaborn.")

# 2. DASHBOARD TÉCNICO
else:
    # Sidebar
    st.sidebar.title("Navegación")
    st.sidebar.image("https://images.unsplash.com/photo-1559757175-5700dde675bc?auto=format&fit=crop&q=80&w=200")
    if st.sidebar.button("🏠 Volver al Inicio"):
        set_page('landing')
        st.rerun()
    
    st.sidebar.divider()
    st.sidebar.markdown(f"**Estudiante:**\nJulio Molinares")

    # Carga de datos con feedback visual para el usuario
    with st.spinner('Sincronizando con Kaggle y preparando tablas SQL...'):
        df = load_data()

    if not df.empty:
        st.title("📊 Panel Analítico: Salud Mental Estudiantil")
        
        tab_graficos, tab_sql, tab_docs = st.tabs(["📈 Análisis Visual", "💻 Consola SQL", "📖 Documentación"])

        with tab_graficos:
            st.header("Análisis de Factores Críticos")
            
            # Identificación automática de columnas para evitar errores si el dataset cambia ligeramente
            col_sleep = next((c for c in df.columns if 'Sleep' in c), None)
            col_phq = next((c for c in df.columns if 'PHQ' in c or 'Depression' in c), None)
            col_gender = next((c for c in df.columns if 'Gender' in c), None)
            col_gad = next((c for c in df.columns if 'GAD' in c or 'Anxiety' in c), None)

            # Gráfico 1: Sueño vs Depresión
            if col_sleep and col_phq:
                st.subheader(f"1. Relación entre Depresión ({col_phq}) y Sueño")
                col_g1, col_h1 = st.columns([3, 1])
                with col_g1:
                    fig1, ax1 = plt.subplots(figsize=(10, 5))
                    sns.boxenplot(data=df, x=col_sleep, y=col_phq, ax=ax1, palette="mako")
                    st.pyplot(fig1)
                with col_h1:
                    with st.popover("💡 Ayuda"):
                        st.write("Este gráfico muestra cómo varían los síntomas depresivos según las horas de sueño. Las cajas extendidas representan la distribución estadística de los estudiantes.")

            st.divider()

            # Gráfico 2: Densidad de Ansiedad por Género
            if col_gender and col_gad:
                st.subheader(f"2. Distribución de Ansiedad ({col_gad}) por Género")
                col_g2, col_h2 = st.columns([3, 1])
                with col_g2:
                    fig2, ax2 = plt.subplots(figsize=(10, 5))
                    sns.violinplot(data=df, x=col_gender, y=col_gad, ax=ax2, inner="quart", palette="magma")
                    st.pyplot(fig2)
                with col_h2:
                    with st.popover("💡 Ayuda"):
                        st.write("El gráfico de violín permite comparar la densidad de los niveles de ansiedad entre diferentes géneros, mostrando dónde se concentra la mayor cantidad de casos.")

        with tab_sql:
            st.header("Motor de Consultas SQL")
            st.markdown("Tabla disponible: `salud_mental` (Datos normalizados)")
            
            # Consulta por defecto basada en columnas detectadas
            c_gen = col_gender if col_gender else df.columns[0]
            c_val = col_phq if col_phq else df.columns[1]
            
            query_input = st.text_area(
                "Escribe tu consulta SQL aquí:", 
                f"SELECT {c_gen}, AVG({c_val}) as Promedio FROM salud_mental GROUP BY {c_gen}"
            )
            
            if st.button("Ejecutar Consulta ⚡"):
                try:
                    res = run_query(query_input, df)
                    st.success("Consulta ejecutada con éxito")
                    st.dataframe(res, use_container_width=True)
                except Exception as e:
                    st.error(f"Error en SQL: {e}")

        with tab_docs:
            st.header("Ficha Técnica del Proyecto")
            st.write(f"**Registros totales:** {len(df)}")
            st.markdown("""
            ### Metodología de Ingeniería de Datos
            - **Extracción:** Conexión vía API con el repositorio de salud mental en Kaggle.
            - **Limpieza:** Implementación de motores de lectura flexibles para evitar errores de delimitadores variables.
            - **Arquitectura:** Creación de una base de datos SQLite efímera para habilitar el motor de consultas relacionales.
            
            ### Fórmulas Aplicadas
            $$ \bar{x} = \frac{\sum x_i}{N} $$
            
            **Analista Principal:** Julio Molinares
            """)

    else:
        st.error("No se pudo cargar el dataset. Verifica tu conexión a internet o el estado del archivo en Kaggle.")

# Pie de página
st.markdown("---")
st.caption("Julio Molinares | Proyecto Integrador Talento Tech 2026")
