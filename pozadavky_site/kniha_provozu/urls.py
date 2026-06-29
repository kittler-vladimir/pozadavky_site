from django.urls import path
from . import views

app_name = 'kniha_provozu'

urlpatterns = [
    path('', views.zaznam_list, name='zaznam_list'),
    path('novy/', views.zaznam_create, name='zaznam_create'),
    path('<int:zaznam_id>/', views.zaznam_detail, name='zaznam_detail'),
    path('<int:zaznam_id>/upravit/', views.zaznam_update, name='zaznam_update'),
]
