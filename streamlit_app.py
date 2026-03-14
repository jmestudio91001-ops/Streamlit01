import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import sqlite3
import os

# Configuración de la página
st.set_page_config(
    page_title="Bienestar Estudiantil - Julio Molinares",
    page_icon="🧠",
    layout="wide"
)

# Estilo profesional de Seaborn
sns.set_theme(style="whitegrid", palette="deep")

# --- LÓGICA DE DATOS Y SQL ---
@st.cache_data
def load_and_prepare_data():
    """Descarga el dataset y lo prepara para SQL."""
    try:
        # Descarga desde Kagglehub
        path = kagglehub.dataset_download("thedevastator/medical-student-mental-health")
        csv_file = [f for f in os.listdir(path) if f.endswith('.csv')][0]
        df = pd.read_csv(os.path.join(path, csv_file))
        
        # Limpieza de nombres de columnas para evitar errores en SQL
        df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

def init_sql_engine(df):
    """Crea una base de datos SQLite en memoria a partir del DataFrame."""
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    df.to_sql('salud_mental', conn, index=False, if_exists='replace')
    return conn

# --- GESTIÓN DE NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def navigate_to(page):
    st.session_state.page = page

# --- COMPONENTES DE LA INTERFAZ ---

# 1. LANDING PAGE
if st.session_state.page == 'landing':
    st.title("🧠 Análisis de Salud Mental en Estudiantes de Medicina")
    st.subheader("Proyecto Integrador - Talento Tech")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("""
        ### Contexto del Estudio
        La educación médica es reconocida como uno de los entornos académicos más estresantes. Este proyecto utiliza 
        herramientas avanzadas de **Ciencia de Datos** para analizar la prevalencia de ansiedad, depresión y 
        problemas de sueño en futuros profesionales de la salud.
        
        **Objetivos del Análisis:**
        * Identificar la correlación entre hábitos de sueño y salud mental.
        * Evaluar niveles de estrés según el año de estudio.
        * Proveer una plataforma interactiva para consultas SQL en tiempo real.
        
        **Tecnologías:** Python, SQL, Streamlit, Seaborn.
        """)
        if st.button("Explorar Panel de Trabajo 📊", use_container_width=True, type="primary"):
            navigate_to('dashboard')
            st.rerun()
            
    with col2:
        # Imagen representativa del tema
        st.image("https://images.unsplash.com/photo-1527613426441-4da17471b66d?auto=format&fit=crop&q=80&w=800", 
                 caption="Bienestar y Salud Mental en el ámbito clínico")

    st.divider()
    st.info("📌 **Nota Técnica:** Los datos son procesados mediante una arquitectura relacional en SQLite para garantizar la integridad de los insights.")
    st.caption("Realizado por: **Julio Molinares**")

# 2. DASHBOARD PRINCIPAL
else:
    df = load_and_prepare_data()
    if df.empty:
        st.stop()
        
    conn = init_sql_engine(df)
    
    # Sidebar de navegación
    st.sidebar.title("Panel de Control")
    st.sidebar.image("https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&q=80&w=200")
    if st.sidebar.button("🏠 Volver al Inicio"):
        navigate_to('landing')
        st.rerun()
        
    st.sidebar.divider()
    st.sidebar.write("**Autor:** Julio Molinares")
    st.sidebar.write("**Curso:** Talento Tech")

    st.title("📊 Dashboard Analítico: Salud Mental")
    
    # Pestañas de organización
    tab_graficos, tab_sql, tab_docs = st.tabs(["📈 Análisis Visual", "💻 Consultas SQL", "📖 Documentación"])

    with tab_graficos:
        st.header("Visualización de Factores Críticos")
        
        # Gráfico 1: Sueño vs Depresión
        st.subheader("1. Calidad de Sueño y Puntuación PHQ-9 (Depresión)")
        col_g1, col_h1 = st.columns([3, 1])
        
        with col_g1:
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            # Columnas probables: Sleep_Duration, PHQ_9_Score
            sns.boxplot(data=df, x='Sleep_Duration', y='PHQ_9_Score', ax=ax1, palette="vlag")
            ax1.set_title("Distribución de Depresión según Horas de Sueño")
            st.pyplot(fig1)
            
        with col_h1:
            with st.popover("❓ Ayuda Analítica"):
                st.markdown("""
                **Interpretación:**
                Este diagrama de cajas (*boxplot*) permite observar si existe una tendencia de mayores puntajes de depresión 
                en estudiantes con privación de sueño. Los puntos fuera de los bigotes representan casos atípicos.
                """)

        st.divider()

        # Gráfico 2: Ansiedad por Género
        st.subheader("2. Distribución de Ansiedad (GAD-7) por Género")
        col_g2, col_h2 = st.columns([3, 1])
        
        with col_g2:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.violinplot(data=df, x='Gender', y='GAD_7_Score', ax=ax2, inner="quart", palette="pastel")
            ax2.set_title("Densidad de Ansiedad por Identidad de Género")
            st.pyplot(fig2)
            
        with col_h2:
            with st.popover("❓ Ayuda Analítica"):
                st.markdown("""
                **Interpretación:**
                El gráfico de violín combina un diagrama de cajas con la densidad de Kernel. Nos permite ver 
                dónde se concentra la mayoría de los estudiantes y comparar la variabilidad entre géneros.
                """)

    with tab_sql:
        st.header("Consola de Consultas Relacionales")
        st.markdown("""
        Ejecuta consultas directas sobre la tabla `salud_mental`. 
        *Ejemplo: `SELECT Gender, AVG(PHQ_9_Score) FROM salud_mental GROUP BY Gender`*
        """)
        
        query_input = st.text_area("Consulta SQL:", value="SELECT Gender, COUNT(*) as Total FROM salud_mental GROUP BY Gender")
        
        if st.button("Ejecutar Query ⚡"):
            try:
                res_df = pd.read_sql_query(query_input, conn)
                st.success("Consulta exitosa")
                st.dataframe(res_df, use_container_width=True)
            except Exception as e:
                st.error(f"Error en la sintaxis SQL: {e}")

    with tab_docs:
        st.header("Documentación del Proyecto")
        st.markdown(f"""
        ### Ficha Técnica
        * **Dataset:** Medical Student Mental Health.
        * **Registros:** {len(df)} estudiantes evaluados.
        * **Escalas:** PHQ-9 (Depresión), GAD-7 (Ansiedad).
        
        ### Modelo de Datos
        Se ha implementado un motor **SQLite en memoria** que permite realizar operaciones de agregación y filtrado 
        de manera eficiente. Los datos originales han sido normalizados para cumplir con los estándares de 
        análisis relacional.
        
        ### Fórmulas Aplicadas
        Promedio de Score:
        $$ \\bar{{X}} = \\frac{{\\sum_{{i=1}}^{{n}} x_i}}{{n}} $$
        
        ---
        **Desarrollado por:** Julio Molinares  
        **Entregable:** Nivel Integrador - Talento Tech
        """)

# Pie de página
st.markdown("---")
st.caption("Julio Molinares | Analista de Datos | Talento Tech 2026")
