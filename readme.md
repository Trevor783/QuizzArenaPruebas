# 📚 Repositorio de Prácticas: Programación Orientada a Objetos (POO) en Python

Este repositorio recopila una serie de ejercicios prácticos diseñados para dominar los conceptos clave de la Programación Orientada a Objetos en Python, abarcando desde la corrección de errores comunes de diseño y encapsulamiento hasta patrones avanzados, polimorfismo y herencia múltiple.

---

## 🛠️ Listado de Ejercicios y Módulos

### 1. Corrección y Diseño de Clases: `gestion_usuarios.py`
* **Descripción:** Análisis y refactorización de una clase `Usuario` con errores típicos de diseño.
* **Conceptos clave:** 
  * Solución al problema de argumentos mutables por defecto (listas compartidas en memoria).
  * Manejo correcto del ámbito de variables de clase frente a variables de instancia (`Usuario.total`).
  * Uso correcto de la referencia `self` en métodos de instancia.

### 2. Gestión de Aforos: `gestion_evento.py`
* **Descripción:** Sistema de control de plazas para eventos con restricciones estrictas de cupo y seguridad de datos.
* **Conceptos clave:**
  * Encapsulamiento de colecciones internas mediante atributos protegidos (`_personas`) y propiedades de solo lectura (`tuple`).
  * Implementación del método mágico `__len__` para obtener el número de inscritos directamente con la función nativa `len()`.
  * Control de excepciones ante reservas duplicadas, exceso de aforo y cancelaciones erróneas.

### 3. Jerarquía Geométrica y Polimorfismo: `figuras_geometricas.py`
* **Descripción:** Cálculo de áreas y perímetros para diferentes formas geométricas utilizando una interfaz uniforme.
* **Conceptos clave:**
  * Polimorfismo aplicado a través de métodos compartidos (`nombre()`, `area()`, `perimetro()`).
  * Reutilización de código mediante herencia: la clase `Cuadrado` hereda directamente de `Rectangulo` para evitar duplicar fórmulas matemáticas.
  * Uso de la librería matemática estándar (`math`) para cálculos trigonométricos (Teorema de Pitágoras en triángulos rectángulos).

### 4. Control Bancario y Transacciones: `cuenta_bancaria.py`
* **Descripción:** Simulación de cuentas corrientes con operaciones de ingreso, retiro y transferencias seguras.
* **Conceptos clave:**
  * Validación estricta de saldos y prevención de sobregiros.
  * Aislamiento de historiales de movimientos: el método `obtener_historial()` devuelve copias defensivas para evitar alteraciones externas en la colección real.
  * Modificación coherente de múltiples objetos durante una transferencia bancaria.

### 5. Patrón Strategy en Descuentos: `refactor_pedidos.py`
* **Descripción:** Refactorización de un calculador de precios basado en condicionales rígidos (`if/elif`) hacia un diseño escalable.
* **Conceptos clave:**
  * Aplicación del **Patrón Strategy** utilizando clases abstractas (`ABC`) y métodos abstractos.
  * Cumplimiento del **Principio Abierto/Cerrado (OCP)**: es posible añadir nuevos tipos de cliente (ej. `ClienteEstudiante`) creando una nueva clase sin modificar la lógica principal de la clase `Pedido`.

### 6. Control de Inventario y Stock: `gestion_inventario.py`
* **Descripción:** Sistema de gestión de productos con control riguroso de referencias y existencias.
* **Conceptos clave:**
  * Asociación de clases (`Inventario` contiene objetos `Producto`).
  * Prevención de códigos duplicados y validación de tipos de datos en constructores.
  * Cálculo dinámico del valor monetario total del inventario.

### 7. Sistema Académico de Cursos: `sistema_cursos.py`
* **Descripción:** Gestión de relaciones jerárquicas entre personas, roles, profesores y alumnos matriculados.
* **Conceptos clave:**
  * Herencia simple: `Alumno` y `Profesor` heredan de la clase base `Persona`.
  * Validación de tipos estrictos (`isinstance`) para asegurar que solo objetos de tipo `Profesor` impartan clases y objetos `Alumno` se matriculen.
  * Sobrecarga del método mágico `__str__` para generar una representación legible y formateada del estado del curso.

### 8. Herencia Múltiple y MRO: `herencia_multiple_explicada.py`
* **Descripción:** Análisis técnico y conceptual del funcionamiento de la herencia múltiple en Python.
* **Conceptos clave:**
  * Comprensión del algoritmo de linealización **C3** y el **MRO (Method Resolution Order)**.
  * Comportamiento dinámico de `super()` como un enlace cooperativo en cadena (y no como un simple salto a la clase padre superior).

### 9. Sistema de Biblioteca: `sistema_biblioteca.py`
* **Descripción:** Sistema integral para el control de préstamos bibliotecarios utilizando relaciones basadas en objetos complejos.
* **Conceptos clave:**
  * Relaciones directas entre objetos (`Prestamo` almacena instancias completas de `Libro` y `Usuario` en lugar de meros identificadores en texto).
  * Restricción de límites operativos (máximo de 3 préstamos simultáneos por usuario).
  * Control de estados de disponibilidad de los ejemplares y finalización de préstamos.

### 10. Tienda Polimórfica de Pedidos: `gestion_pedidos_tienda.py`
* **Descripción:** Sistema de procesamiento de carritos de compras con productos físicos, digitales, suscripciones y descuentos.
* **Conceptos clave:**
  * Polimorfismo puro: eliminación absoluta de condicionales de tipo (`if type(...)` o `isinstance`) en el cálculo global del pedido.
  * Extensibilidad total ante la incorporación de nuevos catálogos o reglas de negocio futuras.

---

## 🚀 Cómo ejecutar los scripts
Cada ejercicio está autocontenido dentro de su respectivo bloque ejecutable (`if __name__ == "__main__":`). Puedes correr cualquier script directamente desde tu terminal utilizando Python:

```bash
python nombre_del_fichero.py