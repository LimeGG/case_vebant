from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Profession(models.Model):
    name = models.CharField(max_length=100, unique=True)


class User(AbstractBaseUser):
    username = models.CharField(max_length=140, unique=True)
    email = models.EmailField('Email', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profession = models.ForeignKey(Profession, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Competence(models.Model):
    name = models.CharField(max_length=100,  unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Material(models.Model):
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    MATERIAL_TYPES = (
        ('text', 'Text'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('online_course', 'Online Course'),
    )
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='materials/', null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()


class MarkedCompetence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)








