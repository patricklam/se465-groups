from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete

from django_gitolite.models import Repo
from django_ssh.models import Key

class Assignment(models.Model):
    slug = models.SlugField()

class Group(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='groups')
    members = models.ManyToManyField(User, related_name='se465_groups')
    repo = models.ForeignKey(Repo, blank=True, null=True)
