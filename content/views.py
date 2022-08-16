from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import Feed

class Main(APIView):
    def get(self, request):

        feed_list = Feed.objects.all()

        # for feed in feed_list:
        #     print(feed.content)

        return render(request, "instagram/main.html", context={"feeds":feed_list})
