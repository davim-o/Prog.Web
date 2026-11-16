from django.urls import path, include
from loja.views.AuthView import login_view, register_view, logout_view

urlpatterns = [
    path("login/", login_view, name='login'),
    path("register/", register_view, name='register'),
    path("logout", logout_view, name='logout'),
    # Rota de autenticação por redes sociais (Cap. 12.2)
    path('social-auth/', include('social_django.urls', namespace="social")),
]
