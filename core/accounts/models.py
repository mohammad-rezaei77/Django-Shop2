from django.db import models
from django .contrib.auth.models import (
                        BaseUserManager,AbstractBaseUser,PermissionsMixin) 
from django.utils.translation import gettext_lazy as _



from .validators import iranian_phone_number_validator
from django.dispatch import receiver
from django.db.models.signals import post_save

class UserType(models.IntegerChoices):
    customer = 1, _("customer")
    admin = 2, _("admin")
    superuser = 3, _("superuser")
 


class UserManager(BaseUserManager):
    #custom user manager where  is the unique identifier of the user
    def create_user(self, email,password,**extra_fields):
        #create and save a user the given email and password and extra_fields
        if not email:
            raise ValueError(_("email must be a valid email address"))
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,password,**extra_fields):
        #create and save a superuser the given email and password and extra_fields
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('type', UserType.customer.value)
        

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("superuser must be have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("superuser must be have is_superuser=True"))

        return self.create_user(email,password,**extra_fields)


class User (AbstractBaseUser,PermissionsMixin):
    #Custom User models our app
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    type = models.IntegerField(choices=UserType.choices, default=UserType.customer.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email   



class CustomerProfile(models.Model):
    user=models.OneToOneField('User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=12,
        validators=[iranian_phone_number_validator]
        )
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
     
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.type == UserType.customer.value:
        CustomerProfile.objects.create(user=instance)
    
