import re
import string
import tkinter as tk
from tkinter import messagebox, scrolledtext


# --- LÓGICA DE GENERACIÓN DE CONTRASEÑAS ---
def generar_contraseñas_logica(nombre, apellido, dni, mascota, cp):
    """
    Genera una lista de contraseñas potenciales a partir de los datos validados.
    """
    contraseñas = set()
   
    # Normalización de entradas
    nombre_completo = (nombre + apellido).lower().replace(" ", "")
    # DNI validado como 8 dígitos + 1 letra. La letra se toma de la posición 8 (índice 8).
    dni_str = str(dni).lower()
    dni_num = dni_str[:8]
    dni_letra = dni_str[8:].upper()
    mascota_limpia = mascota.lower().replace(" ", "")
    cp_str = str(cp)

    if not nombre_completo or not dni_str or not mascota_limpia or not cp_str:
        return []

    # Combinaciones fundamentales
    combinaciones_basicas = [
        # Combinaciones primarias (sin modificación)
        nombre_completo,
        dni_str,
        mascota_limpia,
       
        # Nombre + DNI (dígitos y completo)
        nombre_completo + dni_num,
        nombre_completo + dni_str,
       
        # Mascota + DNI (dígitos y completo)
        mascota_limpia + dni_num,
        mascota_limpia + dni_str,
       
        # DNI (dígitos) + CP
        dni_num + cp_str,
    ]
    contraseñas.update(combinaciones_basicas)
   
    # 1. Variaciones con mayúsculas/capitalización
    for p in combinaciones_basicas:
        contraseñas.add(p.capitalize())
       
    # 2. Variaciones con Leetspeak simple (a->@, e->3, i->1, o->0, s->$, l->1)
    leetspeak_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '1'}
    def aplicar_leetspeak(texto):
        return "".join(leetspeak_map.get(char, char) for char in texto.lower())

    for p in combinaciones_basicas:
        contraseñas.add(aplicar_leetspeak(p))
       
    # 3. Sufijos numéricos y especiales comunes
    sufijos = ["1", "!", "2024", "$", "#"]
   
    for p in [nombre_completo, mascota_limpia, dni_num]:
        for sufijo in sufijos:
            contraseñas.add(p + sufijo)
            contraseñas.add(sufijo + p) # Sufijo al inicio
           
    # 4. Combinaciones de mascota con CP y letra del DNI
    contraseñas.add(mascota_limpia + cp_str)
    contraseñas.add(mascota_limpia + dni_letra)
    contraseñas.add(cp_str + dni_letra)
   
    # 5. Combinaciones inversas del DNI
    contraseñas.add(dni_num[::-1] + nombre_completo)
   
    # Limpiar y filtrar
    # Contraseñas finales: deben tener al menos 8 caracteres
    contraseñas_finales = [p for p in contraseñas if len(p) >= 8]

    return sorted(list(set(contraseñas_finales)))


# --- FUNCIÓN PRINCIPAL DE LA INTERFAZ Y VALIDACIÓN ---

def validar_y_generar():
    """Valida los campos, llama a la función de lógica y muestra los resultados."""
    nombre = entry_nombre.get().strip()
    apellido = entry_apellido.get().strip()
    dni = entry_dni.get().strip()
    mascota = entry_mascota.get().strip()
    cp = entry_cp.get().strip()

    # --- 1. VALIDACIONES ESPECÍFICAS ---
   
    # Nombre y Apellido sin números
    if any(char.isdigit() for char in nombre) or any(char.isdigit() for char in apellido):
        messagebox.showerror("Error de Validación", "El Nombre y el Apellido no pueden contener números.")
        return

    # DNI: 8 dígitos + 1 letra obligatoria
    # Usamos r"^\d{8}[A-Za-z]$" para asegurar 8 dígitos seguidos de una única letra.
    if not re.match(r"^\d{8}[A-Za-z]$", dni):
        messagebox.showerror("Error de Validación", "El DNI debe tener **exactamente 8 números** seguidos de **una única letra** (Ej: 12345678A).")
        return
       
    # Mascota y CP deben estar presentes
    if not mascota or not cp:
        messagebox.showerror("Error de Validación", "El Nombre de la Mascota y el Código Postal son obligatorios.")
        return
   
    # --- 2. GENERACIÓN Y MUESTRA ---

    try:
        lista_contraseñas = generar_contraseñas_logica(nombre, apellido, dni, mascota, cp)
    except Exception as e:
        messagebox.showerror("Error Interno", f"Ocurrió un error al generar las contraseñas: {e}")
        return

    # Limpiar y mostrar resultados
    output_text.delete(1.0, tk.END)
   
    if lista_contraseñas:
        header = f"--- Contraseñas Generadas: {len(lista_contraseñas)} ---\n"
        output_text.insert(tk.END, header)
        output_text.insert(tk.END, "--------------------------------------------------------\n")
       
        for i, p in enumerate(lista_contraseñas):
            output_text.insert(tk.END, f"{i+1:03d}. {p}\n")
       
        output_text.insert(tk.END, "--------------------------------------------------------\n")
        output_text.insert(tk.END, "⚠️ Herramienta de auditoría. Úsala de forma responsable. ⚠️\n", 'rojo')
       
    else:
        output_text.insert(tk.END, "No se pudieron generar contraseñas válidas. Revisa las entradas.\n", 'rojo')

# --- CONFIGURACIÓN DE LA INTERFAZ (Rojo y Azul) ---

# Colores
COLOR_FONDO = "#F0F0F0"  # Gris claro (base para contraste)
COLOR_PRIMARIO = "#FF0000" # Rojo Brillante
COLOR_SECUNDARIO = "#0000FF" # Azul Brillante
COLOR_TEXTO_TITULO = "#00008B" # Azul marino para el texto del título

root = tk.Tk()
root.title("ADIVINADOR DE CONTRASEÑAS TREBUJENA")
root.config(bg=COLOR_FONDO)
root.geometry("650x700")
root.resizable(False, False)

# 1. Etiqueta de Título
title_label = tk.Label(root, text="ADIVINADOR DE CONTRASEÑAS TREBUJENA",
                       font=('Arial', 18, 'bold'), fg=COLOR_PRIMARIO, bg=COLOR_FONDO)
title_label.pack(pady=10)
# Subtítulo en azul
subtitle_label = tk.Label(root, text="Herramienta de Auditoría Personal",
                       font=('Arial', 10), fg=COLOR_SECUNDARIO, bg=COLOR_FONDO)
subtitle_label.pack()

# 2. Marco para las entradas de datos
input_frame = tk.Frame(root, bg=COLOR_FONDO, padx=10, pady=5)
input_frame.pack(pady=10)

# Estilo para las etiquetas
label_style = {'font': ('Arial', 11, 'bold'), 'fg': COLOR_SECUNDARIO, 'bg': COLOR_FONDO}
entry_style = {'width': 35, 'font': ('Arial', 11), 'bg': '#FFFFFF', 'fg': '#333333', 'insertbackground': COLOR_PRIMARIO, 'relief': tk.SOLID}

# Campos de entrada
campos = [
    ("Nombre:", "entry_nombre"),
    ("Apellido:", "entry_apellido"),
    ("DNI (8 Núm. + 1 Letra):", "entry_dni"),
    ("Nombre de Mascota:", "entry_mascota"),
    ("Código Postal:", "entry_cp")
]

# Crear las etiquetas y campos dinámicamente
for i, (texto, var_name) in enumerate(campos):
    label = tk.Label(input_frame, text=texto, **label_style)
    label.grid(row=i, column=0, sticky='w', padx=5, pady=5)
   
    entry = tk.Entry(input_frame, **entry_style)
    entry.grid(row=i, column=1, padx=5, pady=5)
   
    # Asignar la referencia a la variable global (necesario para la función validar_y_generar)
    globals()[var_name] = entry


# 3. Botón de Generación
btn_generar = tk.Button(root, text="🔓 INICIAR ADIVINACIÓN 🔓", command=validar_y_generar,
                        bg=COLOR_PRIMARIO, fg=COLOR_TEXTO_TITULO,
                        font=('Arial', 14, 'bold'), relief=tk.RAISED, activebackground='#CC0000', bd=3)
btn_generar.pack(pady=20, padx=10, fill=tk.X)

# 4. Área de Salida de Contraseñas (ScrolledText)
output_frame = tk.Frame(root, bg=COLOR_FONDO)
output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=65, height=15,
                                        font=('Courier New', 10), bg='#E0E0E0', fg='#333333',
                                        insertbackground=COLOR_PRIMARIO, relief=tk.FLAT)
output_text.pack(fill=tk.BOTH, expand=True)

# Mensaje inicial
output_text.insert(tk.END, "🔵 Introduce todos los datos requeridos y haz clic en Iniciar Adivinación.", 'azul')

# Configurar color del tag para mensajes de error y texto inicial
output_text.tag_config('rojo', foreground=COLOR_PRIMARIO)
output_text.tag_config('azul', foreground=COLOR_SECUNDARIO)


# Iniciar el bucle principal de la interfaz
root.mainloop()