"""
Web Server Gateway Interface:
simple calling convention for web servers to forward requests to web applications or frameworks written in the Python.

WSGI config for DRFtutorial project: exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DRFtutorial.settings")

application = get_wsgi_application()
