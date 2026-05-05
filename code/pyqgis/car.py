# Clase padre (superclase)
# Esta clase define atributos y comportamientos comunes para todos los carros
class Car: 
    
    # Variable de clase (compartida por todas las instancias)
    model = 'Civic'
    
    # Constructor: se ejecuta al crear un objeto de la clase
    def __init__(self, color, type):
        # Variables de instancia (propias de cada objeto)
        self.color = color
        self.type = type
        self.started = False
        self.stopped = False
    
    # Método para encender el carro
    def start(self):
        print('Car Started')
        self.started = True
        self.stopped = False
        
    # Método para apagar el carro
    def stop(self):
        print('Car Stopped')
        self.stopped = True
        self.started = False   # (corregido error: "sefl" -> "self")


# -------------------------
# 1. Instanciar la clase base (Car)
# -------------------------
print('1. Instanciar una clase: Car')

# Crear un objeto (instancia) de la clase Car
my_car = Car('blue', 'automatic')

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
print('2. Instanciar una clase que hereda de otra: Sedan <- Car')

# Crear un objeto de Sedan
my_car = Sedan('blue', 'automatic', 5)

# Accedemos a atributos heredados (de Car)
print(my_car.color)

# Atributo propio de Sedan
print(my_car.seats)

# Método heredado de Car
my_car.start()


# -------------------------
# 3. Herencia multinivel
# ElectricSedan <- Sedan <- Car
# -------------------------
print('3. Instanciar una clase que hereda de otra y esta a su vez hereda de otra: ElectricSedan <- Sedan <- Car')

# Crear un objeto de ElectricSedan
my_future_car = ElectricSedan('red', 'automatic', 5, 500)

# Atributos heredados de Car
print(my_future_car.color)

# Atributos heredados de Sedan
print(my_future_car.seats)

# Atributo propio de ElectricSedan
print(my_future_car.range_km)

# Método heredado de Car
my_future_car.start()