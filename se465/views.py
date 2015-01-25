import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from django_gitolite.models import Repo

from se465.models import Assignment, Group
from se465.utils import gitolite_creator_call, is_se465_student

def home(request):
    context = {'accesses': []}
    return render(request, 'home.html', context)

def setup(request):
    return render(request, 'setup.html')

@login_required
def assignment(request, slug):
    username = request.user.username
    c = {'is_student': is_se465_student(username)}
    def validate_partner(p):
        if not p:
            return None
        try:
            partner = User.objects.get(username=p)
        except User.DoesNotExist:
            c['register_error'] = 'Invalid partner (does not exist)'
            return None
        if request.user == partner:
            c['register_error'] = 'Invalid partner (yourself)'
            return None
        if not is_se465_student(partner.username):
            c['register_error'] = 'Invalid partner'
            return None
        try:
            partner.se465_groups.get(assignment=a)
            c['register_error'] = 'Invalid partner (already in group)'
            return None
        except Group.DoesNotExist:
            pass
        return partner
    
    a = get_object_or_404(Assignment, slug=slug)
    if c['is_student']:
        try:
            g = request.user.se465_groups.get(assignment=a)
            gm = g.members.all()
        except Group.DoesNotExist:
            g = None
            gm = None
        c['group'] = g
        c['gm'] = gm

    if request.method == "POST":
        if not c['is_student'] or c['group']:
            return redirect('assignment', 'project')
        if 'partner' in request.POST:
            partner1 = validate_partner(request.POST['username1'])
            partner2 = validate_partner(request.POST['username2'])
            if (partner1 is None) or (request.POST['username2'] and partner2 is None):
                return render(request, 'se465/assignment.html', c)

            g = Group.objects.create(assignment=a)
            g.coverity_pw = User.objects.make_random_password()
            g.members.add(request.user)
            g.members.add(partner1)
            if not (partner2 is None):
                g.members.add(partner2)

            r = 'se465/1151/project/g{}'.format(str(g.pk))
            gitolite_creator_call('fork se465/1151/project {}'.format(r))
            gitolite_creator_call('perms {} + WRITERS {}'.format(r, username))
            gitolite_creator_call('perms {} + WRITERS {}'.format(r, partner1.username))
            if not (partner2 is None):
                gitolite_creator_call('perms {} + WRITERS {}'.format(r, partner2.username))

            g.repo = 'git@ecgit.uwaterloo.ca:{}'.format(r)
            g.save()
            return redirect('assignment', 'project')
        elif 'solo' in request.POST:
            g = Group.objects.create(assignment=a)
            g.coverity_pw = User.objects.make_random_password()
            g.members.add(request.user)
            r = 'se465/1151/project/g{}'.format(str(g.pk))
            gitolite_creator_call('fork se465/1151/project {}'.format(r))
            gitolite_creator_call('perms {} + WRITERS {}'.format(r, username))
            g.repo = 'git@ecgit.uwaterloo.ca:{}'.format(r)
            g.save()
            return redirect('assignment', 'project')

    return render(request, 'se465/assignment.html', c)
