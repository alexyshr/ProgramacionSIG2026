#| eval: false

# -------------------------
# Importación de dependencias
# -------------------------

# iface: Instancia global que proporciona acceso a la interfaz de usuario (QgisInterface)
from qgis.utils import iface

# QgsExpressionContextUtils: Herramientas para gestionar y acceder a variables de contexto globales, 
# de proyecto o de capa dentro del motor de expresiones de QGIS
from qgis.core import QgsExpressionContextUtils


# -------------------------
# Lógica de personalización
# -------------------------

def customize():
    """
    Función de callback para modificar los atributos visuales de la ventana principal.
    Extrae la versión global del sistema y la concatena al título actual.
    """
    
    # Recuperación de la versión de QGIS desde el ámbito global (Global Scope)
    # Las variables de contexto permiten acceder a metadatos del sistema sin hardcoding
    version = QgsExpressionContextUtils.globalScope().variable('qgis_version')
    
    # Acceso al objeto de la ventana principal (QMainWindow) de Qt
    main_window = iface.mainWindow()
    
    # Captura del título actual definido por el sistema o el proyecto cargado
    current_title = main_window.windowTitle()
    
    # Actualización del título utilizando f-strings para inyectar la versión recuperada
    # La sintaxis de pipe (|) se utiliza como separador visual estándar en interfaces
    main_window.setWindowTitle(f'{current_title} | {version} | UNAL')


# -------------------------
# Registro en el ciclo de vida de QGIS
# -------------------------

# IMPORTANTE: QGIS carga el script startup.py antes de que la interfaz gráfica esté totalmente lista.
# Intentar manipular 'iface' directamente al cargar el script resultaría en un error de tipo 'NoneType'.
# Se utiliza la señal 'initializationCompleted' para diferir la ejecución hasta que la UI sea funcional.
iface.initializationCompleted.connect(customize)
