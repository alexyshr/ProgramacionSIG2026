#| eval: false

# -------------------------
# Importación de dependencias
# -------------------------
import os
import pandas as pd

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


    # Definición del nombre y ruta final del archivo de salida
    output_name = 'output_1.csv'
    output_path = os.path.join(data_dir, output_name)

    # -------------------------
    # Adquisición y validación de la fuente de datos
    # -------------------------

    # Referencia a la capa seleccionada actualmente en la interfaz de QGIS (iface)
    layer = iface.activeLayer()

    # Validación 1: Verificar que exista una capa seleccionada en el panel de capas
    if not layer:
        iface.messageBar().pushMessage(
        'Error crítico', 'Por favor, seleccione una capa en el panel.', level=Qgis.Critical
        )
        
    # Validación 2: Verificar que la capa sea de tipo vectorial (QgsMapLayer.VectorLayer)
    # Este paso es fundamental ya que las capas ráster no poseen una tabla de atributos iterable
    if layer.type() != QgsMapLayer.VectorLayer:
        iface.messageBar().pushMessage(
        'Error de tipo', 'La operación requiere una capa vectorial.', level=Qgis.Critical
        )

    # -------------------------
    # Extracción de metadatos y registros
    # -------------------------

    # Recuperación de la estructura de campos (QgsFields) de la capa
    fields = layer.fields()

    # Generación de la lista de cabeceras mediante comprensión de listas
    # Se extrae únicamente la propiedad .name() de cada objeto QgsField
    fieldnames = [field.name() for field in layer.fields()]

    # Extracción masiva de atributos utilizando el iterador de entidades (getFeatures)
    # Cada elemento de la lista 'data' contiene el vector de atributos de un objeto espacial
    data = [f.attributes() for f in layer.getFeatures()]

    # -------------------------
    # Procesamiento de datos y persistencia
    # -------------------------

    # Instanciación de un DataFrame de Pandas vinculando la matriz de datos con los nombres de campos
    df = pd.DataFrame(data, columns=fieldnames)

    # Exportación física al sistema de archivos
    # Se utiliza index=False para evitar la inclusión de la columna de índices propia de pandas
    df.to_csv(output_path, index=False)

    # Notificación de finalización exitosa en la barra de mensajes de QGIS
    iface.messageBar().pushMessage(
        'Éxito:', 'Archivo de salida escrito en ' + output_path, level=Qgis.Success)