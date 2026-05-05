#| file: code/pyqgis/save_attributes_algorithm.py
#| eval: false

# -------------------------
# Importación de dependencias
# -------------------------
from PyQt5.QtCore import QCoreApplication
from qgis.core import (Qgis,
                       QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination,
                       QgsVectorFileWriter,
                       QgsWkbTypes,
                       QgsProject)

class SaveAttributesAlgorithm(QgsProcessingAlgorithm):
    """
    Extensión del framework de procesamiento para persistir atributos vectoriales
    en formato plano CSV sin componentes geométricos.
    """

    def initAlgorithm(self, config=None):
        """
        Definición de la interfaz de entrada y salida del algoritmo.
        Se configuran los parámetros que el usuario visualizará en el diálogo.
        """
        # Parámetro de entrada: Fuente de objetos espaciales (Capa vectorial)
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                'INPUT',
                'Input layer',
                [Qgis.ProcessingSourceType.VectorAnyGeometry]
            )
        )

        # Parámetro de salida: Destino del archivo CSV
        # QgsProcessingParameterFileDestination gestiona la creación de rutas en el SO
        self.addParameter(
            QgsProcessingParameterFileDestination(
                'OUTPUT',
                'Output File',
                'CSV files (*.csv)',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Núcleo operativo del algoritmo donde se ejecuta la lógica de procesamiento.
        
        Args:
            parameters: Diccionario con los valores proporcionados por el usuario.
            context: Contexto de ejecución del framework de procesamiento.
            feedback: Objeto para reportar progreso y gestionar cancelaciones.
        """
        # Recuperación de la capa vectorial desde el parámetro de entrada
        layer = self.parameterAsVectorLayer(parameters, 'INPUT', context)

        # Recuperación de la ruta de salida definida por el usuario
        output = self.parameterAsFileOutput(parameters, 'OUTPUT', context)

        # Configuración del iterador y conteo para la barra de progreso
        total = layer.featureCount()
        features = layer.getFeatures()
        
        # Definición de opciones técnicas para el escritor de archivos
        # Se utiliza el controlador de CSV de OGR/GDAL
        save_options = QgsVectorFileWriter.SaveVectorOptions()
        save_options.driverName = 'CSV'
        save_options.fileEncoding = 'UTF-8'

        # Inicialización del objeto escritor (Writer)
        # Se define QgsWkbTypes.NoGeometry para omitir la exportación de vértices
        writer = QgsVectorFileWriter.create(
            fileName=output,
            fields=layer.fields(),
            geometryType=QgsWkbTypes.NoGeometry,
            srs=layer.crs(),
            transformContext=QgsProject.instance().transformContext(),
            options=save_options)

        # Ciclo de iteración sobre los objetos espaciales de la capa
        for current, f in enumerate(features):
            # Verificación de interrupción por parte del usuario
            if feedback.isCanceled():
                break

            # Inserción de la entidad en el archivo de salida
            writer.addFeature(f)

            # Actualización dinámica de la barra de progreso en la interfaz
            if total != 0:
                # Cálculo porcentual del avance del proceso
                progress = int(100 * (current / total))
            else:
                progress = 0
            feedback.setProgress(progress)

        # Retorno de los resultados para su integración en modelos o scripts superiores
        return {'OUTPUT': output}

    def name(self):
        """Identificador interno del algoritmo (minúsculas, sin espacios)."""
        return 'save_attributes'

    def displayName(self):
        """Nombre legible que aparecerá en la caja de herramientas."""
        return self.tr('Save Attributes As CSV')

    def group(self):
        """Categoría o grupo de algoritmos al que pertenece."""
        return self.tr(self.groupId())

    def groupId(self):
        """Identificador único del grupo."""
        return ''

    def tr(self, string):
        """Soporte para la internacionalización de cadenas de texto."""
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        """Generación de una nueva instancia de la clase del algoritmo."""
        return SaveAttributesAlgorithm()