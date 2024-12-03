from rest_framework import serializers
from .models import Planta, PlantaUser

class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = '__all__'

class PlantaUserSerializer(serializers.ModelSerializer):
    planta = PlantaSerializer()  # Incluye los datos de la planta

    class Meta:
        model = PlantaUser
        fields = '__all__'

from .models import ImageModel

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'