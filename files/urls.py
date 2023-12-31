from django.urls import path
from .views import index, login_view, logout_view, generate_signed_url

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('generate-signed-url/', generate_signed_url, name='generate_signed_url'),
]