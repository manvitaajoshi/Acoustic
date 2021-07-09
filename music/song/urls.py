from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("", views.main, name='main'),
    path("login_form", views.login_form, name='login_form'),
    path("register", views.register, name='register'),
    path("upload_download", views.upload_download, name='upload_download'),
    path("song_upload", views.song_upload, name='song_upload'),
    path("song_list", views.song_list, name='song_list'),
    path("delete_song/<int:pk>", views.delete_song, name='delete_song'),
    path("song_request", views.song_request, name='song_request'),
    path("all_requests", views.all_requests, name='all_requests'),
    path("delete_request/<int:pk>", views.delete_request, name='delete_request'),
    path("search_song", views.search_song, name='search_song'),
    path("search_artist", views.search_artist, name='search_artist'),
    path("options", views.options, name='options'),
    path("read_request/<int:pk>", views.read_request, name='read_request'),
    path("log_out", views.log_out, name='log_out'),

]

# to be used only in development mode not in production mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
