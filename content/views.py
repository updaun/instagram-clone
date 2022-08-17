from uuid import uuid4

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
import os
from instagram.settings import MEDIA_ROOT

from content.models import Feed, Like, Reply, Bookmark
from user.models import User

class Main(APIView):
    def get(self, request):

        feed_object_list = Feed.objects.all().order_by('-id')

        feed_list = []

        for feed in feed_object_list:
            user = User.objects.filter(email=feed.email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(reply_content=reply.reply_content,
                                       nickname=user.nickname))
            feed_list.append(dict(
                id=feed.id,
                image=feed.image,
                content=feed.content,
                like_count=feed.like_count,
                profile_image=user.profile_image,
                nickname=user.nickname,
                reply_list = reply_list
            ))

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
        email = request.session.get('email', None)
       
        Feed.objects.create(image=image,
                            content=content,
                            email=email,
                            like_count=0)

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        
        email = request.session.get('email', None)
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        return render(request, 'content/profile.html', {"user":user})



class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get('feed_id', None)
        reply_content = request.data.get('reply_content', None)
        email = request.session.get('email', None)

        Reply.objects.create(feed_id=feed_id,
                             reply_content=reply_content,
                             email=email)
        
        return Response(status=200)