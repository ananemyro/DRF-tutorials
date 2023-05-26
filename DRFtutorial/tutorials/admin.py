from django.contrib import admin
from .models import Skill, Teacher, Tutorial


# Register models with the Django admin interface


class SkillAdmin(admin.ModelAdmin):
    model = Skill
    list_display = ['name', 'level']


class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ['first_name', 'last_name']


class TutorialAdmin(admin.ModelAdmin):
    model = Tutorial
    list_display = ['title', 'description', 'published', 'teacher']


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Skill, SkillAdmin)