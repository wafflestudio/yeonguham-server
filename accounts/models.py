from django.db import models, transaction
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.ImageField(max_length=None, blank=True, null=True)
    lab = models.CharField(max_length=50, blank=True)
    TAG_CHOICES = [
        ("MED", "Medical"),
        ("BIO_SCI", "Bio_Sci"),
        ("COMP_EN", "Computer_En"),
        ("EC_EN", "Electrical_En"),
        ("MECH_EN", "Mechanical_En"),
        ("ARCHI", "Archi"),
        ("ENV_EN", "Environ_En"),
        ("ECO", "Economics"),
        ("PSY", "Psychology"),
        ("COMMUN_SCI", "Commun_Sci"),
        ("ANTHRO", "Anthropology"),
        ("IND", "Industrial"),
        ("FOOD", "FoodNutri"),
        ("LING", "Linguistics"),
        ("CLOTH", "Clothing"),
        ("EDU", "Education"),
        ("ARTPHY", "ArtPhy"),
    ]
    interests = ArrayField(
        models.CharField(max_length=14, choices=TAG_CHOICES), default=list, size=17
    )
    access_token = models.CharField(max_length=50, null=True)
    refresh_token = models.CharField(max_length=50, null=True)


# Custom manager for proxy user model
class CustomUserManager(models.Manager):
    @transaction.atomic
    def create_user_and_profile(
        self, username, email, access_token, refresh_token, interests
    ):
        user = User(username=username, email=email)
        user.set_unusable_password()
        user.save()

        profile = Profile(
            user=user,
            access_token=access_token,
            refresh_token=refresh_token,
            interests=interests,
        )
        profile.save()

        return user


# Proxy user model
class ProxyUser(User):
    objects = CustomUserManager()

    class Meta:
        proxy = True
