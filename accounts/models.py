from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


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

    @receiver(post_save, sender=User)
    def create_user_researchee(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_researchee(sender, instance, **kwargs):
        instance.researchee.save()
