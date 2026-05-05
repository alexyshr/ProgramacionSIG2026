# -------------------------
# Importación de dependencias
# -------------------------
import os

# PyQt5: Gestión de recursos iconográficos
from PyQt5.QtGui import QIcon

# qgis.core: Clase base para la creación de proveedores de procesamiento
from qgis.core import QgsProcessingProvider

# Importación del algoritmo que será registrado bajo este proveedor
from .save_attributes_algorithm import SaveAttributesAlgorithm

# Determinación del directorio raíz del complemento para la carga de recursos
plugin_dir = os.path.dirname(__file__)

class SaveAttributesProvider(QgsProcessingProvider):
    """
    Clase proveedora que actúa como contenedor y gestor de los algoritmos 
    del complemento Save Attributes dentro del framework de QGIS.
    """

    def __init__(self):
        """
        Constructor de la clase. 
        Inicializa la clase base QgsProcessingProvider.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Gestión de la descarga del proveedor.
        Se invoca al desactivar el complemento para liberar recursos.
        """
        QgsProcessingProvider.unload(self)

    def loadAlgorithms(self):
        """
        Registro de algoritmos individuales.
        
        En este método se instancian y añaden todos los algoritmos que 
        pertenecen a este proveedor mediante el método addAlgorithm().
        """
        self.addAlgorithm(SaveAttributesAlgorithm())

    def id(self):
        """
        Identificador único del proveedor.
        
        Se utiliza internamente para llamar a los algoritmos desde la consola 
        o desde otros scripts (ej: 'save_attributes:nombre_algoritmo').
        """
        return 'save_attributes'

    def name(self):
        """
        Nombre legible para el usuario.
        
        Es el texto que aparecerá como cabecera de grupo en la 
        Processing Toolbox (Caja de herramientas de procesamiento).
        """
        return self.tr('Save Attributes')

    def icon(self):
        """
        Definición del icono del proveedor.
        
        Carga el recurso gráfico que identificará visualmente al grupo 
        de herramientas en la interfaz de QGIS.
        """
        icon_path = os.path.join(plugin_dir, 'logo.png')
        return QIcon(icon_path)

    def longName(self):
        """
        Nombre extendido del proveedor.
        Generalmente coincide con el nombre principal para mantener consistencia.
        """
        return self.name()