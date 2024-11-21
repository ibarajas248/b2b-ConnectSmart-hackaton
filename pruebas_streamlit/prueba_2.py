import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
import time

# Configurar la página
st.set_page_config(page_title="Distribución Activos y Pasivos", layout="wide")

# URL de la API
url_api = "https://www.datos.gov.co/resource/6cat-2gcs.json"

# Función para cargar todos los datos usando paginación y almacenarlos en caché
@st.cache_data
def cargar_datos_completos(url, limit=1000, anio_corte="2023"):
    # Lista para almacenar todos los registros
    datos_completos = []

    # Paginación
    offset = 0
    while True:
        try:
            # Realizar la solicitud con limit, offset y el filtro para el año de corte
            response = requests.get(url, params={"$limit": limit, "$offset": offset, "a_o_de_corte": anio_corte})

            # Verificar si la respuesta es exitosa
            if response.status_code == 200:
                # Convertir la respuesta JSON en una lista de diccionarios
                datos = response.json()

                # Si no hay más datos, detener la paginación
                if not datos:
                    break

                # Agregar los datos actuales a la lista
                datos_completos.extend(datos)

                # Incrementar el offset para la siguiente página
                offset += limit

                # Pausa breve para evitar sobrecargar la API (si es necesario)
                time.sleep(1)  # Ajusta este valor si es necesario
            else:
                st.warning(f"Error al cargar datos: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            st.warning(f"Error de conexión: {e}")
            break

    # Convertir la lista completa de datos a un DataFrame
    return pd.DataFrame(datos_completos)

# Cargar todos los datos filtrados por el año de corte 2023
df = cargar_datos_completos(url_api, anio_corte="2023")

# Verificar si el DataFrame tiene datos
if not df.empty:
    # Agregar un filtro por código CIIU
    codigo_ciiu = st.selectbox(
        "Selecciona un código CIIU para filtrar las empresas",
        options=df['ciiu'].dropna().unique()
    )
#dddd
    # Filtrar los datos según el código CIIU seleccionado
    df_filtrado = df[df['ciiu'] == codigo_ciiu]

    # Mostrar el DataFrame filtrado
    if not df_filtrado.empty:
        st.write(f"Datos filtrados por el código CIIU: {codigo_ciiu}")
        st.write(df_filtrado)

        # Convertir las columnas necesarias a tipo numérico (eliminando símbolos de monedas y comas)
        df_filtrado['total_activos'] = pd.to_numeric(df_filtrado['total_activos'].replace({'\$': '', ',': ''}, regex=True), errors='coerce')
        df_filtrado['total_pasivos'] = pd.to_numeric(df_filtrado['total_pasivos'].replace({'\$': '', ',': ''}, regex=True), errors='coerce')

        # Lista de empresas disponibles después de filtrar por CIIU
        empresas_disponibles = df_filtrado['raz_n_social'].dropna().unique()

        # Seleccionar empresas mediante un buscador
        empresas_seleccionadas = st.multiselect(
            "Selecciona las empresas que deseas analizar",
            options=empresas_disponibles
        )

        # Verificar si se han seleccionado empresas
        if empresas_seleccionadas:
            # Filtrar empresas seleccionadas
            empresas_filtradas = df_filtrado[df_filtrado['raz_n_social'].isin(empresas_seleccionadas)]
            empresas_filtradas = empresas_filtradas[['raz_n_social', 'total_activos', 'total_pasivos']]

            # Mostrar el DataFrame de las empresas seleccionadas
            st.write("DataFrame de Empresas Seleccionadas:")
            st.write(empresas_filtradas)

            # Crear gráfico dinámico según la cantidad de empresas seleccionadas
            empresas = empresas_filtradas['raz_n_social']
            activos = empresas_filtradas['total_activos']
            pasivos = empresas_filtradas['total_pasivos']

            # Ajustar la altura del gráfico dinámicamente (0.8 altura por empresa)
            altura_grafico = max(4, 0.8 * len(empresas))
            fig, ax = plt.subplots(figsize=(12, altura_grafico))
            ax.barh(empresas, activos, label='Activos', color='blue')
            ax.barh(empresas, pasivos, label='Pasivos', color='red', left=activos)

            ax.set_xlabel('Monto (en millones)')
            ax.set_title('Distribución de Activos y Pasivos por Compañía')
            ax.legend()

            st.pyplot(fig)
        else:
            st.warning("Por favor, selecciona al menos una empresa para continuar.")
    else:
        st.warning(f"No se encontraron datos para el código CIIU: {codigo_ciiu}.")
else:
    st.warning("No se pudieron cargar los datos.")
