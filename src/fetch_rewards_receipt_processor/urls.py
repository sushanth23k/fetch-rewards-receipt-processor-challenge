from django.urls import path
from . import views

urlpatterns = [
    path("process_receipt_auth/", views.process_receipt_authentication_authorization, name="process_receipt_auth"),
    path("get_receipt_points_auth/<str:id>/", views.get_receipt_points_authentication_authorization, name="get_receipt_points_auth"),
    path("process_receipt/", views.process_receipt_unauthentication_unauthorization, name="process_receipt"),
    path("get_receipt_points/<str:id>/", views.get_receipt_points_unauthentication_unauthorization, name="get_receipt_points"),
]