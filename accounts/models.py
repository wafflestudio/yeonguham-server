from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime, date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Researchee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, blank=True)
    birth = models.DateField(auto_now=False, auto_now_add=False)
    profileImage = models.ImageField(max_length=255, blank=True, null=True)
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
    def create_user_researchee(self, sender, instance, created, **kwargs):
        if created:
            Researchee.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_researchee(self, sender, instance, **kwargs):
        instance.researchee.save()

    def get_age(self):
        today = date.today()
        return int((today - self.birth).days / 365)


class Researcher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, blank=True)
    lab = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100)

    @receiver(post_save, sender=User)
    def create_user_researcher(self, sender, instance, created, **kwargs):
        if created:
            Researcher.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_Researcher(self, sender, instance, **kwargs):
        instance.researcher.save()
