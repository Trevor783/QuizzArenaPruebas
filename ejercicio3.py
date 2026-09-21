import math

# Función proporcionada (sin modificaciones)
def imprimir_informe(figuras):
    for figura in figuras:
        print(
            figura.nombre(),
            round(figura.area(), 2),
            round(figura.perimetro(), 2)
        )


class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def nombre(self):
        return "Rectángulo"

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


class Circulo:
    def __init__(self, radio):
        self.radio = radio

    def nombre(self):
        return "Círculo"

    def area(self):
        return math.pi * (self.radio ** 2)

    def perimetro(self):
        # El perímetro de un círculo corresponde a su circunferencia
        return 2 * math.pi * self.radio


class TrianguloRectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def nombre(self):
        return "Triángulo Rectángulo"

    def area(self):
        return (self.base * self.altura) / 2

    def perimetro(self):
        # Se calcula la hipotenusa usando el Teorema de Pitágoras
        hipotenusa = math.sqrt(self.base ** 2 + self.altura ** 2)
        return self.base + self.altura + hipotenusa


# =====================================================================
# CLASE CUADRADO (Duplicando la menor cantidad de código posible)
# =====================================================================
# Solución: Un cuadrado es geométricamente un caso especial de rectángulo 
# donde el ancho y el alto son iguales (lados iguales). Por lo tanto, 
# heredamos de 'Rectangulo' y reutilizamos sus métodos de área y perímetro.
class Cuadrado(Rectangulo):
    def __init__(self, lado):
        # Reutilizamos el constructor del Rectángulo pasando 'lado' para base y altura
        super().__init__(lado, lado)

    def nombre(self):
        return "Cuadrado"
    
    # Nota: No necesitamos reescribir area() ni perimetro() porque 
    # los hereda directamente de Rectangulo, evitando duplicación de código.


# ==========================================
# BLOQUE DE PRUEBAS
# ==========================================
if __name__ == "__main__":
    # Creamos una lista con diferentes figuras polimórficas
    mis_figuras = [
        Rectangulo(10, 5),
        Circulo(3),
        TrianguloRectangulo(3, 4),
        Cuadrado(4)
    ]

    # Ejecutamos la función original sin modificarla
    imprimir_informe(mis_figuras)