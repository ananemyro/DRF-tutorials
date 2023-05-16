from django.contrib import admin
from . import models

admin.site.register(models.Tutorial)  # register models with the Django admin interface
