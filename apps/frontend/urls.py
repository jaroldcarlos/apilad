from django.urls import path
from apps.backend.views import activate
from . import views

app_name = "frontend"

urlpatterns = [
    path('listado-de-eventos/', views.event_list, name='event_list'),
    path('<slug:slug>.html', views.PageDetailView.as_view(), name='page'),
    path('evento/<slug>.html', views.event_detail, name='event_detail'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('proyecto/igualarte-teatro-e-inclusion.html', views.project_igualarte_teatro, name='project_igualarte_teatro'),
    path('asociacion/latramoya.html', views.latramoya_view , name='latramoya_view'),
    path('quienes-somos/organigrama.html', views.organigramme_view, name='organigramme_view'),
    path('quienes-somos/equipo-profesional.html', views.team_professional_view, name='team_professional_view'),
    path('quienes-somos/colaboradores.html', views.team_volunteer_view, name='team_volunteer_view'),
    path('', views.home, name='home'),
]

