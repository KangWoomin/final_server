from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, userID, name, email, password=None):
        user = self.model(
            userID=userID,
            email = self.normalize_email(email),
            name = name,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, userID, name, email, password=None):
        user = self.create_user(
            userID=userID,
            email=email,
            name=name,
            password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    userID = models.CharField(verbose_name='userID', max_length=100, unique=True)
    email = models.EmailField(verbose_name='email', max_length=100)
    name = models.CharField(verbose_name='name',max_length=80)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['email','name']

    def __str__(self):
        return self.userID
    
    from django.contrib.auth.models import Permission
    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        return self.user_permissions.filter(codename=perm.split('.')[-1]).exists()

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        return self.user_permissions.filter(content_type_app_label=app_label).exists()
    
@property
def is_staff(self):
    return self.is_admin