from django.db import models

# create relations between models

class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)
    teacher = models.CharField(max_length=70, blank=False, default='')

# /tutorials (return the list of tutorials + first, last name of teacher) GET -- (to test)


class Teacher(models.Model):
    first_name = models.CharField(max_length=70, blank=False, default='')
    last_name = models.CharField(max_length=70, blank=False, default='')
    skill = models.CharField(max_length=30, blank=False, default='')

# /teachers (returns the list of teachers, all attributes) (authenticated) GET
# /teachers (returns list of teachers, name ONLY) (no authentication) GET


class Skill(models.Model):
    name = models.CharField(max_length=30, blank=False, default='')
    level = models.CharField(max_length=30, blank=False, default='')

# /skills (add new skills) (authenticated) POST -- (to test)
# /skills (returns list of skills) (no authentication) GET -- (to test)
