from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from .models import Feed
import os
from instagram.settings import MEDIA_ROOT

from user.models import User

class Main(APIView):
    def get(self, request):

        feed_list = Feed.objects.all().order_by('-id')

        # for feed in feed_list:
        #     print(feed.content)

        # 세션 정보 확인 (세션 초기화시 keyerror 발생)
        # print('로그인한 사용자 :', request.session['email'])
        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        return render(request, "instagram/main.html", context={"feeds":feed_list, "user":user})


class UploadFeed(APIView):
    def post(self, request):

        file = request.FILES['file']

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # 필요 없어짐
        # image = request.data.get('image')
        image = uuid_name
        content = request.data.get('content')
        user_id = request.data.get('user_id')
        profile_image = request.data.get('profile_image')

        Feed.objects.create(image=image,
                            content=content,
                            user_id=user_id,
                            profile_image=profile_image,
                            like_count=0)

        return Response(status=200)