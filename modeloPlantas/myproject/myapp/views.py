from rest_framework.viewsets import ModelViewSet
from .models import Planta, PlantaUser
from .serializers import PlantaSerializer, PlantaUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ImageModel
from .serializers import ImageSerializer
import os
from django.conf import settings

import os
import numpy as np
from skimage.transform import resize
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from keras.models import load_model
import matplotlib.pyplot as plt

# Cargar el modelo preentrenado
modelo_h5 = 'C:/Users/Guido/Desktop/Devs/IoT/IoTSebas/modeloPlantas/myproject/myapp/plantas.h5'
riesgo_model = load_model(modelo_h5)

# Definir las etiquetas
sriesgos = ['AloeVera', 'Graptopetalum', 'CrasullaGollum']

class PlantaViewSet(ModelViewSet):
    queryset = Planta.objects.all()
    serializer_class = PlantaSerializer

class PlantaUserViewSet(ModelViewSet):
    queryset = PlantaUser.objects.all()
    serializer_class = PlantaUserSerializer

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Permitir cargar archivos

    def post(self, request, *args, **kwargs):
        # Verificar si la solicitud tiene un archivo llamado "image"
        uploaded_file = request.FILES.get('image')
        if not uploaded_file:
            return Response({"error": "No se encontró un archivo con la clave 'image'"}, status=400)

        # Ruta donde se almacenará el archivo
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_images', uploaded_file.name)

        # Crear el directorio si no existe
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Guardar el archivo en el sistema de archivos local
        with open(save_path, 'wb') as file:
            for chunk in uploaded_file.chunks():
                file.write(chunk)

        # Procesar la imagen para el modelo
        try:
            # Leer y redimensionar la imagen
            image = plt.imread(save_path)
            image_resized = resize(image, (21, 28), anti_aliasing=True, clip=False, preserve_range=True)
            image_array = np.array(image_resized, dtype=np.uint8)

            # Preprocesar la imagen para el modelo
            test_X = image_array.astype('float32') / 255.
            test_X = np.expand_dims(test_X, axis=0)  # Agregar dimensión para batch

            # Realizar predicción
            predicted_classes = riesgo_model.predict(test_X)
            predicted_label = sriesgos[np.argmax(predicted_classes[0])]
            # Imprimir la salida del modelo en la consola
            print("Predicción bruta:", predicted_classes[0])
            print("Etiqueta predicha:", predicted_label)

            planta = Planta.objects.filter(nombre=predicted_label).first()
            if not planta:
                return Response({"error": f"No se encontró una planta con el nombre '{predicted_label}'"}, status=404)

            # Crear un nuevo registro en `myapp_plantauser` (ID autoincremental)
            planta_user = PlantaUser.objects.create(planta=planta)
        except Exception as e:
            return Response({"error": f"Error al procesar la imagen: {str(e)}"}, status=500)

        # Construir la URL para acceder a la imagen
        image_url = request.build_absolute_uri(f'{settings.MEDIA_URL}uploaded_images/{uploaded_file.name}')

        return Response({
            "message": "Imagen cargada y procesada correctamente",
            "image_url": image_url,
            "predicted_plant": predicted_label
        }, status=200)
