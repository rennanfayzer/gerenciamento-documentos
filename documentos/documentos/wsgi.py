import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "documentos.settings")
application = get_wsgi_application()

# ---- Início da adição WhiteNoise ----
from whitenoise import WhiteNoise
from django.conf import settings

application = WhiteNoise(
    application,
    root=settings.STATIC_ROOT,
    prefix='static/',
)
# ---- Fim da adição WhiteNoise ----
