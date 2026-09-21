class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0.0):
        self.titular = titular
        
        # Validamos que el saldo inicial no sea negativo
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        
        self._saldo = float(saldo_inicial)
        
        # Historial interno protegido (privado mediante guion bajo)
        self._historial = []
        if saldo_inicial > 0:
            self._historial.append(f"Cuenta creada con saldo inicial: {saldo_inicial}")

    @property
    def saldo(self):
        # Propiedad de solo lectura para consultar el saldo actual
        return self._saldo

    def ingresar(self, cantidad):
        # CONDICIÓN: No se permiten cantidades negativas o cero
        if cantidad <= 0:
            raise ValueError("La cantidad a ingresar debe ser mayor que cero.")
        
        self._saldo += cantidad
        self._historial.append(f"Ingreso: +{cantidad} (Saldo actual: {self._saldo})")

    def retirar(self, cantidad):
        # CONDICIÓN: No se permiten cantidades negativas o cero
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser mayor que cero.")
        
        # CONDICIÓN: No se puede retirar más dinero del disponible (evita sobregiros)
        if cantidad > self._saldo:
            raise ValueError("Fondos insuficientes para realizar el retiro.")
        
        self._saldo -= cantidad
        self._historial.append(f"Retiro: -{cantidad} (Saldo actual: {self._saldo})")

    def transferir(self, cuenta_destino, cantidad):
        # Validaciones de cantidad y fondos (reutilizando lógica de seguridad)
        if cantidad <= 0:
            raise ValueError("La cantidad a transferir debe ser mayor que cero.")
        if cantidad > self._saldo:
            raise ValueError("Fondos insuficientes para realizar la transferencia.")
        if not isinstance(cuenta_destino, CuentaBancaria):
            raise TypeError("La cuenta de destino debe ser una instancia de CuentaBancaria.")
        
        # CONDICIÓN: Una transferencia debe modificar correctamente ambas cuentas
        # 1. Modificamos la cuenta origen (restamos)
        self._saldo -= cantidad
        self._historial.append(f"Transferencia enviada: -{cantidad} a {cuenta_destino.titular} (Saldo actual: {self._saldo})")
        
        # 2. Modificamos la cuenta destino (sumamos) y registramos en su historial también
        cuenta_destino._saldo += cantidad
        cuenta_destino._historial.append(f"Transferencia recibida: +{cantidad} de {self.titular} (Saldo actual: {cuenta_destino._saldo})")

    def obtener_historial(self):
        # CONDICIÓN: El historial devuelto no debe permitir modificar el historial interno real.
        # Solución: Devolvemos una copia superficial de la lista (list()) o una tupla (tuple()).
        # Si modifican la lista devuelta desde fuera, el '_historial' original no sufrirá alteraciones.
        return list(self._historial)


# ==========================================
# BLOQUE DE PRUEBAS Y EJEMPLO DE USO
# ==========================================
if __name__ == "__main__":
    # Creamos cuentas de prueba
    cuenta_ana = CuentaBancaria("Ana", 400.0)
    cuenta_marc = CuentaBancaria("Marc", 100.0)

    # 1. Realizamos operaciones válidas
    cuenta_ana.ingresar(200)
    cuenta_ana.retirar(50)
    cuenta_ana.transferir(cuenta_marc, 150)

    print(f"Saldo final Ana: {cuenta_ana.saldo}€")     # Salida esperada: 400 + 200 - 50 - 150 = 400
    print(f"Saldo final Marc: {cuenta_marc.saldo}€")   # Salida esperada: 100 + 150 = 250

    # 2. Comprobación de seguridad en el historial
    historial_ana = cuenta_ana.obtener_historial()
    historial_ana.append("Intento de hackeo o modificación externa")  # Modificamos la copia externa

    print("\n--- Historial real de Ana (protegido) ---")
    for mov in cuenta_ana.obtener_historial():
        print(mov)  # No contendrá el texto malicioso de la línea anterior, demostrando el aislamiento.