import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Función para mostrar el buscador en la página
def mostrar_estadisticas():
    # Mostrar la nueva imagen de SECOPII con un tamaño reducido
    image_url = "https://blogger.googleusercontent.com/img/a/AVvXsEhWytS90hKcN0Ycn0qDQc9HVPioeV9tISGBDXO3s1_hnhfNHl7AayiN3b7kqoSv12dRMSG-Uoktz1Vwc4aPHz1b3flW-1Mq-P4OXvC2xw2BXUCp5WPG0ZOSSJHjheQcuSEEX_iRT7kCmiEF49iC4NS98vC9rUcWaQnTnyb6j1dDSdW6Gmhnn_JPNm3B"
    st.image(image_url, caption='', use_container_width=False, width=300)  # Ajustar el tamaño de la imagen



    st.write("Filtra y visualiza los registros de la API de datos.gov.co")

    # URL de la API
    json_url = "https://www.datos.gov.co/resource/p6dx-8zbt.json"

    # Input para la búsqueda en el campo 'codigo_principal_de_categoria'
    search_category = st.text_input("Ingrese el código UNSPSC de la categoría (ejemplo, V1.81101500) para filtrar:")

    # Función para obtener los datos de la API y filtrar por codigo_principal_de_categoria
    @st.cache_data
    def fetch_filtered_data(json_url, search_category, limit=1000):
        try:
            # Realizamos la búsqueda por el campo 'codigo_principal_de_categoria'
            query = f"$where=CONTAINS(codigo_principal_de_categoria, '{search_category}')&$limit={limit}"
            response = requests.get(f"{json_url}?{query}")

            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    return df
                else:
                    st.warning("No se encontraron registros con esa categoría adicional.")
                    return pd.DataFrame()
            else:
                st.error("Error al obtener datos de la API.")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
            return pd.DataFrame()

    # Ejecutar búsqueda cuando se ingresa una categoría
    if search_category:
        df = fetch_filtered_data(json_url, search_category)
        if not df.empty:
            st.write(f"Resultados para el código de categoría '{search_category}':")
            st.dataframe(df)

            # Opciones adicionales de filtrado
            st.subheader("Filtrar datos adicionales")
            columnas = df.columns.tolist()



            columna_seleccionada = st.selectbox("Selecciona una columna para filtrar", columnas)


            if columna_seleccionada:
                unique_values = df[columna_seleccionada].unique().tolist()
                valores_seleccionados = st.multiselect(f"Selecciona valores de {columna_seleccionada}", unique_values)
                if valores_seleccionados:
                    df = df[df[columna_seleccionada].isin(valores_seleccionados)]
                    st.dataframe(df)

            # Filtro por rango numérico (para columnas numéricas)
            columnas_numericas = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if columnas_numericas:
                columna_num = st.selectbox("Selecciona una columna numérica para filtrar", columnas_numericas)
                min_value, max_value = st.slider(
                    f"Selecciona el rango para {columna_num}",
                    min_value=float(df[columna_num].min()),
                    max_value=float(df[columna_num].max()),
                    value=(float(df[columna_num].min()), float(df[columna_num].max()))
                )
                df = df[(df[columna_num] >= min_value) & (df[columna_num] <= max_value)]
                st.dataframe(df)

            # Estadísticas descriptivas
            st.subheader("Estadísticas Descriptivas")
            st.write(df.describe())

            # Gráfico de barras horizontal para una variable seleccionada
            st.subheader("Distribución de una variable")
            columna = st.selectbox("Selecciona una columna para ver su distribución", df.columns)

            # Crear el gráfico de barras horizontal
            fig, ax = plt.subplots()
            sns.barplot(y=df[columna].value_counts().index, x=df[columna].value_counts().values, ax=ax, orient='h')

            # Mostrar el gráfico
            st.pyplot(fig)

# Ejecutar la función
if __name__ == "__main__":
    mostrar_estadisticas()
