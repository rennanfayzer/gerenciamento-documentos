from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # CRUD de Funcionários
    path('funcionarios/', views.funcionario_list, name='funcionario_list'),
    path('funcionarios/novo/', views.funcionario_create, name='funcionario_create'),
    path('funcionarios/<int:pk>/editar/', views.funcionario_update, name='funcionario_update'),
    path('funcionarios/<int:pk>/excluir/', views.funcionario_delete, name='funcionario_delete'),
    path('funcionarios/<int:funcionario_id>/', views.funcionario_detail, name='funcionario_detail'),

    # CRUD de Locais
    path('locais/', views.local_list, name='local_list'),
    path('locais/novo/', views.local_create, name='local_create'),
    path('locais/<int:pk>/editar/', views.local_update, name='local_update'),
    path('locais/<int:pk>/excluir/', views.local_delete, name='local_delete'),

    # CRUD de Documentos
    path('funcionarios/<int:funcionario_id>/documento/novo/', views.documento_create, name='documento_create'),
    path('documento/<int:documento_id>/editar/', views.documento_update, name='documento_edit'),
    path('documento/<int:documento_id>/excluir/', views.documento_delete, name='documento_delete'),

    # CRUD de Gestores Locais
    path('gestores/', views.gestor_list, name='gestor_list'),
    path('gestores/novo/', views.gestor_create, name='gestor_create'),
    path('gestores/<int:pk>/editar/', views.gestor_update, name='gestor_update'),
    path('gestores/<int:pk>/excluir/', views.gestor_delete, name='gestor_delete'),

    path('no_permission/', views.no_permission, name='no_permission'),

    path('logs/', views.logs_view, name='logs_view'),

    path('funcionarios/exportar/pdf/', views.export_funcionarios_pdf, name='export_funcionarios_pdf'),
    path('documentos/exportar/pdf/', views.export_documentos_pdf, name='export_documentos_pdf'),
    path('funcionarios/exportar/excel/', views.export_funcionarios_excel, name='export_funcionarios_excel'),
    path('documentos/exportar/excel/', views.export_documentos_excel, name='export_documentos_excel'),

    path('busca-avancada/', views.advanced_search, name='advanced_search'),
    path('get-filtered-dashboard-data/', views.get_filtered_dashboard_data, name='get_filtered_dashboard_data'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('alertas/', views.alertas, name='alertas'),

    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
]
