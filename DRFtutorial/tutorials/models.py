from django.db import models

# TO DO: migrate to postgresql
# new model: Teacher (attributes: first name, last name, skills)
# new model: Skills (attributes: name, level)
# create relationship between models
# tutorials: add attribute teacher

'''
create APIs:
1) /admin/teachers (returns the list of teachers) (authenticated)
/admin/tutorials (return the list of tutorials) (authenticated) (first, last name of teacher)
/admin/skills (add new skills) (authenticated)

2) /teachers (returns list of teachers, last first name ONLY) (no authentication)
/skills (returns list of skills) (no authentication)

'''

class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)
