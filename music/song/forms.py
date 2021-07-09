from django import forms
from django.forms import TextInput

from .models import Songs, Post, CustomUser


class SongForm(forms.ModelForm):
    class Meta:
        model = Songs
        fields = ('song_name', 'artist_name', 'album_name', 'audio_song', 'album_cover', 'uploaded_by')
        widgets = {
            'uploaded_by': TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Username only'}),
        }

class RequestSong(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'song_name', 'artist_name', 'album_name', 'note')
        widgets = {
            'author': TextInput(attrs={
                'class': 'form_input',
                'placeholder': 'Username only'}),
        }
        # widgets = {
        #     'title': TextInput(attrs={
        #         'class': 'form_input',
        #         'placeholder': ''}),
        #     'author': TextInput(attrs={
        #         'class': 'form_input',
        #         'placeholder': ''}),
        #     'song_name': TextInput(attrs={
        #         'class': 'form_input',
        #         'placeholder': ''}),
        #     'artist_name': TextInput(attrs={
        #         'class': 'form_input',
        #         'placeholder': ""}),
        #     'album_name': TextInput(attrs={
        #         'class': 'form_input',
        #         'placeholder': ''}),
        #    'note': TextInput(attrs={
        #         'class': 'form_input',
        #         'placeholder': ''}),
        # }