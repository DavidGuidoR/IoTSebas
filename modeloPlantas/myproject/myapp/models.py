from django.db import models

class Planta(models.Model):
    nombre = models.CharField(max_length=100)
    humedad = models.FloatField()

    def __str__(self):
        return self.nombre

class PlantaUser(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name="usuarios")
    # Puedes agregar más campos si necesitas, por ejemplo, un usuario asociado
    # usuario = models.CharField(max_length=100)

    def __str__(self):
        return f"Planta asociada: {self.planta.nombre}"

class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')  # Directorio donde se guardará la imagen
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Fecha de carga
