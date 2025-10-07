import itertools
import string


def generar_contraseñas(nombre, dni):
    """
    Genera una lista de contraseñas potenciales a partir de un nombre y DNI.
    """
    contraseñas = set() # Usamos un conjunto (set) para evitar contraseñas duplicadas

    # 1. Contraseñas básicas (Nombre y DNI en diferentes combinaciones)
    nombre_limpio = nombre.lower().replace(" ", "")
    dni_str = str(dni)
    nombre_mayus = nombre.capitalize().replace(" ", "")

    combinaciones_basicas = [
        # Formatos comunes
        nombre_limpio,
        dni_str,
        nombre_limpio + dni_str,
        dni_str + nombre_limpio,
        nombre_mayus + dni_str,
        dni_str + nombre_mayus,
    ]
    contraseñas.update(combinaciones_basicas)

    # 2. Contraseñas con año (asumiendo los primeros 4 dígitos del DNI/ID son relevantes o un año)
    # Se añade un año común (por ejemplo, el año actual o el anterior)
    anio_comun = "2024" # Puedes cambiar esto
    contraseñas.add(nombre_limpio + anio_comun)
    contraseñas.add(nombre_mayus + anio_comun)
    contraseñas.add(dni_str + anio_comun)
    contraseñas.add(anio_comun + nombre_limpio)
   
    # 3. Variaciones con substituciones (Leetspeak simple)
    # Ejemplo: a -> @, e -> 3, i -> 1, o -> 0, s -> $, l -> 1
    leetspeak_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '1'}
   
    def aplicar_leetspeak(texto):
        texto_leet = ""
        for char in texto.lower():
            texto_leet += leetspeak_map.get(char, char)
        return texto_leet

    for p in combinaciones_basicas:
        contraseñas.add(aplicar_leetspeak(p))
       
    # 4. Variaciones con símbolos y números al final (1-9)
    for p in combinaciones_basicas:
        contraseñas.add(p + "1")
        contraseñas.add(p + "!")
        contraseñas.add(p + "#")

    # 5. Combinaciones con las iniciales (si el nombre tiene más de una palabra)
    partes_nombre = nombre.split()
    if len(partes_nombre) > 1:
        iniciales = "".join(p[0] for p in partes_nombre).lower()
        contraseñas.add(iniciales + dni_str)
        contraseñas.add(dni_str + iniciales)
        contraseñas.add(iniciales.capitalize() + dni_str)

    # 6. Combinaciones con fecha de nacimiento (si el DNI es largo, tomamos los últimos 4 dígitos como posible año)
    if len(dni_str) >= 4:
        ultimos_cuatro = dni_str[-4:]
        contraseñas.add(nombre_limpio + ultimos_cuatro)
        contraseñas.add(nombre_mayus + ultimos_cuatro)
        contraseñas.add(ultimos_cuatro + nombre_limpio)

    # Limpiar y filtrar: eliminar contraseñas muy cortas o vacías
    contraseñas_finales = [p for p in contraseñas if len(p) >= 6]

    return sorted(list(set(contraseñas_finales))) # Devolver una lista ordenada y única

# --- Función Principal del Script ---
if __name__ == "__main__":
    print("🤖 Generador de Contraseñas Potenciales 🤖")
    print("-" * 40)
   
    # Solicitar la entrada de datos al usuario
    while True:
        nombre = input("▶️  Introduce el Nombre (Ej: Juan Perez): ").strip()
        if nombre:
            break
        print("El nombre no puede estar vacío.")

    while True:
        dni_input = input("▶️  Introduce el DNI/ID (Solo números o alfanumérico): ").strip()
        # Intentamos obtener solo los números del DNI/ID
        dni_str = ''.join(filter(str.isalnum, dni_input))
        if dni_str:
            break
        print("El DNI/ID no puede estar vacío o solo contener caracteres especiales.")

    print("\nGenerando contraseñas...")
   
    # Llamar a la función generadora
    lista_contraseñas = generar_contraseñas(nombre, dni_str)
   
    # Mostrar resultados
    print("-" * 40)
    print(f"✅ Se generaron {len(lista_contraseñas)} contraseñas potenciales:")
    print("-" * 40)
   
    # Imprimir la lista de contraseñas
    for i, p in enumerate(lista_contraseñas):
        print(f"{i+1:03d}. {p}")
   
    print("-" * 40)
    print("Recuerda usar solo esta herramienta de forma ética y legal. 👮")