# -------------------------
# Importación de dependencias
# -------------------------

# Importamos QgsDistanceArea para cálculos geodésicos, QgsPointXY para geometría vectorial 
# y el espacio de nombres Qgis para acceder a las constantes de unidades de medida
from qgis.core import QgsDistanceArea, QgsPointXY, Qgis


# -------------------------
# Definición de parámetros espaciales
# -------------------------

# Coordenadas geográficas en formato tupla (latitud, longitud)
# Punto de origen: San Francisco, CA
san_francisco = (37.7749, -122.4194)

# Punto de destino: New York City, NY
new_york = (40.661, -73.944)


# -------------------------
# Configuración del motor de cálculo
# -------------------------

# Instanciamos la clase QgsDistanceArea para gestionar el análisis espacial
d = QgsDistanceArea()

# Definimos el elipsoide de referencia como WGS84 para habilitar cálculos elipsoidales.
# Esto asegura que la API utilice fórmulas de alta precisión (como Vincenty) 
# en lugar de aproximaciones planas o esféricas
d.setEllipsoid('WGS84')


# -------------------------
# Preparación de datos geométricos
# -------------------------

# Desempaquetado de coordenadas para procesamiento individual
lat1, lon1 = san_francisco
lat2, lon2 = new_york

# NOTA TÉCNICA: QgsPointXY requiere estrictamente el orden (X, Y).
# En sistemas geográficos, esto corresponde a (Longitud, Latitud)
point1 = QgsPointXY(lon1, lat1)
point2 = QgsPointXY(lon2, lat2)


# -------------------------
# Ejecución del análisis geodésico
# -------------------------

# Cálculo de la distancia de la línea geodésica sobre el elipsoide definido.
# El método measureLine recibe una lista de nodos y devuelve el valor escalar en metros
distance = d.measureLine([point1, point2])

# Salida del valor bruto en metros
print('Distance in meters', distance)


# -------------------------
# Gestión y conversión de unidades mediante API
# -------------------------

# En lugar de conversiones aritméticas manuales, se utiliza el método convertLengthMeasurement.
# Este método requiere el valor de entrada y una constante de la enumeración Qgis.DistanceUnit

# Conversión a kilómetros
distance_km = d.convertLengthMeasurement(distance, Qgis.DistanceUnit.Kilometers)
print('Distance in kilometers', distance_km)

# Conversión a millas
distance_mi = d.convertLengthMeasurement(distance, Qgis.DistanceUnit.Miles)
print('Distance in miles', distance_mi)