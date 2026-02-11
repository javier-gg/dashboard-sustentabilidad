
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="🌳 Dashboard Sustentabilidad", 
                   page_icon="🌳", 
                   layout="wide")

# Título
st.title("🌳 Dashboard de Sustentabilidad Forestal 🌍")
st.markdown("*Monitoreando nuestro impacto ambiental*")

# Sidebar
st.sidebar.header("🔍 Filtros")
mes_seleccionado = st.sidebar.multiselect(
    "Selecciona los meses:",
    ["Enero", "Febrero", "Marzo", "Abril", "Mayo"],
    default=["Enero", "Febrero", "Marzo", "Abril", "Mayo"]
)

# Datos de ejemplo
datos = {
    'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
    'Arboles': [120, 150, 180, 210, 190],
    'CO2_kg': [240, 300, 360, 420, 380],
    'Región': ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
}

df = pd.DataFrame(datos)
df_filtrado = df[df['Mes'].isin(mes_seleccionado)]

# Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌱 Árboles Plantados", 
              f"{df_filtrado['Arboles'].sum():,}",
              delta="+15%")

with col2:
    st.metric("🌿 CO₂ Absorbido (kg)", 
              f"{df_filtrado['CO2_kg'].sum():,}",
              delta="+12%")

with col3:
    st.metric("📍 Regiones Activas", 
              len(df_filtrado),
              delta="5 regiones")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(df_filtrado, x='Mes', y='Arboles',
                  title='🌳 Árboles por Mes',
                  color='Arboles',
                  color_continuous_scale='Greens')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(df_filtrado, values='Arboles', names='Mes',
                  title='📊 Distribución por Mes',
                  color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico de línea
fig3 = px.line(df_filtrado, x='Mes', y='CO2_kg',
               title='📈 Evolución de CO2 Absorbido',
               markers=True)
fig3.update_traces(line_color='darkgreen', line_width=3)
st.plotly_chart(fig3, use_container_width=True)

# Tabla de datos
st.markdown("### 📋 Datos Detallados")
st.dataframe(df_filtrado, use_container_width=True)
