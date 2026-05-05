#| file: code/pyqgis/basemap_loader_minimal/load_basemap.py
#| eval: false

# -------------------------
# Importación de dependencias
# -------------------------
import os
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

# Obtención de la ruta absoluta del directorio del complemento
# Fundamental para referenciar recursos locales como iconos o metadatos
plugin_dir = os.path.dirname(__file__)

class BasemapLoaderPlugin:
    """
    Clase principal que gestiona el ciclo de vida del complemento Basemap Loader.
    """

    def __init__(self, iface):
        """
        Constructor de la clase.
        
        Args:
            iface: Referencia a la interfaz de QGIS (QgisInterface), proporcionada 
                   automáticamente por el núcleo de la aplicación al cargar el plugin.
        """
        self.iface = iface

    def initGui(self):
        """
        Inicialización de la Interfaz Gráfica de Usuario (GUI).
        Este método se invoca exclusivamente cuando se activa el complemento.
        """
        # Definición de la ruta del recurso gráfico
        icon_path = os.path.join(plugin_dir, 'logo.png')
        
        # QAction: Define una abstracción de comando que puede asociarse a botones o menús
        # Se vincula a la ventana principal para asegurar la jerarquía de widgets en Qt
        self.action = QAction(
            QIcon(icon_path), 
            'Load Basemap', 
            self.iface.mainWindow()
        )
        
        # Inserción de la acción en la barra de herramientas de complementos
        self.iface.addToolBarIcon(self.action)
        
        # Conexión mediante el mecanismo de señales y slots: 
        # Al activar el botón (triggered), se ejecuta el método run()
        self.action.triggered.connect(self.run)
      
    def unload(self):
        """
        Gestión de la descarga del complemento.
        Elimina de forma segura los elementos creados de la memoria y de la UI
        para evitar fugas de recursos o iconos huérfanos.
        """
        self.iface.removeToolBarIcon(self.action)
        del self.action
        
    def run(self):
        """
        Punto de entrada de la lógica operativa del complemento.
        En esta etapa inicial, despliega una notificación informativa en la barra de mensajes.
        """
        self.iface.messageBar().pushMessage('Notificación: Basemap Loader activado con éxito')