import pandas as pd
import plotly.express as px
import streamlit as st

## Configuración de página
st.set_page_config(page_title = "🌳 Dashboard sustentabilidad", 
                   page_icon = "🌍", 
                   layout = "wide")

## CSS personalizado para mejorar la apariencia
st.markdown("""
    <style>
    /* Títulos principales */
    h1 {
        color: #2d5016;
        text-align: center;
        font-size: 3em;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
    }

    /* Estilo de las métricas */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html = True)

## Título
st.markdown("<h1> 🌳 Dashboard de superficie forestal en México</h1>",
            unsafe_allow_html = True)

## Carga de datos
data = pd.read_csv("red_forestal.csv")

## Extraemos los estados
estados = data["Entidad"].unique()

## Extraemos los años
years = data["Anio"].unique()

## Sidebar para seleccionar estados y años
st.sidebar.header("🔍 Filtros")
anio_seleccionado = st.sidebar.multiselect(
    "Selecciona el año:",
    years,
    default = years)
estado_seleccionado = st.sidebar.multiselect(
    "Selecciona el estado:",
    estados,
    default = estados)

## Filtramos los datos
df_filtrado = data[data["Entidad"].isin(estado_seleccionado)]
df_filtrado = df_filtrado[df_filtrado["Anio"].isin(anio_seleccionado)]
df_filtrado_anual = df_filtrado.groupby(["Entidad", "Anio"])["Superficie_ha"].agg("sum").reset_index()

## Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌱 Superficie forestal total (ha)", 
              f"{round(df_filtrado["Superficie_ha"].sum(), 2):,}")

with col2:
    st.metric("🌿 Superficie forestal promedio (ha)", 
              f"{round(df_filtrado["Superficie_ha"].mean(), 2):,}")

with col3:
    st.metric("📍 Regiones Activas", 
              len(df_filtrado["Entidad"].unique()))

## Gráficos
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(df_filtrado,
                  x = "Entidad", 
                  y = "Superficie_ha",
                  title = "🌳 Superficie forestal por entidad",
                  color = "Superficie_ha",
                  color_continuous_scale = "Greens",
                  hover_data = ["Municipio", "Superficie_ha", "Anio"],
                  template = "plotly_white")
    fig1.update_layout(xaxis_title = "Entidad federativa",
                       yaxis_title = "Superficie forestal (ha)")
    st.plotly_chart(fig1, width = "stretch")

with col2:
    fig2 = px.line(df_filtrado_anual,
                   x = "Anio", 
                   y = "Superficie_ha",
                   title = "🌳 Superficie forestal anual",
                   color = "Entidad",
                   template = "plotly_white")
    fig2.update_layout(xaxis_title = "Año",
                       yaxis_title = "Superficie forestal (ha)",
                       xaxis = dict(tickvals = anio_seleccionado))
    st.plotly_chart(fig2, width = "stretch")

## Gráfica de violín
fig3 = px.violin(df_filtrado,
                 y = "Superficie_ha",
                 title = "🌳 Distribución de la superficie forestal",
                 color = "Entidad",
                 template = "plotly_white")
fig3.update_layout(xaxis_title = "Entidad",
                   yaxis_title = "Superficie forestal (ha)")
st.plotly_chart(fig3, width = "stretch")

## Tabla de datos
st.markdown("### 📋 Datos Detallados")
st.dataframe(df_filtrado, width = "stretch")
