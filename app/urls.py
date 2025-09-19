from django.urls import path
from . import views

urlpatterns = [
    path('agent/<str:agent_name>/', views.agent_symbols_api, name='agent_symbols_api'),
]