from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def test_db_connection(request):
    try:
        with connections['Mysql'].cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return HttpResponse(f"Database connection successful: {result[0]}")
    except Exception as e:
        return HttpResponse(f"Database connection failed: {e}")

# Create your views here.