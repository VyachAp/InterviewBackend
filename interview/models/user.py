from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator


class MyAccountManager(BaseUserManager):
    def create_user(self, phone, *args, **kwargs):
        if not phone:
            raise ValueError('Не введён номер телефона')

        user = self.model(
            phone=phone
        )
        if not kwargs['superuser']:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, *args, **kwargs):
        user = self.create_user(
            phone=phone,
            superuser=True
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.set_password(kwargs['password'])

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    SEX_CHOICES = [
        ('M', "Мужской"),
        ('F', "Женский"),
        ('U', "Не указывать")
    ]
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+79999999999'. Up to 15 digits allowed.")
    phone = models.CharField('Номер телефона', validators=[phone_regex], max_length=12,
                             blank=True, unique=True, editable=False)  # validators should be a list
    username = models.CharField("Никнейм", max_length=30, blank=True, null=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    avatar = models.URLField("Аватар", null=True, blank=True)
    date_of_birth = models.DateField("Дата рождения", null=True, blank=True)
    sex = models.CharField("Пол", max_length=2, choices=SEX_CHOICES, null=True, blank=True)
    country = models.CharField("Страна", max_length=64, null=True, blank=True)
    city = models.CharField("Город", max_length=64, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    surname = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    objects = MyAccountManager()

    def __str__(self):
        return self.phone

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
