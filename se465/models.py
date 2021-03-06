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
    repo = models.CharField(max_length=255)
    coverity_pw = models.CharField(max_length=12)
    def __unicode__(self):
        members = self.members.all()
        member_names = []
        for m in members:
            member_names.append(m.username)
        return "g{0}: {1}".format(self.pk, ' '.join(member_names))
