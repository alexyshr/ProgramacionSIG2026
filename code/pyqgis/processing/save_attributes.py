# -------------------------
# Importación de dependencias
# -------------------------

# os: Gestión de rutas de archivos y directorios del sistema operativo
import os

# PyQt5: Clases para la construcción de la interfaz gráfica y gestión de acciones
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

# qgis.core: Acceso al núcleo de procesamiento y al registro de la aplicación
from qgis.core import QgsProcessingAlgorithm, QgsApplication

# processing: Interfaz para la ejecución de diálogos y algoritmos del framework
import processing

# Importación relativa del proveedor de algoritmos personalizado
from .save_attributes_provider import SaveAttributesProvider

# Obtención del directorio absoluto del complemento para referenciar recursos
plugin_dir = os.path.dirname(__file__)

class SaveAttributesPlugin:
    """
    Clase controladora encargada de orquestar la integración del complemento
    con el Framework de Procesamiento y la Interfaz de QGIS.
    """

    def __init__(self, iface):
        """
        Constructor de la clase controladora.
        
        Args:
            iface: Instancia de la interfaz de QGIS proporcionada por la factoría.
        """
        self.iface = iface

    def initProcessing(self):
        """
        Sincronización con el registro de procesamiento.
        
        Instancia el proveedor de algoritmos y lo inyecta en el registro global 
        de QGIS, permitiendo que las herramientas aparezcan en la Processing Toolbox.
        """
        self.provider = SaveAttributesProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)
        
    def initGui(self):
        """
        Inicialización de la Interfaz Gráfica de Usuario (GUI).
        
        Configura los puntos de acceso del usuario (menús e iconos) y conecta
        las señales de interacción con la lógica de ejecución.
        """
        # Registro previo del proveedor para asegurar disponibilidad del algoritmo
        self.initProcessing()
        
        # Localización y carga del recurso iconográfico
        icon = os.path.join(plugin_dir, 'logo.png')
        
        # QAction: Define el comportamiento y apariencia del botón del complemento
        self.action = QAction(
            QIcon(icon), 
            'Save Attributes as CSV', 
            self.iface.mainWindow()
        )
        
        # Conexión mediante mecanismo de Signals/Slots: 
        # Al pulsar el botón, se invoca el método run()
        self.action.triggered.connect(self.run)
        
        # Integración de la acción en el menú de complementos y barra de herramientas
        self.iface.addPluginToMenu('&Save Attributes', self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        """
        Gestión de la descarga y limpieza de recursos.
        
        Garantiza la remoción segura del proveedor y los elementos de la interfaz,
        evitando colisiones o fugas de memoria al desactivar el complemento.
        """
        # Remoción del proveedor del registro global
        QgsApplication.processingRegistry().removeProvider(self.provider)
        
        # Limpieza de la interfaz gráfica de usuario
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu('&Save Attributes', self.action)  
        
        # Eliminación de la referencia del objeto de acción
        del self.action

    def run(self):
        """
        Punto de entrada para la ejecución operativa.
        
        Utiliza el framework de procesamiento para desplegar el diálogo de 
        parámetros correspondiente al algoritmo registrado.
        """
        # Ejecución del diálogo estándar de procesamiento basado en el ID del algoritmo
        processing.execAlgorithmDialog('save_attributes:save_attributes')