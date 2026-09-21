
class Evento:
    def __init__(self, capacidad_maxima):
        # Almacenamos el límite máximo de plazas
        self._capacidad_maxima = capacidad_maxima
        
        # CONDICIÓN: La lista interna de personas inscritas no debe poder 
        # modificarse directamente desde fuera. Usamos un atributo protegido (_personas).
        self._personas = []

    def reservar(self, persona):
        # CONDICIÓN: Una persona no puede reservar dos veces
        if persona in self._personas:
            raise ValueError(f"La persona '{persona}' ya tiene una reserva confirmada.")
        
        # CONDICIÓN: No pueden superarse las plazas disponibles
        if len(self._personas) >= self._capacidad_maxima:
            raise ValueError("Lo sentimos, el evento ha alcanzado su capacidad máxima.")
        
        # Si pasa las validaciones, registramos a la persona
        self._personas.append(persona)

    def cancelar(self, persona):
        # CONDICIÓN: No puede cancelarse una reserva inexistente
        if persona not in self._personas:
            raise ValueError(f"No se encontró una reserva asociada a '{persona}'.")
        
        # Eliminamos a la persona de la lista de inscritos
        self._personas.remove(persona)

    def plazas_disponibles(self):
        # Calcula el número de plazas que aún quedan libres
        return self._capacidad_maxima - len(self._personas)

    def __len__(self):
        # REquisito: len(evento) debe devolver el número de personas inscritas
        return len(self._personas)

    @property
    def personas(self):
        # Diseñado para proteger la lista interna: devolvemos una tupla (inmutable) 
        # en lugar de la lista original, evitando modificaciones externas directas.
        return tuple(self._personas)


#PRUEBA

if __name__ == "__main__":
    # Creamos un evento con un máximo de 2 plazas
    taller = Evento(2)

    # 1. Reservas exitosas
    taller.reservar("Ana")
    taller.reservar("Marc")
    print(f"Plazas disponibles: {taller.plazas_disponibles()}")  # Salida: 0
    print(f"Total con len(): {len(taller)}")                     # Salida: 2

    # 2. Prueba de error: Reservar dos veces a la misma persona
    try:
        taller.reservar("Ana")
    except ValueError as error:
        print(f"Error controlado: {error}")

    # 3. Prueba de error: Superar las plazas disponibles
    try:
        taller.reservar("Lucía")
    except ValueError as error:
        print(f"Error controlado: {error}")

    # 4. Cancelación de una reserva existente
    taller.cancelar("Ana")
    print(f"Plazas disponibles tras cancelar a Ana: {taller.plazas_disponibles()}")  # Salida: 1

    # 5. Prueba de error: Cancelar una reserva que no existe
    try:
        taller.cancelar("Carlos")
    except ValueError as error:
        print(f"Error controlado: {error}")