from django.urls import path
from apps.backend.views import activate
from . import views

app_name = "backend"

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('users/list', views.Users_List.as_view(), name='users_list'),
    path('users/create', views.Users_Create.as_view(), name='users_create'),
    path('users/update/<pk>', views.Users_Update.as_view(), name='users_update'),
    path('users/change-password', views.change_password, name='users_change_password'),
    path('users/delete/<pk>', views.Users_Delete.as_view(), name='users_delete'),
]
