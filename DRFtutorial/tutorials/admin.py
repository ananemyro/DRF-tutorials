from django.contrib import admin
from .models import Skill, Teacher, Tutorial

class SkillAdmin(admin.ModelAdmin):
    model = Skill
    list_display = ['name', 'level']


class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ['first_name', 'last_name']


class TutorialAdmin(admin.ModelAdmin):
    model = Tutorial
    list_display = ['title', 'description', 'published', 'teacher']
    # list_display = ['title', 'description', 'published']


admin.site.register(Tutorial, TutorialAdmin)  # register models with the Django admin interface
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Skill, SkillAdmin)