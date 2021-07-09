from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from .models import CustomUser, Songs, Post
from .forms import SongForm, RequestSong
from django import forms


# Create your views here.
def main(request):
    return render(request, 'main.html')


def login_form(request):
    if request.POST:
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("options")

        else:
            messages.error(request, 'Invalid credentials.')
            return HttpResponseRedirect("login_form")
    else:
        return render(request, 'login_form.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        dob = request.POST.get("dob")
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, user_type=2)
            user.acousticuser.username = username
            user.acousticuser.password = password
            user.acousticuser.email = email
            user.acousticuser.dob = dob
            user.save()
            return redirect('login_form')
        except:
            messages.error(request, 'Username already taken.')
            return redirect('register')
    else:
        return render(request, 'register.html')

@login_required
def log_out(request):
    if request.method == 'POST':
        logout(request)
    return redirect('main')

@login_required
def upload_download(request):
    context = {}
    if request.method == 'POST':
        song_name = request.POST.get("song_name")
        artist_name = request.POST.get("artist_name")
        album_name = request.POST.get("album_name")
        audio_song = request.FILES['audio_song']
        fs = FileSystemStorage()
        file_name = fs.save(audio_song.name, audio_song)
        context['url'] = fs.url(file_name)
    return render(request, 'upload_download.html', context)

@login_required
def song_list(request):
    songs = Songs.objects.all()
    return render(request, 'song_list.html', {'songs': songs})

@login_required
def song_upload(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song_list')
    else:
        initial = {'uploaded_by': request.user.username}
        form = SongForm(initial=initial)
    return render(request, 'song_upload.html', {'form': form})


@login_required
def delete_song(request, pk):
    if request.method == 'POST':
        song = Songs.objects.get(pk=pk)
        song.delete()
        return redirect('song_list')

@login_required
def all_requests(request):
    posts = Post.objects.all()
    return render(request, 'all_requests.html', {'posts': posts})

@login_required
def read_request(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        params = {'post': post}
        return render(request, 'read_request.html', params)


# def song_request(request):
#     if request.method == 'POST':
#         title = request.POST.get("title")
#         author = request.POST.get("author")
#         song_name = request.POST.get("song_name")
#         artist_name = request.POST.get("artist_name")
#         album_name = request.POST.get("album_name")
#         note = request.POST.get("note")
#         post = Post.objects.create_user(title=title, author=author, song_name=song_name, artist_name=artist_name,
#                                                 album_name=album_name, note=note)
#         post.acousticuser.title = title
#         post.acousticuser.author = author
#         post.acousticuser.song_name = song_name
#         post.acousticuser.artist_name = artist_name
#         post.acousticuser.album_name = album_name
#         post.acousticuser.note = note
#         post.save()
#         return HttpResponseRedirect('all_requests')
#     else:
#         return render(request, 'song_request.html')
@login_required
def song_request(request):
    if request.method == 'POST':

        #instance = CustomUser.objects.filter(user=request.user).first()
        form = RequestSong(request.POST, request.FILES)
        #form.fields["Author"].initial = CustomUser.username
        if form.is_valid():
            form.save()
            return redirect('all_requests')
    else:
        initial = {'author': request.user.username}
        form = RequestSong(initial=initial)
    return render(request, 'song_request.html', {'form': form})

@login_required
def delete_request(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('all_requests')

@login_required
def search_song(request):
    search = request.GET['search']
    if search != "":
        songs = Songs.objects.filter(song_name__icontains=search)
        params = {'songs': songs}
        return render(request, 'search.html', params)
    else:
        return redirect('song_list')

@login_required
def search_artist(request):
    search = request.GET['search']
    if search != "":
        songs = Songs.objects.filter(artist_name__icontains=search)
        params = {'songs': songs}
        return render(request, 'search.html', params)
    else:
        return redirect('song_list')

@login_required
def options(request):
    return render(request, 'options.html')
