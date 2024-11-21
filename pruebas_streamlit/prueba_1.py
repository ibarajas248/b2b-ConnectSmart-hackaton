import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configurar la página
st.set_page_config(page_title="Distribución Activos y Pasivos", layout="wide")

# Cargar archivo interactivo
uploaded_file = st.file_uploader("Carga un archivo Excel", type=["xlsx"])
if uploaded_file:
    # Leer el archivo subido
    df = pd.read_excel(uploaded_file)

    # Convertir columnas necesarias
    df['Activos Totales'] = pd.to_numeric(df['Activos Totales'], errors='coerce')
    df['Pasivos Totales'] = pd.to_numeric(df['Pasivos Totales'], errors='coerce')

    # Lista de empresas disponibles
    empresas_disponibles = df['Compañía'].dropna().unique()

    # Seleccionar empresas mediante un buscador
    empresas_seleccionadas = st.multiselect(
        "Selecciona las empresas que deseas analizar",
        options=empresas_disponibles,
        default=['Marval S.A.S.', 'Amarilo S A S']
    )

    # Verificar si se han seleccionado empresas
    if empresas_seleccionadas:
        # Filtrar empresas seleccionadas
        empresas_filtradas = df[df['Compañía'].isin(empresas_seleccionadas)]
        empresas_filtradas = empresas_filtradas[['Compañía', 'Activos Totales', 'Pasivos Totales']]

        # Crear gráfico dinámico según la cantidad de empresas seleccionadas
        empresas = empresas_filtradas['Compañía']
        activos = empresas_filtradas['Activos Totales']
        pasivos = empresas_filtradas['Pasivos Totales']

        # Ajustar la altura del gráfico dinámicamente (0.8 altura por empresa)
        altura_grafico = max(4, 0.8 * len(empresas))
        fig, ax = plt.subplots(figsize=(12, altura_grafico))
        ax.barh(empresas, activos, label='Activos', color='blue')
        ax.barh(empresas, pasivos, label='Pasivos', color='red', left=activos)

        ax.set_xlabel('Monto')
        ax.set_title('Distribución de Activos y Pasivos por Compañía')
        ax.legend()

        st.pyplot(fig)
    else:
        st.warning("Por favor, selecciona al menos una empresa para continuar.")
else:
    st.warning("Por favor, sube un archivo Excel para continuar.")
