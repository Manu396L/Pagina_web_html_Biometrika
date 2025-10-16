from django.urls import path
from . import views

app_name='crud'

urlpatterns = [
    path('', views.task_list_and_create, name='crud_list'),
    path('update_task/<int:task_id>', views.update_nombre_empleado, name='update_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    
    path('edificios/', views.listar_edificios, name='listar_edificios'),
    path('edificios/crear/', views.crear_edificio, name='crear_edificio'),
    path('edificios/editar/<int:pk>/', views.editar_edificio, name='editar_edificio'),
    path('edificios/eliminar/<int:pk>/', views.eliminar_edificio, name='eliminar_edificio'),
]