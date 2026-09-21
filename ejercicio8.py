class A:
    def metodo(self):
        return "A"

class B(A):
    def metodo(self):
        # Aquí 'super()' busca al siguiente en la fila (según el orden de Python)
        return "B" + super().metodo()

class C(A):
    def metodo(self):
        return "C" + super().metodo()

class D(B, C):
    def metodo(self):
        return "D" + super().metodo()


# --- ¿QUÉ ESTÁ PASANDO AQUÍ? ---
# 
# Se puede pensar que 'super()' significa siempre "llama a la clase de arriba 
# (el padre)". Pero cuando hay herencia múltiple (como D que hereda de B y de C), 
# Python hace una lista de orden llamada MRO (Method Resolution Order).

print("Orden en el que Python busca los métodos (MRO):")
print(D.mro())
print("-" * 50)


# --- EJECUTANDO EL EJEMPLO ---
obj = D()
resultado = obj.metodo()

print(f"Resultado de obj.metodo(): {resultado}")

# ¿Por qué sale "DBCA"?
# 1. Empieza en D -> añade "D".
# 2. El 'super()' de D le dice a Python: "busca al siguiente en la fila". 
#    Mirando el MRO, el siguiente es B -> añade "B".
# 3. El 'super()' de B busca al siguiente en la fila. El siguiente es C -> añade "C".
# 4. El 'super()' de C busca al siguiente. El siguiente es A -> añade "A".
# 5. Como A ya no tiene más 'super()', ahí termina la cadena.
# 
# Resultado final: "D" + "B" + "C" + "A" = "DBCA"