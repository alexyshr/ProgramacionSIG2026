# -------------------------
# Importación de dependencias y módulos core
# -------------------------

# os: Gestión de rutas y directorios del sistema de archivos
import os

# PyQt5: Componentes para la gestión de acciones y recursos gráficos en la interfaz
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

# qgis.core: Clases fundamentales para el manejo de capas ráster, la gestión del proyecto 
# y la definición de sistemas de referencia de coordenadas (CRS)
from qgis.core import QgsRasterLayer, QgsProject, QgsCoordinateReferenceSystem

# Determinación de la ruta absoluta del directorio del complemento
# Se utiliza para localizar recursos locales (como logo.png) independientemente del SO
plugin_dir = os.path.dirname(__file__)

class BasemapLoaderPlugin:
    """
    Clase principal para la carga automatizada de mapas base (XYZ Tiles).
    Establece la conexión entre la interfaz de usuario y el proveedor de datos ráster.
    """

    def __init__(self, iface):
        """
        Constructor de la clase.
        
        Args:
            iface: Instancia de QgisInterface para interactuar con la ventana principal de QGIS.
        """
        self.iface = iface

    def initGui(self):
        """
        Inicialización de la Interfaz Gráfica (GUI).
        Configura la acción del botón, su icono y su ubicación en la barra de herramientas.
        """
        # Localización del recurso gráfico (formato vectorial o ráster)
        icon_path = os.path.join(plugin_dir, 'logo.png')
        
        # QAction: Define una acción ejecutable vinculada al hilo principal de la aplicación
        self.action = QAction(
            QIcon(icon_path), 
            'Load Basemap', 
            self.iface.mainWindow()
        )
        
        # Inserción del icono en la barra de herramientas de complementos (Plugins Toolbar)
        self.iface.addToolBarIcon(self.action)
        
        # Implementación del paradigma dirigido por eventos (Signals and Slots)
        # La señal 'triggered' ejecuta el método run() al interactuar con el botón
        self.action.triggered.connect(self.run)
      
    def unload(self):
        """
        Gestión de la descarga del complemento.
        Libera los recursos de la UI y elimina la acción de la barra de herramientas 
        para mantener la limpieza del entorno al desactivar el plugin.
        """
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        """
        Lógica de procesamiento principal para la carga de capas XYZ.
        """
        # Configuración de parámetros para el servicio de OpenStreetMap (OSM)
        basemap_url = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
        zmin = 0     # Nivel mínimo de zoom
        zmax = 19    # Nivel máximo de zoom permitido por el servidor de OSM
        crs = 'EPSG:3857' # Sistema de Referencia Pseudo-Mercator utilizado en web maps
        
        # Codificación de caracteres especiales en la URL para asegurar la compatibilidad con la URI
        # Los caracteres '=' y '&' se sustituyen por sus equivalentes en formato de codificación porcentual
        encoded_url = basemap_url.replace('=', '%3D').replace('&', '%26')
        
        # Construcción de la URI de conexión para el proveedor 'wms' (XYZ)
        # Se define el tipo de proveedor, la URL codificada, los límites de zoom y el CRS
        uri = f'type=xyz&url={encoded_url}&zmax={zmax}&zmin={zmin}&crs={crs}'
        
        # Instanciación de la capa ráster mediante el objeto QgsRasterLayer
        # Parámetros: (URI, nombre de la capa en la leyenda, nombre del proveedor 'wms')
        rlayer = QgsRasterLayer(uri, 'OpenStreetMap', 'wms')
        
        # Bloque de validación de integridad de la capa
        if rlayer.isValid():
            # Adición de la capa al registro global del proyecto activo
            QgsProject.instance().addMapLayer(rlayer)
            
            # Notificación visual de éxito en la barra de mensajes superior de QGIS
            self.iface.messageBar().pushSuccess('Éxito', 'Capa de mapa base cargada correctamente')
        else:
            # Reporte de error en caso de fallo en la conexión o URI malformada
            self.iface.messageBar().pushCritical('Error', 'No se pudo cargar la capa: URI inválida')