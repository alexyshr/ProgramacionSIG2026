#| file: code/pyqgis/basemap_loader_minimal/__init__.py
#| eval: false

# Importación de la lógica definida en el módulo hermano
from .load_basemap import BasemapLoaderPlugin

def classFactory(iface):
    """
    Función de factoría requerida por QGIS.
    
    Constituye el puente entre el gestor de complementos y la clase definida.
    Debe retornar una instancia de la clase principal del complemento.

    Args:
        iface: Instancia de QgisInterface para la manipulación de la aplicación.
    """
    return BasemapLoaderPlugin(iface)