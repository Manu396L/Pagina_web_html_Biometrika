from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'usuario'  # esto habilita el namespace 'usuario:login'

urlpatterns = [ 
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.logged_out, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('ubicaciones/', views.ubicaciones_view, name='ubicaciones'),
    path('personal/', views.gestion_personal, name='gestion_personal'),
    path('personal/<int:id>/editar/', views.editar_personal, name='editar_personal'),
    path('register/personal/', views.register_personal, name='register_personal'),
    path('alertas/', views.alertas_view, name='alertas'),
    path('dispositivos/', views.dispositivos, name='dispositivos'),


    
    path('password-change/',auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)