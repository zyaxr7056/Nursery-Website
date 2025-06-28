"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

app = application  # For Vercel compatibility, we assign the WSGI application to 'app'
# This allows Vercel to recognize the WSGI application correctly.
# The 'app' variable is used by Vercel to route requests to the Django application.