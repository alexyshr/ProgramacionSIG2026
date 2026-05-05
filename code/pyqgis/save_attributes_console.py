#| eval: false

# -------------------------
# Importación de dependencias
# -------------------------
import os
import time

# -------------------------
# Validación de precondición de persistencia
# -------------------------

# Recuperación de la ruta absoluta del archivo de proyecto activo
# El método fileName() es indispensable para anclar los datos al directorio de trabajo
project_full_path = QgsProject.instance().fileName()

# Estructura de control para gestionar la salida temprana (Early Exit)
if not project_full_path:
    # Notificación de error en la interfaz de usuario (iface)
    iface.messageBar().pushCritical(
      'Error de ejecución', 
      'Operación cancelada: El proyecto actual debe estar guardado para establecer el directorio raíz.'
    )

else:
    
    # -------------------------
    # Configuración de rutas e insumos
    # -------------------------
    
    # Establecimiento del directorio base del proyecto
    project_dir = os.path.dirname(project_full_path)
    data_dir = project_dir


    # -------------------------
    # Adquisición y validación de la capa activa
    # -------------------------

    # Referencia al objeto de la capa seleccionada en la interfaz de usuario (iface)
    layer = iface.activeLayer()

    # Validación de existencia: Asegura que el usuario haya seleccionado una capa en el TOC
    if not layer:
        iface.messageBar().pushMessage('Error:', 'Por favor, seleccione una capa', level=Qgis.Critical) 

    # Validación de tipo: El escritor de archivos vectoriales requiere específicamente una QgsVectorLayer
    if layer.type() != QgsMapLayer.VectorLayer:
        iface.messageBar().pushMessage('Error:', 'La capa seleccionada debe ser de tipo vectorial', level=Qgis.Critical)

    # -------------------------
    # Parámetros de configuración del escritor (Writer)
    # -------------------------

    output_name = 'output_2.csv'
    output_path = os.path.join(data_dir, output_name)

    # Instanciación de las opciones de guardado para definir el formato de salida
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = 'CSV'        # Definición del controlador OGR para valores separados por comas
    save_options.fileEncoding = 'UTF-8'    # Codificación de caracteres para asegurar compatibilidad internacional

    # Configuración de opciones específicas de la capa provenientes de GDAL/OGR
    # 'SEPARATOR=COMMA' fuerza el uso de la coma como delimitador, evitando conflictos regionales
    save_options.layerOptions = ['SEPARATOR=COMMA']

    # -------------------------
    # Inicialización del flujo de escritura
    # -------------------------

    # Creación del objeto writer mediante el método factory 'create'
    # Este método inicializa el archivo en disco y prepara el esquema de campos
    writer = QgsVectorFileWriter.create(
        fileName=output_path,
        fields=layer.fields(),                   # Mapeo del esquema de la tabla de atributos original
        geometryType=QgsWkbTypes.NoGeometry,      # Al exportar a CSV, se omite la información geométrica
        srs=layer.crs(),                         # Definición del Sistema de Referencia de Coordenadas
        transformContext=QgsProject.instance().transformContext(), # Gestión del contexto de transformación del proyecto
        options=save_options)

    # Verificación de integridad del escritor
    # Si el archivo está bloqueado o la ruta es inválida, se captura el mensaje de error de la API
    if writer.hasError() != QgsVectorFileWriter.NoError:
        iface.messageBar().pushMessage(
            'Error crítico de escritura:', writer.errorMessage, level=Qgis.Critical)

    # -------------------------
    # Iteración y persistencia de entidades
    # -------------------------

    # Se recorre el iterador de objetos espaciales de la capa fuente
    # Cada entidad (QgsFeature) se envía al búfer del escritor
    for f in layer.getFeatures():
        writer.addFeature(f)

    # -------------------------
    # Finalización y cierre de recursos
    # -------------------------

    # IMPORTANTE: Se debe eliminar explícitamente el objeto writer
    # Esta acción fuerza el vaciado de los búferes (flush) a disco y cierra el manejador del archivo
    del writer

    # Notificación de finalización exitosa en la interfaz de QGIS
    iface.messageBar().pushMessage(
        'Éxito:', 'Archivo exportado correctamente en: ' + output_path, level=Qgis.Success)