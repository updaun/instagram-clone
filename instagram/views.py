from django.shortcuts import render
from rest_framework.views import APIView
import os

class Sub(APIView):
    def get(self, request):
        print("GET method!!")
        return render(request, "instagram/main.html")

    def post(self, request):
        print("POST method!!")
        return render(request, "instagram/main.html")