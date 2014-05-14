"""
WSGI config for nextmng project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import newrelic.agent

newrelic.agent.initialize('newrelic.ini')
application = get_wsgi_application()