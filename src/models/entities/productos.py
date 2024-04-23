class Producto:
    def __init__(self, id, nombre, imagen, precio):
        self.id = id
        self.nombre = nombre
        self.imagen = imagen
        self.precio = precio

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "imagen": self.imagen,
            # Convertir precio a un tipo serializable, como float
            "precio": float(self.precio)
        }
