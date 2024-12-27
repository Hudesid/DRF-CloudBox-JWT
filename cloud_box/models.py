from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    password = models.CharField(max_length=128)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """ Hash the password before saving """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """ Check the password hash """
        return check_password(raw_password, self.password)


class Folder(models.Model):
    folder_name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.folder_name


class File(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    file_size = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', blank=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super(File, self).save(*args, **kwargs)

