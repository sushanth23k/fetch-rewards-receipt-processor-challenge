from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.db import connections
import requests
import os
from json import dumps,loads

# Create your views here.
