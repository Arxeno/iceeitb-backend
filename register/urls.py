from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_multipart),
    path('uploads/<str:team_name>/<str:filename>', views.get_uploads)
]
