import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import kagglehub
import os
from datetime import datetime

# Configuración profesional de la página
st.set_page_config(
    page_title="Análisis COVID-19 Perú - Julio Molinares",
    page_icon="📊",
    layout="wide"
)

# Configuración estética de Seaborn
sns.set_theme(style="whitegrid", palette="viridis")

# Función para la descarga y limpieza de datos
@st.cache_data
def load_data():
    try:
        # Descarga automática desde Kagglehub
        path = kagglehub.dataset_download("martinclark/peru-covid19-august-2020")
        
        # Identificar el archivo CSV en el directorio descargado
        files = os.listdir(path)
        csv_file = [f for f in files if f.endswith('.csv')][0]
        full_path = os.path.join(path, csv_file)
        
        df = pd.read_csv(full_path)
        
        # Pre-procesamiento de fechas si la columna existe
        if 'FECHA_RESULTADO' in df.columns:
            df['FECHA_RESULTADO'] = pd.to_datetime(df['FECHA_RESULTADO'], format='%Y%m%d', errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos desde Kaggle: {e}")
        return pd.DataFrame()

# --- GESTIÓN DE NAVEGACIÓN (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def set_page(page_name):
    st.session_state.page = page_name

# --- LANDING PAGE (Página de Inicio) ---
if st.session_state.page == 'landing':
    st.title("🛡️ Análisis Epidemiológico: Perú 2020")
    st.subheader("Curso de Análisis de Datos - Nivel Integrador | Taleen Tech")
    
    col_text, col_img = st.columns([1, 1])
    
    with col_text:
        st.markdown("""
        ### Introducción al Dataset
        Este conjunto de datos recopila información crítica sobre la propagación del COVID-19 en el territorio peruano. 
        A través de este panel, exploraremos:
        
        * **Distribución Geográfica:** Identificación de las zonas de mayor incidencia.
        * **Análisis Temporal:** Evolución de los contagios durante los meses críticos.
        * **Métricas Demográficas:** Comprensión de los grupos más afectados.
        
        **Objetivo del Proyecto:** Aplicar técnicas de limpieza, manipulación y visualización de datos para generar insights de valor sobre la emergencia sanitaria.
        """)
        st.button("Ingresar al Panel de Trabajo 🚀", on_click=lambda: set_page('dashboard'), use_container_width=True)
    
    with col_img:
        st.image("https://images.unsplash.com/photo-1584483766114-2cea6facdf57?auto=format&fit=crop&q=80&w=800", 
                 caption="Respuesta sanitaria y análisis de datos en tiempo real")

    st.divider()
    st.info("Proyecto Final realizado por: **Julio Molinares**")

# --- DASHBOARD (Panel de Análisis) ---
else:
    # Barra lateral (Sidebar)
    st.sidebar.image("https://images.unsplash.com/photo-1576086213369-97a306d36557?auto=format&fit=crop&q=80&w=200")
    st.sidebar.title("Menú Principal")
    if st.sidebar.button("🏠 Volver al Inicio"):
        set_page('landing')
    
    st.sidebar.divider()
    st.sidebar.markdown("### Desarrollado por:")
    st.sidebar.write("Julio Molinares")
    
    # Carga de datos con indicador de progreso
    with st.spinner("Conectando con Kaggle y procesando datos..."):
        df = load_data()

    if not df.empty:
        st.title("📈 Panel de Trabajo: Análisis Integrador")
        
        # Organización por pestañas para mejor experiencia de usuario
        tab_viz, tab_data, tab_docs = st.tabs(["📊 Visualizaciones", "🔍 Datos Crudos", "📖 Documentación"])

        with tab_viz:
            st.header("Exploración Estadística Visual")
            
            # Gráfico 1: Análisis Regional
            st.subheader("1. Casos Positivos por Departamento")
            col_plot1, col_help1 = st.columns([3, 1])
            
            with col_plot1:
                if 'DEPARTAMENTO' in df.columns:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    top_depts = df['DEPARTAMENTO'].value_counts().head(12)
                    sns.barplot(x=top_depts.values, y=top_depts.index, ax=ax, palette="mako")
                    ax.set_title("Top 12 Departamentos con Mayor Incidencia")
                    st.pyplot(fig)
                else:
                    st.warning("No se encontró la columna 'DEPARTAMENTO'.")
            
            with col_help1:
                with st.popover("💡 Ayuda: Análisis Regional"):
                    st.markdown("""
                    **¿Qué vemos aquí?**
                    Este gráfico de barras muestra la frecuencia absoluta de casos positivos registrados por departamento. 
                    Ayuda a identificar la descentralización de la pandemia hacia el interior del país.
                    """)

            st.divider()

            # Gráfico 2: Serie de Tiempo
            st.subheader("2. Evolución Cronológica de Contagios")
            col_plot2, col_help2 = st.columns([3, 1])
            
            with col_plot2:
                if 'FECHA_RESULTADO' in df.columns:
                    time_series = df.groupby('FECHA_RESULTADO').size().reset_index(name='CASOS')
                    fig2, ax2 = plt.subplots(figsize=(10, 5))
                    sns.lineplot(data=time_series, x='FECHA_RESULTADO', y='CASOS', ax=ax2, color='#e74c3c', linewidth=2)
                    plt.xticks(rotation=45)
                    ax2.set_title("Curva Epidemiológica (Marzo - Agosto 2020)")
                    st.pyplot(fig2)
                else:
                    st.warning("No hay datos de fecha disponibles para el gráfico temporal.")

            with col_help2:
                with st.popover("💡 Ayuda: Tendencia"):
                    st.markdown("""
                    **¿Qué vemos aquí?**
                    La línea de tiempo permite observar los picos máximos de contagio diario. Las fluctuaciones pueden 
                    deberse a la capacidad de procesamiento de pruebas de cada laboratorio regional.
                    """)

        with tab_data:
            st.header("Inspección de Datos")
            st.write("Vista previa de los primeros 50 registros:")
            st.dataframe(df.head(50), use_container_width=True)
            
            st.markdown("### Estadísticas Descriptivas")
            st.write(df.describe(include='all'))

        with tab_docs:
            st.header("Documentación del Proyecto")
            st.markdown(f"""
            ### Detalles de la Implementación
            Este panel fue construido utilizando herramientas de código abierto líderes en la industria del análisis de datos.
            
            * **Fuente:** Dataset de Martin Clark hospedado en Kaggle.
            * **Bibliotecas:**
                * `Pandas`: Manipulación y limpieza de estructuras de datos.
                * `Seaborn`: Visualización estadística de alta fidelidad.
                * `Streamlit`: Despliegue de la interfaz de usuario.
            
            ### Indicadores Clave
            El análisis se centra en la frecuencia de casos y la temporalidad, aplicando la siguiente lógica para la tasa de crecimiento:
            
            $$ \\text{{Crecimiento}} = \\frac{{\\text{{Casos actual}} - \\text{{Casos anterior}}}}{{\\text{{Casos anterior}}}} $$
            
            **Estudiante:** Julio Molinares  
            **Programa:** Análisis de Datos - Nivel Integrador
            """)

    else:
        st.error("Error crítico: No se ha podido establecer la conexión con el dataset.")

# Pie de página constante
st.markdown("---")
st.caption("© 2024 Proyecto Integrador Taleen Tech | Desarrollado por Julio Molinares")
