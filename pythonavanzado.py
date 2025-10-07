import itertools
import string
import tkinter as tk
from tkinter import messagebox, scrolledtext


# --- LÓGICA DE GENERACIÓN DE CONTRASEÑAS (Misma función mejorada) ---
def generar_contraseñas_logica(nombre, dni):
    """
    Genera una lista de contraseñas potenciales a partir de un nombre y DNI.
    """
    contraseñas = set()
   
    # Normalización de entradas
    nombre_limpio = nombre.lower().replace(" ", "")
    dni_str = ''.join(filter(str.isalnum, str(dni)))
    nombre_mayus = nombre.capitalize().replace(" ", "")

    if not nombre_limpio or not dni_str:
        return []

    # 1. Contraseñas básicas (Nombre y DNI en diferentes combinaciones)
    combinaciones_basicas = [
        nombre_limpio,
        dni_str,
        nombre_limpio + dni_str,
        dni_str + nombre_limpio,
        nombre_mayus + dni_str,
        dni_str + nombre_mayus,
    ]
    contraseñas.update(combinaciones_basicas)

    # 2. Variaciones con substituciones (Leetspeak simple)
    leetspeak_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '1'}
    def aplicar_leetspeak(texto):
        return "".join(leetspeak_map.get(char, char) for char in texto.lower())

    for p in combinaciones_basicas:
        contraseñas.add(aplicar_leetspeak(p))
       
    # 3. Variaciones con números y símbolos comunes al final
    sufijos = ["1", "2", "!", "#", "*"]
    anio_actual = "2024" # Se puede actualizar
   
    for p in combinaciones_basicas:
        contraseñas.add(p + anio_actual)
        contraseñas.add(anio_actual + p)
        for sufijo in sufijos:
            contraseñas.add(p + sufijo)

    # 4. Combinaciones con iniciales
    partes_nombre = nombre.split()
    if len(partes_nombre) > 1:
        iniciales = "".join(p[0] for p in partes_nombre).lower()
        contraseñas.add(iniciales + dni_str)
        contraseñas.add(iniciales.capitalize() + dni_str)
        contraseñas.add(dni_str + iniciales)

    # 5. Combinaciones con fecha de nacimiento (si el DNI es largo, tomamos los últimos 4 dígitos)
    if len(dni_str) >= 4:
        ultimos_cuatro = dni_str[-4:]
        contraseñas.add(nombre_limpio + ultimos_cuatro)
        contraseñas.add(nombre_mayus + ultimos_cuatro)

    # Limpiar y filtrar: eliminar contraseñas muy cortas o vacías
    contraseñas_finales = [p for p in contraseñas if len(p) >= 6]

    return sorted(list(set(contraseñas_finales)))


# --- FUNCIÓN PRINCIPAL DE LA INTERFAZ (Tkinter) ---

def generar_y_mostrar():
    """Obtiene los datos de la interfaz, genera las contraseñas y las muestra."""
    nombre = entry_nombre.get().strip()
    dni = entry_dni.get().strip()

    if not nombre or not dni:
        messagebox.showerror("Error de Entrada", "Por favor, introduce tanto el Nombre como el DNI/ID.")
        return

    # Llamar a la función lógica de generación
    lista_contraseñas = generar_contraseñas_logica(nombre, dni)
   
    # Limpiar el área de texto
    output_text.delete(1.0, tk.END)
   
    if lista_contraseñas:
        # Formatear la salida
        header = f"--- Se generaron {len(lista_contraseñas)} Contraseñas Potenciales ---\n"
        output_text.insert(tk.END, header)
        output_text.insert(tk.END, "--------------------------------------------------------\n")
       
        # Insertar cada contraseña
        for i, p in enumerate(lista_contraseñas):
            output_text.insert(tk.END, f"{i+1:03d}. {p}\n")
       
        output_text.insert(tk.END, "--------------------------------------------------------\n")
        output_text.insert(tk.END, "⚠️ Úsalo de forma ética y legal. ⚠️\n")
       
    else:
        output_text.insert(tk.END, "No se pudieron generar contraseñas válidas. Revisa las entradas.")

# --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---

# Inicializar la ventana
root = tk.Tk()
root.title("🔐 Generador Avanzado de Contraseñas (Py/Tkinter)")
root.geometry("600x600") # Establecer un tamaño inicial
root.resizable(False, False) # Deshabilitar el redimensionamiento

# 1. Marco para las entradas de datos
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(pady=10)

# Etiqueta y campo para el Nombre
label_nombre = tk.Label(input_frame, text="Nombre Completo:", font=('Arial', 10, 'bold'))
label_nombre.grid(row=0, column=0, sticky='w', padx=5, pady=5)
entry_nombre = tk.Entry(input_frame, width=40, font=('Arial', 10))
entry_nombre.grid(row=0, column=1, padx=5, pady=5)

# Etiqueta y campo para el DNI/ID
label_dni = tk.Label(input_frame, text="DNI/ID/Número:", font=('Arial', 10, 'bold'))
label_dni.grid(row=1, column=0, sticky='w', padx=5, pady=5)
entry_dni = tk.Entry(input_frame, width=40, font=('Arial', 10))
entry_dni.grid(row=1, column=1, padx=5, pady=5)

# 2. Botón de Generación
btn_generar = tk.Button(root, text="🚀 GENERAR CONTRASEÑAS 🚀", command=generar_y_mostrar,
                        bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), relief=tk.RAISED)
btn_generar.pack(pady=10, padx=10, fill=tk.X)

# 3. Área de Salida de Contraseñas (ScrolledText para tener scroll)
output_frame = tk.Frame(root)
output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=60, height=20,
                                        font=('Courier New', 10), bg='#f0f0f0')
output_text.pack(fill=tk.BOTH, expand=True)

# Mensaje inicial
output_text.insert(tk.END, "Introduce el Nombre y el DNI/ID, y haz clic en Generar.")

# Iniciar el bucle principal de la interfaz
root.mainloop()