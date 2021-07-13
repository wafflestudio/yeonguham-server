from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from ..accounts.models import Profile

# Create your models here.


class Research(models.Model):
    subject = models.CharField(max_length=20, blank=False, null=True)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    recruit_start = models.DateTimeField(auto_now=False, auto_now_add=False)
    recruit_end = models.DateTimeField(auto_now=False, auto_now_add=False)
    research_start = models.DateTimeField(auto_now=False, auto_now_add=False)
    research_end = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    link = models.URLField(max_length=200, blank=True)
    detail = models.TextField()
    requirement = models.TextField()
    capacity = models.IntegerField()
    current_number = models.IntegerField(default=0)
    hit = models.IntegerField(default=0)
    researcher = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="researches"
    )
    tags = models.ManyToManyField(
        "Tag", null=True, related_name="researches", through="TagResearch"
    )
    mark_users = models.ManyToManyField(
        User, null=True, related_name="marked_research", through="Mark"
    )
    researchees = models.ManyToManyField(
        "Profile", through="ResearcheeResearch", null=True
    )
    STATUS_CHOICES = (
        ("EXP", "EXPIRED"),
        ("RCR", "RECRUITING"),
        ("PRE", "PREPARING"),
        ("FUL", "FULL"),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    location = models.TextField()
    images = ArrayField(models.ImageField(), size=4)

    class Meta:
        ordering = ["-hit"]

    def __str__(self):
        return self.title

    def get_status(self):
        now = datetime.now()
        if now < self.recruit_start:
            self.status = "PRE"
        elif now < self.recruit_end and self.current_number < self.capacity:
            self.status = "RCR"
        elif now < self.recruit_end:
            self.status = "FUL"
        else:
            self.status = "EXP"


class ResearcheeResearch(models.Model):
    researchee = models.ForeignKey(Profile, on_delete=models.CASCADE)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)


class Notice(models.Model):
    research = models.ForeignKey(
        Research, on_delete=models.CASCADE, related_name="notices", null=True
    )
    title = models.CharField(max_length=256)
    body = models.TextField()
    image = models.ImageField(
        blank=True, height_field=None, width_field=None, max_length=None
    )


class Reward(models.Model):
    research = models.OneToOneField(
        Research, on_delete=models.CASCADE, related_name="reward", null=True
    )
    reward_type = models.CharField(max_length=50)
    amount = models.IntegerField()


class TagResearch(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)


class Tag(models.Model):
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
    tag_name = models.CharField(max_length=14, choices=TAG_CHOICES)


class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)


class Ask(models.Model):
    research = models.ForeignKey(
        Research, on_delete=models.CASCADE, related_name="asks", null=True
    )
    asker = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="asks", null=True
    )
    content = models.TextField()
    private = models.BooleanField(default=False)


class Answer(models.Model):
    ask = models.ForeignKey(Ask, on_delete=models.CASCADE, related_name="answers")
    content = models.TextField()
