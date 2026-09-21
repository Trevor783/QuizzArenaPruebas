from abc import ABC, abstractmethod

# 1. Definimos una interfaz abstracta (Estrategia) para los tipos de descuento
class TipoCliente(ABC):
    @abstractmethod
    def aplicar_descuento(self, precio, cantidad):
        pass


# 2. Implementaciones concretas para cada tipo de cliente existente
class ClienteNormal(TipoCliente):
    def aplicar_descuento(self, precio, cantidad):
        return precio * cantidad


class ClienteVIP(TipoCliente):
    def aplicar_descuento(self, precio, cantidad):
        return precio * cantidad * 0.8  # 20% de descuento


class Empleado(TipoCliente):
    def aplicar_descuento(self, precio, cantidad):
        return precio * cantidad * 0.5  # 50% de descuento


class ClientePremium(TipoCliente):
    def aplicar_descuento(self, precio, cantidad):
        return precio * cantidad * 0.7  # 30% de descuento


# 3. NUEVO TIPO DE CLIENTE: Añadido sin modificar la clase Pedido ni los demás tipos
class ClienteEstudiante(TipoCliente):
    def aplicar_descuento(self, precio, cantidad):
        return precio * cantidad * 0.85  # 15% de descuento


# ==========================================
# 4. CLASE PEDIDO (Lógica principal desacoplada)
# ==========================================
class Pedido:
    def calcular_precio(self, estrategia_descuento, precio, cantidad):
        """
        Calcula el precio final delegando la regla de descuento 
        al objeto 'estrategia_descuento' (Polimorfismo puro).
        """
        if not isinstance(estrategia_descuento, TipoCliente):
            raise TypeError("Se requiere una estrategia de descuento válida.")
        
        return estrategia_descuento.aplicar_descuento(precio, cantidad)


# ==========================================
# BLOQUE DE PRUEBAS Y EJEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    pedido = Pedido()

    precio_unitario = 100.0
    cantidad_items = 2  # Total base: 200.0

    # Instanciamos los diferentes comportamientos de descuento
    normal = ClienteNormal()
    vip = ClienteVIP()
    empleado = Empleado()
    premium = ClientePremium()
    estudiante = ClienteEstudiante()

    print(f"Total Normal: {pedido.calcular_precio(normal, precio_unitario, cantidad_items)}€")       # 200.0
    print(f"Total VIP: {pedido.calcular_precio(vip, precio_unitario, cantidad_items)}€")             # 160.0
    print(f"Total Empleado: {pedido.calcular_precio(empleado, precio_unitario, cantidad_items)}€")   # 100.0
    print(f"Total Premium: {pedido.calcular_precio(premium, precio_unitario, cantidad_items)}€")     # 140.0
    print(f"Total Estudiante: {pedido.calcular_precio(estudiante, precio_unitario, cantidad_items)}€") # 170.0