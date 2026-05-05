#| eval: false

# -------------------------
# Importación de dependencias
# -------------------------

# os: Gestión de rutas de archivos con independencia del sistema operativo
import os

# qgis.core: Acceso al singleton del proyecto activo
from qgis.core import QgsProject

# PyQt5.QtWidgets: Componentes de la interfaz gráfica (labels y cuadros combinados)
from PyQt5.QtWidgets import QLabel, QComboBox


# -------------------------
# Validación de precondición de persistencia
# -------------------------

# Recuperación de la ruta absoluta del archivo de proyecto actual
# El método fileName() devuelve una cadena vacía si el proyecto no ha sido guardado
project_full_path = QgsProject.instance().fileName()

# Estructura de control para gestionar la salida temprana (Early Exit)
if not project_full_path:
    # Notificación de error crítico en la barra de mensajes de la interfaz (iface)
    # Impide que el script intente referenciar directorios locales inexistentes
    iface.messageBar().pushCritical(
        'Error de ejecución', 
        'Operación cancelada: El proyecto actual debe estar guardado para establecer el directorio raíz.'
    )

else:
    # -------------------------
    # Configuración de rutas y UI
    # -------------------------
    
    # Extracción del directorio base del proyecto activo mediante os.path.dirname
    project_dir = os.path.dirname(project_full_path)
    data_dir = project_dir

    # Creación de una nueva barra de herramientas en la ventana principal de QGIS
    projectToolbar = iface.addToolBar('Project Selector')

    # Instanciación de etiquetas y selectores
    # El parámetro 'parent' vincula la jerarquía del widget a la barra de herramientas
    label = QLabel('Seleccione un proyecto para cargar:', parent=projectToolbar)
    
    projectSelector = QComboBox(parent=projectToolbar)
    projectSelector.addItem('sf.qgz')
    projectSelector.addItem('places.qgz')
    
    # Inicialización del índice en -1 para evitar la carga automática al instanciar
    projectSelector.setCurrentIndex(-1)


    # -------------------------
    # Lógica de carga de proyectos
    # -------------------------

    def loadProject(projectName):
        """
        Lee y carga un archivo de proyecto específico desde el directorio de datos.
        Advertencia: Este método reemplaza la sesión actual en el canvas.
        """
        project = QgsProject.instance()
        
        # Construcción de la ruta absoluta del recurso seleccionado
        project_path = os.path.join(data_dir, projectName)
        
        # Validación opcional: verificar existencia física antes de la lectura
        if os.path.exists(project_path):
            project.read(project_path)
            iface.messageBar().pushInfo('Carga exitosa', f'Proyecto cargado: {projectName}')
        else:
            iface.messageBar().pushWarning('Archivo no encontrado', f'No se halló: {projectName}')


    # -------------------------
    # Conexión de eventos e integración
    # -------------------------

    # Mecanismo de señales y slots: se vincula el cambio de texto con la función de carga
    projectSelector.currentTextChanged.connect(loadProject)

    # Inyección de widgets en la barra de herramientas personalizada
    projectToolbar.addWidget(label)
    projectToolbar.addWidget(projectSelector)