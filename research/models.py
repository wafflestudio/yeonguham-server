from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Researchee, Researcher

# Create your models here.
class Research(models.Model):
    subject = models.CharField(max_length=20, blank=False, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    recruit_start = models.DateTimeField(auto_now=False, auto_now_add=False)
    recruit_end = models.DateTimeField(auto_now=False, auto_now_add=False)
    researchStart = models.DateTimeField(auto_now=False, auto_now_add=False)
    researchEnd = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    detail = models.TextField()
    requirement = models.TextField()
    capacity = models.IntegerField()
    current_number = models.IntegerField(default=0)
    researcher = models.ForeignKey(
        Researcher, on_delete=models.CASCADE, related_name="researches"
    )
    tag = models.ManyToManyField(
        "Tag", blank=True, related_name="researches", through="TagResearch"
    )
    mark_users = models.ManyToManyField(
        User, blank=True, related_name="marked_research", through="Mark"
    )
    researchees = models.ManyToManyField(
        "accounts.Researchee", through="ResearcheeResearch"
    )
    STATUS_CHOICES = (("EXP", "EXPIRED"), ("RCR", "RECRUITING"), ("PRE", "PREPARING"))
    status = models.TextField(choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

    def get_status(self):
        now = datetime.now()
        if now < self.recruit_start:
            self.status = "PRE"
        elif now < self.recruit_end:
            self.status = "RCR"
        else:
            self.status = "EXP"


class ResearcheeResearch(models.Model):
    researchees = models.ForeignKey(Researchee, on_delete=models.CASCADE)
    researches = models.ForeignKey(Research, on_delete=models.CASCADE)


class Notice(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    body = models.TextField()
    image = models.ImageField(
        blank=True, height_field=None, width_field=None, max_length=None
    )


class Reward(models.Model):
    research = models.OneToOneField(Research, on_delete=models.CASCADE)
    reward_type = models.CharField(max_length=50)
    amount = models.IntegerField()


class TagResearch(models.Model):
    researches = models.ForeignKey(Research, on_delete=models.CASCADE)
    tags = models.ForeignKey("Tag", on_delete=models.CASCADE)


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)


class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    research = models.ForeignKey("Research", on_delete=models.CASCADE)
