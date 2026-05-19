#| file: code/pyqgis/car.py
# Clase padre (superclase)
# Esta clase define atributos y comportamientos comunes para todos los carros
class Car: 
    
    # Variables de clase (compartidas por todas las instancias en la memoria de la clase)
    model = 'Civic'
    features = []  # Objeto mutable (lista) compartido colectivamente
    
    # Constructor: se ejecuta al crear un objeto de la clase
    def __init__(self, color, type):
        # Variables de instancia (propias y aisladas para cada objeto en particular)
        self.color = color
        self.type = type
        self.started = False
        self.stopped = False
        
    # Método especial para personalizar la representación del objeto en texto (print)
    def __str__(self):
        # Identificación dinámica del tipo de clase (Car, Sedan o ElectricSedan)
        class_name = self.__class__.__name__
        msg = f"[{class_name}] Modelo base: {self.model} | Color: {self.color} | Transmisión: {self.type}"
        
        # Inclusión condicional de atributos si la instancia pertenece a una subclase
        if hasattr(self, 'seats'):
            msg += f" | Capacidad: {self.seats} puestos"
        if hasattr(self, 'range_km'):
            msg += f" | Autonomía: {self.range_km} km"
            
        return msg
    
    # Método para encender el carro
    def start(self):
        print('Car Started')
        self.started = True
        self.stopped = False
        
    # Método para apagar el carro
    def stop(self):
        print('Car Stopped')
        self.stopped = True
        self.started = False 


# -------------------------
# 1. Instanciar la clase base (Car)
# -------------------------
print('1. Instanciar una clase: Car')

# Crear un objeto (instancia) de la clase Car
my_car = Car('blue', 'automatic')

# Ahora imprimirá el mensaje personalizado definido en __str__
print(my_car)

# Llamar a un método de la clase
my_car.start()

# Consultar una variable de instancia
print('Car Started?', my_car.started)

# Consultar una variable de clase
print('Car model', Car.model)


# -------------------------
# HERENCIA
# -------------------------

# Clase hija (subclase) que hereda de Car
# Sedan ES UN tipo de Car (relación "es-un")
class Sedan(Car):
        
    def __init__(self, color, type, seats):
        # Llamamos al constructor de la clase padre (Car)
        super().__init__(color, type)
        
        # Atributo adicional propio de Sedan
        self.seats = seats
        

# Clase hija de Sedan (y nieta de Car)
# ElectricSedan hereda todo de Sedan y Car
class ElectricSedan(Sedan):

    def __init__(self, color, type, seats, range_km):
        # Llamamos al constructor de Sedan (que a su vez llama a Car)
        super().__init__(color, type, seats)
        
        # Atributo adicional propio de autos eléctricos
        self.range_km = range_km


# -------------------------
# 2. Instanciar una subclase (Sedan)
# -------------------------
print('\n2. Instanciar una clase que hereda de otra: Sedan <- Car')

# Crear un objeto de Sedan
my_sedan = Sedan('blue', 'automatic', 5)

# Imprime el mensaje heredado y adaptado automáticamente para Sedan
print(my_sedan)

# Método heredado de Car
my_sedan.start()


# -------------------------
# 3. Herencia multinivel
# ElectricSedan <- Sedan <- Car
# -------------------------
print('\n3. Instanciar una clase que hereda de otra y esta a su vez hereda de otra: ElectricSedan <- Sedan <- Car')

# Crear un objeto de ElectricSedan
my_future_car = ElectricSedan('red', 'automatic', 5, 500)

# Imprime el mensaje heredado y adaptado con los datos de autonomía de ElectricSedan
print(my_future_car)

# Método heredado de Car
my_future_car.start()


# -------------------------
# 4. Demostración del alcance de variables de clase e instancia
# -------------------------
print('\n4. Demostración de variables de clase (Alcance y mutabilidad)')

# Instanciación de dos objetos independientes
car_a = Car('black', 'manual')
car_b = Car('white', 'automatic')

# Caso A: Intento de modificación de variable inmutable (str) vía instancia
car_a.model = 'Corolla'  # Crea una variable de instancia "sombra" local para car_a
print(f"Modelo car_a: {car_a.model}")  # Imprime 'Corolla' (desde la instancia)
print(f"Modelo car_b: {car_b.model}")  # Imprime 'Civic' (desde la clase)
print(f"Modelo Clase Car: {Car.model}")  # Imprime 'Civic' (la clase no mutó)

# Caso B: Modificación global directa sobre la clase base
Car.model = 'Accord'
print(f"Nuevo modelo car_b: {car_b.model}")  # Refleja 'Accord' (apunta al espacio de la clase)

# Caso C: Modificación de un objeto mutable (list) desde una instancia específica
car_a.features.append('Sunroof')  # Altera directamente la lista compartida en memoria
print(f"Atributos compartidos en car_b: {car_b.features}")  # Refleja ['Sunroof']