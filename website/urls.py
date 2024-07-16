from django.urls import path

from website import views

# http://127.0.0.1:8000/


urlpatterns = [
    path('', views.send_data, name='send_data')
]

