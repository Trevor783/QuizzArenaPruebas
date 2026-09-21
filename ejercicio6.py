class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        # Validaciones de tipos y valores válidos
        if not codigo or not isinstance(codigo, str):
            raise ValueError("El código del producto debe ser un texto válido.")
        if not nombre or not isinstance(nombre, str):
            raise ValueError("El nombre del producto debe ser un texto válido.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if stock < 0:
            raise ValueError("El stock inicial no puede ser negativo.")

        self.codigo = codigo
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)

    @property
    def valor_stock(self):
        # Calcula el valor monetario del stock actual de este producto
        return self.precio * self.stock

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - Precio: {self.precio}€ - Stock: {self.stock}"


class Inventario:
    def __init__(self):
        # CONDICIÓN: La colección interna de productos no debe quedar expuesta directamente.
        # Usamos un diccionario privado (_productos) donde la clave es el código.
        self._productos = {}

    def agregar_producto(self, producto):
        if not isinstance(producto, Producto):
            raise TypeError("El elemento a agregar debe ser una instancia de la clase Producto.")
        
        # CONDICIÓN: Dos productos no pueden tener el mismo código
        if producto.codigo in self._productos:
            raise ValueError(f"Ya existe un producto registrado con el código '{producto.codigo}'.")
        
        self._productos[producto.codigo] = producto

    def eliminar_producto(self, codigo):
        if codigo not in self._productos:
            raise KeyError(f"No se encontró ningún producto con el código '{codigo}'.")
        
        del self._productos[codigo]

    def buscar(self, codigo):
        # Devolvemos el producto si existe, o lanzamos excepción si no se encuentra
        if codigo not in self._productos:
            raise KeyError(f"No se encontró ningún producto con el código '{codigo}'.")
        return self._productos[codigo]

    def vender(self, codigo, cantidad):
        # CONDICIÓN: Cantidad debe ser válida
        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero.")
        
        producto = self.buscar(codigo)
        
        # CONDICIÓN: No puede venderse más stock del disponible
        if cantidad > producto.stock:
            raise ValueError(f"Stock insuficiente. Stock actual disponible: {producto.stock}")
        
        producto.stock -= cantidad

    def reponer(self, codigo, cantidad):
        # CONDICIÓN: Cantidad debe ser válida
        if cantidad <= 0:
            raise ValueError("La cantidad a reponer debe ser mayor que cero.")
        
        producto = self.buscar(codigo)
        producto.stock += cantidad

    def valor_total(self):
        # CONDICIÓN: valor_total() devuelve el valor monetario de todo el stock del inventario
        total = sum(prod.valor_stock for prod in self._productos.values())
        return total

    def obtener_productos(self):
        # Método seguro para consultar los productos sin exponer la estructura interna mutable original
        # Devuelve una tupla con copias o referencias de solo lectura de los objetos Producto
        return tuple(self._productos.values())


# ==========================================
# BLOQUE DE PRUEBAS Y EJEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    mi_inventario = Inventario()

    # 1. Crear productos válidos
    p1 = Producto("A001", "Laptop", 800.0, 5)
    p2 = Producto("A002", "Ratón Inalámbrico", 25.5, 20)

    # Agregar al inventario
    mi_inventario.agregar_producto(p1)
    mi_inventario.agregar_producto(p2)

    # 2. Prueba de error: Añadir producto con código duplicado
    try:
        p3 = Producto("A001", "Teclado", 50.0, 10)
        mi_inventario.agregar_producto(p3)
    except ValueError as e:
        print(f"Error controlado (Código duplicado): {e}")

    # 3. Operaciones de venta y reposición
    mi_inventario.vender("A002", 5)   # Vendemos 5 ratones (quedan 15)
    mi_inventario.reponer("A001", 3)  # Reponemos 3 laptops (ahora hay 8)

    # 4. Cálculo del valor total del inventario
    # Laptop: 8 * 800 = 6400 | Ratón: 15 * 25.5 = 382.5
    print(f"Valor total del inventario: {mi_inventario.valor_total()}€")  # Salida: 6782.5

    # 5. Prueba de error: Vender más de lo disponible
    try:
        mi_inventario.vender("A001", 10)
    except ValueError as e:
        print(f"Error controlado (Stock insuficiente): {e}")