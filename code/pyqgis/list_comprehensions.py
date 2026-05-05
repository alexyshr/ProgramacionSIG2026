#| eval: false

# -------------------------
# Definición de la fuente de datos
# -------------------------

# Creación de un objeto iterable (lista) con una secuencia de enteros
my_list = [1, 2, 3, 4, 5]


# -------------------------
# Método 1: Flujo mediante bucle for
# -------------------------

# Inicialización de una estructura de datos vacía en la memoria RAM
new_list = []

# Implementación de un ciclo de iteración explícita
for x in my_list:
    # Aplicación de una transformación aritmética (suma)
    # y acumulación secuencial mediante el método .append()
    new_list.append(x + 1)

# Despliegue de la colección resultante: [2, 3, 4, 5, 6]
print(new_list)


# -------------------------
# Método 2: Evaluación declarativa (List Comprehension)
# -------------------------

# La sintaxis de comprensión encapsula la intención del algoritmo en una sola línea.
# [expresión for elemento in iterable]
# Esta construcción es evaluada a nivel del intérprete (C en CPython), lo que suele 
# ofrecer una ventaja de rendimiento sobre el bucle .append() tradicional.
new_list = [x + 1 for x in my_list]

# Verificación de la consistencia de los datos
print(new_list)