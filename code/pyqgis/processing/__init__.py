# -------------------------
# Inicialización del módulo
# -------------------------

# Importación de la clase principal desde el archivo de lógica de negocio (save_attributes.py)
# El uso del punto (.) indica una importación relativa dentro del mismo paquete
from .save_attributes import SaveAttributesPlugin

def classFactory(iface):
    """
    Función de factoría requerida por el ecosistema de QGIS.

    Este método es invocado automáticamente por QGIS al cargar el complemento.
    Actúa como constructor global que proporciona al plugin acceso a la interfaz
    de usuario mediante el objeto iface.

    Args:
        iface: Instancia de la clase QgisInterface para la manipulación de la GUI.

    Returns:
        Una instancia de SaveAttributesPlugin que gestiona el ciclo de vida del plugin.
    """
    # Generación y retorno de la instancia de la clase del complemento
    return SaveAttributesPlugin(iface)


