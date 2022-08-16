from django.urls import path
from content.views import UploadFeed

urlpatterns = [
    path('upload', UploadFeed.as_view())
]
