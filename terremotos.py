#Cardona Ramirez Mauricio de jesus 
#ApiRest de Terremotos 
import requests
from tkinter import *
from datetime import datetime

def MostrarDatos():
    # Limpiar el Text widget antes de mostrar nuevos resultados
    result_text.delete(1.0, END)
    
    # URL de la API de Terremotos de USGS
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    # Parámetros para obtener terremotos recientes
    parametros = {
        'format': 'geojson',  # Formato de la respuesta
        'starttime': '2024-10-18',  # Fecha de inicio
        'endtime': '2024-10-19',    # Fecha de fin
        'minmagnitude': 5           # Magnitud mínima
    }

    # Realizar solicitud GET
    response = requests.get(url, params=parametros)

    if response.status_code == 200:
        datos = response.json()

        # Verificar si hay resultados
        if datos['features']:
            # Limitar a mostrar solo los primeros 5 terremotos
            resultado = ""
            for i, terremoto in enumerate(datos['features'][:5]):
                propiedades = terremoto['properties']

                # Datos del terremoto
                magnitud = propiedades['mag']
                lugar = propiedades['place']
                tiempo = datetime.utcfromtimestamp(propiedades['time'] / 1000).strftime('%Y-%m-%d %H:%M:%S UTC')
                detalle = propiedades.get('detail', 'Sin detalles')

                # Agregar el resultado al texto a mostrar
                resultado += f"Terremoto {i+1}:\nMagnitud: {magnitud}\nLugar: {lugar}\nTiempo: {tiempo}\n\n"

            # Insertar el resultado en el Text widget
            result_text.insert(END, resultado)
        else:
            result_text.insert(END, "No se encontraron terremotos en el rango de fechas proporcionado.")
    else:
        result_text.insert(END, "Ocurrió un error al consultar la API.")

#Crear ventana
ventana = Tk()
ventana.resizable(0, 0)
ventana.geometry("400x400")
ventana.title("Terremotos Recientes")
ventana.configure(bg="#2D2D2D")

#Crear botón
boton = Button(ventana, text="Mostrar Terremotos", command=MostrarDatos, font=("Helvetica", 12), bg="#FF5733", fg="white", width=15)
boton.pack(pady=10)

#Título
titulo = Label(ventana, text="Información de Terremotos", font=("Helvetica", 16, "bold"), fg="white", bg="#2D2D2D")
titulo.pack(pady=20)

# Frame para Text y Scrollbar
frame_resultado = Frame(ventana)
frame_resultado.pack(pady=10)

#widget para resultados
result_text = Text(frame_resultado, wrap=WORD, font=("Helvetica", 12), fg="white", bg="#2D2D2D", width=40, height=10)
result_text.pack(side=LEFT, fill=BOTH, expand=True)

#Crear Scrollbar 
scrollbar = Scrollbar(frame_resultado, command=result_text.yview)
scrollbar.pack(side=RIGHT, fill=Y)

result_text.config(yscrollcommand=scrollbar.set)

# Iniciar ventana
ventana.mainloop()
