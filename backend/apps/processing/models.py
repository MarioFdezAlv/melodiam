from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    # Permite que el campo de usuario sea nulo si se procesa sin almacenar
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="songs", null=True, blank=True
    )
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to="songs/")
    # Se guarda la salida del procesamiento en formato JSON
    processed_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
