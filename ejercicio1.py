class Usuario:
    # 1. Variable de clase para llevar el conteo global de usuarios.
    total = 0

    def __init__(self, nombre, cursos=None):
        self.nombre = nombre
        
        # PROBLEMA 1 (Argumento mutable por defecto): 
        # Si usábamos 'cursos=[]' por defecto, todos los usuarios que no 
        # especificaran cursos compartían EXACTAMENTE la misma lista en memoria.
        # SOLUCIÓN: Usar 'None' y crear una nueva lista independiente para cada instancia.
        if cursos is None:
            self.cursos = []
        else:
            self.cursos = list(cursos)
        
        # PROBLEMA 2 (Error de ámbito / UnboundLocalError):
        # Hacer 'total += 1' dentro del método hacía que Python buscara una 
        # variable local llamada 'total' que aún no existía.
        # SOLUCIÓN: Debemos referenciar explícitamente a la variable de clase 
        # escribiendo 'Usuario.total += 1'.
        Usuario.total += 1

    def agregar_curso(self, curso):
        # PROBLEMA 3 (Falta de referencia 'self'):
        # El código original decía 'cursos.append(curso)', lo cual fallaba 
        # porque la variable 'cursos' no existía en ese ámbito.
        # SOLUCIÓN: Se debe utilizar 'self.cursos.append(curso)' para modificar 
        # la lista del objeto actual.
        self.cursos.append(curso)


# ==========================================
# BLOQUE DE PRUEBAS
# ==========================================
if __name__ == "__main__":
    u1 = Usuario("Ana")
    u2 = Usuario("Marc")

    u1.agregar_curso("Python")

    # PROBLEMA 4 (Independencia de datos y conteo correcto):
    # Ahora verificamos que cada usuario tenga su propia lista y el total sea exacto.
    print("Cursos de Ana:", u1.cursos)   # Salida esperada: ['Python']
    print("Cursos de Marc:", u2.cursos)  # Salida esperada: [] (independiente de Ana)
    print("Total de usuarios creados:", Usuario.total)  # Salida esperada: 2