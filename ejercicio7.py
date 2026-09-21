class Persona:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

    def __str__(self):
        return f"{self.nombre} ({self.email})"


class Alumno(Persona):
    def __init__(self, nombre, email, matricula):
        super().__init__(nombre, email)
        self.matricula = matricula


class Profesor(Persona):
    def __init__(self, nombre, email, especialidad):
        super().__init__(nombre, email)
        self.especialidad = especialidad


class Curso:
    def __init__(self, nombre, profesor, capacidad_maxima):
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor asignado debe ser una instancia de la clase Profesor.")
        if capacidad_maxima <= 0:
            raise ValueError("La capacidad máxima del curso debe ser mayor que cero.")

        self.nombre = nombre
        self._profesor = profesor
        self.capacidad_maxima = int(capacidad_maxima)
        
        # Colección interna protegida para los alumnos matriculados
        self._alumnos = []

    @property
    def profesor(self):
        return self._profesor

    def cambiar_profesor(self, nuevo_profesor):
        # CONDICIÓN: Solamente un Profesor puede ser profesor del curso
        if not isinstance(nuevo_profesor, Profesor):
            raise TypeError("El nuevo profesor debe ser una instancia de la clase Profesor.")
        self._profesor = nuevo_profesor

    def matricular(self, alumno):
        # CONDICIÓN: Únicamente pueden matricularse objetos Alumno
        if not isinstance(alumno, Alumno):
            raise TypeError("Solo se pueden matricular objetos de la clase Alumno.")
        
        # CONDICIÓN: Un alumno no puede matricularse dos veces
        if alumno in self._alumnos:
            raise ValueError(f"El alumno '{alumno.nombre}' ya se encuentra matriculado en este curso.")
        
        # CONDICIÓN: Debe respetarse la capacidad máxima
        if len(self._alumnos) >= self.capacidad_maxima:
            raise ValueError("No es posible matricular al alumno: el curso ha alcanzado su capacidad máxima.")
        
        self._alumnos.append(alumno)

    def desmatricular(self, alumno):
        if alumno not in self._alumnos:
            raise ValueError(f"El alumno '{alumno.nombre}' no está matriculado en este curso.")
        
        self._alumnos.remove(alumno)

    def obtener_alumnos(self):
        # Devuelve una tupla para proteger la colección interna de modificaciones externas directas
        return tuple(self._alumnos)

    def __str__(self):
        # REQUISITO: Implementar __str__() para mostrar un curso de forma legible
        alumnos_str = ", ".join([a.nombre for a in self._alumnos]) if self._alumnos else "Ninguno"
        return (
            f"Curso: {self.nombre}\n"
            f"Profesor: {self._profesor.nombre} ({self._profesor.especialidad})\n"
            f"Plazas ocupadas: {len(self._alumnos)}/{self.capacidad_maxima}\n"
            f"Alumnos matriculados: [{alumnos_str}]"
        )


#PRUEBA
if __name__ == "__main__":
    # 1. Creamos profesores y alumnos
    prof_carlos = Profesor("Carlos Pérez", "carlos@mail.com", "Desarrollo Web")
    prof_laura = Profesor("Laura Gómez", "laura@mail.com", "Bases de Datos")

    alumno1 = Alumno("Ana", "ana@mail.com", "A001")
    alumno2 = Alumno("Marc", "marc@mail.com", "A002")
    alumno3 = Alumno("Lucía", "lucia@mail.com", "A003")

    # 2. Creamos un curso con capacidad máxima de 2 alumnos
    curso_python = Curso("Programación en Python", prof_carlos, 2)

    # 3. Matriculaciones válidas
    curso_python.matricular(alumno1)
    curso_python.matricular(alumno2)

    print("--- Estado del Curso ---")
    print(curso_python)
    print("-" * 30)

    # 4. Pruebas de error (Validaciones)
    try:
        # Intentar matricular un tercer alumno superando la capacidad
        curso_python.matricular(alumno3)
    except ValueError as e:
        print(f"Error controlado (Capacidad): {e}")

    try:
        # Intentar matricular al mismo alumno dos veces
        curso_python.matricular(alumno1)
    except ValueError as e:
        print(f"Error controlado (Duplicado): {e}")

    try:
        # Intentar pasar un objeto que no es profesor
        curso_python.cambiar_profesor(alumno1)
    except TypeError as e:
        print(f"Error controlado (Tipo profesor): {e}")

    # 5. Desmatricular y cambiar profesor de forma correcta
    curso_python.desmatricular(alumno1)
    curso_python.matricular(alumno3)  # Ahora sí entra porque hay una plaza libre
    curso_python.cambiar_profesor(prof_laura)

    print("\n--- Estado Actualizado del Curso ---")
    print(curso_python)