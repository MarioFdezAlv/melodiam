import os
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

from .models import Song
from .serializers import SongSerializer


def process_audio(file_path):
    """
    Llama a Demucs para separar la pista. La salida se guardará en un directorio 'demucs_output'
    dentro del mismo directorio del archivo.
    """
    output_dir = os.path.join(os.path.dirname(file_path), "demucs_output")
    os.makedirs(output_dir, exist_ok=True)

    # Comando para invocar Demucs; se usa el modelo por defecto.
    # La salida se ubicará en output_dir.
    command = ["demucs", file_path, "--out", output_dir]

    try:
        subprocess.run(command, check=True)
        # Se asume que Demucs genera carpetas por pista dentro de output_dir.
        result = {"message": "Audio processed successfully", "output_dir": output_dir}
    except subprocess.CalledProcessError as e:
        result = {"error": f"Error processing audio: {str(e)}"}
    return result


class DeconstructSongView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        audio_file = request.data.get("audio_file")
        if not audio_file:
            return Response(
                {"error": "No audio file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Guarda el archivo temporalmente
        file_path = default_storage.save("temp/" + audio_file.name, audio_file)

        # Llama a Demucs para procesar el audio
        result = process_audio(file_path)
        return Response(result, status=status.HTTP_200_OK)


class SongListCreateView(generics.ListCreateAPIView):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Song.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
