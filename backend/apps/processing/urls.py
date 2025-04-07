from django.urls import path
from .views import DeconstructSongView, SongListCreateView

urlpatterns = [
    path("deconstruct/", DeconstructSongView.as_view(), name="deconstruct_song"),
    path("songs/", SongListCreateView.as_view(), name="song_list_create"),
]
