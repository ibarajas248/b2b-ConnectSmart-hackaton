import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns



def mostrar_estadisticas():
    image_url = "https://bidig.areandina.edu.co/wp-content/uploads/2023/08/nature-11.png"
    st.image(image_url, caption='', use_container_width=False, width=300)  # Ajustar el tamaño de la imagen

    # Título de la aplicación
    st.title("Análisis de Compañías - Ganancias, Pérdidas y Solvencia")

    # Ruta fija al archivo
    file_path = 'data/emis_construccion.xlsx'  # Ajusta esta ruta según tu ubicación de archivo

    # Verificar si el archivo existe
    if os.path.exists(file_path):
        # Leer el archivo Excel y cargarlo en un DataFrame
        df = pd.read_excel(file_path)

        # Mostrar las primeras filas del DataFrame para ver su estructura
        st.subheader("Vista previa de los datos")
        st.write(df.head(10000))

        # Filtrar las compañías con ganancias (valor positivo en 'Ganancia (Pérdida) Neta')
        df_ganancias = df[df['Ganancia (Pérdida) Neta'] > 0]

        # Ordenar por 'Ganancia (Pérdida) Neta' de mayor a menor y seleccionar las 10 primeras
        df_top_ganancias = df_ganancias.sort_values(by='Ganancia (Pérdida) Neta', ascending=False).head(10)

        # Filtrar las compañías con pérdidas (valor negativo en 'Ganancia (Pérdida) Neta')
        df_perdidas = df[df['Ganancia (Pérdida) Neta'] < 0]

        # Ordenar por 'Ganancia (Pérdida) Neta' de menor a mayor (más pérdidas)
        df_top_perdidas = df_perdidas.sort_values(by='Ganancia (Pérdida) Neta', ascending=True).head(10)

        # Mostrar los resultados
        st.subheader("Top 10 compañías con mayor ganancia")
        st.write(df_top_ganancias[['Compañía', 'Ganancia (Pérdida) Neta']])

        st.subheader("Top 10 compañías con más pérdidas")
        st.write(df_top_perdidas[['Compañía', 'Ganancia (Pérdida) Neta']])

        # Filtrar los 10 primeros registros con mayores activos
        top_10_activos = df.nlargest(10, 'Activos Totales')

        # Omitir el primer registro (más grande)
        top_10_activos_sin_primero = top_10_activos.iloc[1:]

        # Graficar los activos totales (sin el primero)
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Compañía', y='Activos Totales', data=top_10_activos_sin_primero)
        plt.xticks(rotation=90)  # Rotar las etiquetas del eje x si son muy largas
        plt.title('Top 10 Compañías con Mayores Activos Totales (sin el primero)')
        plt.xlabel('Compañía')
        plt.ylabel('Activos Totales')
        plt.tight_layout()

        # Mostrar el gráfico en Streamlit
        st.pyplot(plt)

        # Filtrar las 20 primeras compañías con mayores activos
        top_20_como_df = df.nlargest(20, 'Activos Totales')  # Filtrar las 20 compañías con mayores activos

        # Excluir la primera compañía (la que tiene el mayor valor de activos)
        top_20_como_df_sin_primero = top_20_como_df.iloc[1:]

        # Graficar la relación entre Activos Totales y Ganancia (Pérdida) Neta para las 20 primeras compañías sin la primera
        plt.figure(figsize=(12, 8))  # Aumentar el tamaño del gráfico para más claridad

        # Usar un gráfico de dispersión con un estilo mejorado
        sns.scatterplot(x='Activos Totales',
                        y='Ganancia (Pérdida) Neta',
                        data=top_20_como_df_sin_primero,
                        hue='Compañía',  # Colorear los puntos según la compañía
                        palette='viridis',  # Mejor paleta de colores
                        s=100,  # Tamaño de los puntos
                        edgecolor='black',  # Agregar borde negro a los puntos para más contraste
                        marker='o',  # Usar círculos como puntos
                        legend=None)  # No mostrar leyenda de compañías, ya que puede ser confuso en gráficos grandes

        # Agregar título y etiquetas más detalladas
        plt.title(
            'Relación entre Activos Totales y Ganancia (Pérdida) Neta de las 20 Primeras Compañías (sin la primera)',
            fontsize=16)
        plt.xlabel('Activos Totales', fontsize=14)
        plt.ylabel('Ganancia (Pérdida) Neta', fontsize=14)

        # Mejorar la visualización con ajustes de formato
        plt.tight_layout()

        # Mostrar el gráfico mejorado en Streamlit
        st.pyplot(plt)




    else:
        st.error(f"El archivo no existe en la ruta proporcionada: {file_path}")


if __name__ == "__main__":
    mostrar_estadisticas()
