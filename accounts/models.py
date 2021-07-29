from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.ImageField(max_length=None, blank=True, null=True)
    lab = models.CharField(max_length=50, blank=True)
    TAG_CHOICES = [
        ("MEDICAL", "Medical"),
        ("BIO_SCI", "Bio_Sci"),
        ("COMPUTER_EN", "Computer_En"),
        ("ELECTRICAL_EN", "Electrical_En"),
        ("MECHANICAL_EN", "Mechanical_En"),
        ("ARCHI", "Archi"),
        ("ENVIRON_EN", "Environ_En"),
        ("ECONOMICS", "Economics"),
        ("PSYCHOLOGY", "Psychology"),
        ("COMMUN_SCI", "Commun_Sci"),
        ("ANTHROPOLOGY", "Anthropology"),
        ("INDUSTRIAL", "Industrial"),
        ("FOODNUTRI", "FoodNutri"),
        ("LINGUISTICS", "Linguistics"),
        ("CLOTHINGF", "Clothing"),
        ("EDUCATION", "Education"),
        ("ARTPHY", "ArtPhy"),
    ]
    interests = ArrayField(
        models.CharField(max_length=14, choices=TAG_CHOICES), default=list, size=17
    )
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
