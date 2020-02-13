from django.urls import path

from services.views import ListView

urlpatterns = [
    path('list', ListView.as_view(), name='service list'),
]
