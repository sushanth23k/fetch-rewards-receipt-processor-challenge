from django.urls import path
from . import views

urlpatterns = [
    path("test_db_connection/",views.test_db_connection,name="test_db_connection"),
]