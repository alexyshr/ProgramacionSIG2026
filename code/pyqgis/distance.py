# Importamos clases del módulo principal de QGIS para trabajar con geometría
from qgis.core import QgsDistanceArea, QgsPointXY


# Definimos coordenadas geográficas (latitud, longitud)
# San Francisco (California, USA)
san_francisco = (37.7749, -122.4194)

# Nueva York (USA)
new_york = (40.661, -73.944)


# Creamos un objeto de la clase QgsDistanceArea
# Este objeto se usa para calcular distancias y áreas sobre la superficie terrestre
d = QgsDistanceArea()

# Definimos el modelo de la Tierra (elipsoide)
# 'WGS84' es el sistema estándar usado por GPS
# Esto permite calcular distancias más precisas (curvatura de la Tierra)
d.setEllipsoid('WGS84')


# -------------------------
# Preparación de coordenadas
# -------------------------

# Desempaquetamos las tuplas en variables separadas
lat1, lon1 = san_francisco
lat2, lon2 = new_york

# IMPORTANTE:
# QgsPointXY usa el orden (X, Y) = (longitud, latitud)
# Esto suele confundir porque normalmente escribimos (lat, lon)
# Aquí debemos invertir el orden

# Creamos el punto para San Francisco
point1 = QgsPointXY(lon1, lat1)

# Creamos el punto para Nueva York
point2 = QgsPointXY(lon2, lat2)


# -------------------------
# Cálculo de distancia
# -------------------------

# measureLine calcula la distancia entre una serie de puntos
# En este caso pasamos una lista con 2 puntos → distancia directa entre ellos
# El resultado se devuelve en METROS
distance = d.measureLine([point1, point2])


# -------------------------
# Resultado
# -------------------------

# Convertimos de metros a kilómetros dividiendo entre 1000
# y lo imprimimos
print(distance / 1000)