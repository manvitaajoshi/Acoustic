from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings

# Create your models here.
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp3', '.wav', '.mp4', '.aac', '.wma', '.m4a', '.flac']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    user_type_data = ((1, "HOD"), (2, "Listeners"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    admin = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    objects = models.Manager()


class AcousticUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    dob = models.DateField()
    objects = models.Manager()


class Songs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    album_name = models.CharField(max_length=200)
    uploaded_by = models.CharField(max_length=200, null=True, blank=True)
    audio_song = models.FileField(upload_to='media/songs', default="", validators=[validate_file_extension])
    album_cover = models.ImageField(upload_to='media/cover_image', default="", null=True, blank=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.audio_song.delete()
        self.album_cover.delete()
        super(Songs, self).delete()


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #admin = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, null=True)
    song_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    album_name = models.CharField(max_length=200)
    note = models.TextField(null=True, blank=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        super(Post, self).delete()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        super(Comment, self).delete()


@receiver(post_save, sender=CustomUser)
def create_userprofile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            AcousticUser.objects.create(admin=instance, dob="2001-01-01")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.acousticuser.save()
