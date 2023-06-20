from django.contrib import admin

# Register your models here.

from gitlab.models import GitLab

admin.site.register(GitLab)