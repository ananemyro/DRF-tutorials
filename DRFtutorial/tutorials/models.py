from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=30, blank=False, default='')
    level = models.CharField(max_length=30, blank=False, default='')

    # def __str__(self):
    #     return f"{self.name} ({self.level})"


class Teacher(models.Model):
    first_name = models.CharField(max_length=70, blank=False, default='')
    last_name = models.CharField(max_length=70, blank=False, default='')
    skills = models.ManyToManyField(Skill)


class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
