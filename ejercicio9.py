class Libro:
    def __init__(self, isbn, titulo, autor):
        if not isbn or not isinstance(isbn, str):
            raise ValueError("El ISBN debe ser un texto válido.")
        
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.disponible = True  # Por defecto el libro está disponible

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"Libro: '{self.titulo}' (ISBN: {self.isbn}) - Autor: {self.autor} [{estado}]"


class Usuario:
    def __init__(self, id_usuario, nombre):
        if not id_usuario or not isinstance(id_usuario, str):
            raise ValueError("El identificador de usuario debe ser un texto válido.")
        
        self.id_usuario = id_usuario
        self.nombre = nombre

    def __str__(self):
        return f"Usuario: {self.nombre} (ID: {self.id_usuario})"


class Prestamo:
    def __init__(self, libro, usuario):
        # CONDICIÓN: Un Prestamo debe relacionar un libro y un usuario (usando objetos)
        if not isinstance(libro, Libro):
            raise TypeError("Se requiere un objeto de la clase Libro.")
        if not isinstance(usuario, Usuario):
            raise TypeError("Se requiere un objeto de la clase Usuario.")
        
        self.libro = libro
        self.usuario = usuario
        self.activo = True

    def finalizar(self):
        # Marca el préstamo como finalizado y libera el libro
        self.activo = False
        self.libro.disponible = True

    def __str__(self):
        estado = "Activo" if self.activo else "Finalizado"
        return f"Préstamo -> Libro: '{self.libro.titulo}' | Usuario: {self.usuario.nombre} [{estado}]"


class Biblioteca:
    def __init__(self):
        # Colecciones protegidas para evitar modificaciones directas externas
        self._libros = {}      # Diccionario: {isbn: objeto Libro}
        self._usuarios = {}    # Diccionario: {id_usuario: objeto Usuario}
        self._prestamos = []   # Lista de objetos Prestamo

    def agregar_libro(self, libro):
        if not isinstance(libro, Libro):
            raise TypeError("Solo se pueden agregar objetos de la clase Libro.")
        
        # CONDICIÓN: Cada libro debe tener un ISBN único
        if libro.isbn in self._libros:
            raise ValueError(f"Ya existe un libro registrado con el ISBN '{libro.isbn}'.")
        
        self._libros[libro.isbn] = libro

    def registrar_usuario(self, usuario):
        if not isinstance(usuario, Usuario):
            raise TypeError("Solo se pueden registrar objetos de la clase Usuario.")
        
        # CONDICIÓN: Cada usuario debe tener un identificador único
        if usuario.id_usuario in self._usuarios:
            raise ValueError(f"Ya existe un usuario registrado con el ID '{usuario.id_usuario}'.")
        
        self._usuarios[usuario.id_usuario] = usuario

    def prestar(self, isbn, id_usuario):
        # Validar existencia de libro y usuario
        if isbn not in self._libros:
            raise KeyError(f"No se encontró el libro con ISBN '{isbn}'.")
        if id_usuario not in self._usuarios:
            raise KeyError(f"No se encontró el usuario con ID '{id_usuario}'.")
        
        libro = self._libros[isbn]
        usuario = self._usuarios[id_usuario]

        # CONDICIÓN: No puede prestarse un libro que ya esté prestado
        if not libro.disponible:
            raise ValueError(f"El libro '{libro.titulo}' ya se encuentra prestado.")

        # CONDICIÓN: Cada usuario puede tener como máximo 3 libros simultáneamente
        prestamos_usuario_activos = [
            p for p in self._prestamos 
            if p.usuario.id_usuario == id_usuario and p.activo
        ]
        if len(prestamos_usuario_activos) >= 3:
            raise ValueError(f"El usuario '{usuario.nombre}' ha alcanzado el límite máximo de 3 libros prestados simultáneamente.")

        # Creamos el préstamo utilizando los objetos Libro y Usuario
        nuevo_prestamo = Prestamo(libro, usuario)
        libro.disponible = False  # Cambiamos el estado del libro
        self._prestamos.append(nuevo_prestamo)

    def devolver(self, isbn):
        if isbn not in self._libros:
            raise KeyError(f"No se encontró el libro con ISBN '{isbn}'.")
        
        # Buscamos el préstamo activo asociado a este ISBN
        prestamo_encontrado = None
        for p in self._prestamos:
            if p.libro.isbn == isbn and p.activo:
                prestamo_encontrado = p
                break
        
        if not prestamo_encontrado:
            raise ValueError(f"No consta ningún préstamo activo para el libro con ISBN '{isbn}'.")

        # CONDICIÓN: Devolver un libro debe finalizar el préstamo correspondiente
        prestamo_encontrado.finalizar()

    def prestamos_activos(self):
        # Devuelve una tupla con los préstamos que siguen vigentes
        return tuple(p for p in self._prestamos if p.activo)


# ==========================================
# BLOQUE DE PRUEBAS Y EJEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    biblioteca = Biblioteca()

    # 1. Registrar libros
    libro1 = Libro("978-0132350884", "Clean Code", "Robert C. Martin")
    libro2 = Libro("978-0201633610", "Design Patterns", "Erich Gamma")
    libro3 = Libro("978-1118008188", "Python for Everybody", "Charles Severance")
    libro4 = Libro("978-0596007126", "Head First Design Patterns", "Eric Freeman")

    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)
    biblioteca.agregar_libro(libro4)

    # 2. Registrar usuarios
    user1 = Usuario("U001", "Ana Gómez")
    user2 = Usuario("U002", "Marc Pérez")

    biblioteca.registrar_usuario(user1)
    biblioteca.registrar_usuario(user2)

    # 3. Realizar préstamos
    biblioteca.prestar("978-0132350884", "U001")  # Ana toma Clean Code
    biblioteca.prestar("978-0201633610", "U001")  # Ana toma Design Patterns
    biblioteca.prestar("978-1118008188", "U001")  # Ana toma Python for Everybody

    print(f"Préstamos activos totales: {len(biblioteca.prestamos_activos())}")

    # 4. Prueba de error: Ana intenta pedir un 4to libro (supera el límite de 3)
    try:
        biblioteca.prestar("978-0596007126", "U001")
    except ValueError as e:
        print(f"Error controlado (Límite de libros): {e}")

    # 5. Prueba de error: Intentar prestar un libro que ya está prestado
    try:
        biblioteca.prestar("978-0132350884", "U002")  # Marc intenta pedir Clean Code (lo tiene Ana)
    except ValueError as e:
        print(f"Error controlado (Libro no disponible): {e}")

    # 6. Devolución de un libro y nuevo préstamo
    biblioteca.devolver("978-0132350884")  # Ana devuelve Clean Code
    print("Libro devuelto con éxito. Clean Code ahora está disponible.")

    # Ahora Marc sí puede pedir Clean Code
    biblioteca.prestar("978-0132350884", "U002")
    print(f"Préstamos activos actualizados: {len(biblioteca.prestamos_activos())}")