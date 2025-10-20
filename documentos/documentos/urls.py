from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from gestao_docs.api import DocumentoViewSet, FuncionarioViewSet, LocalMobilizacaoViewSet

router = DefaultRouter()
router.register(r'documentos', DocumentoViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'locais', LocalMobilizacaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestao_docs.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Sistema de login
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
