"""
WSGI config for td_biblio sandbox.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandbox.settings')

application = get_wsgi_application()
