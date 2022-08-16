from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# Create your models here.

class User(AbstractBaseUser):
    '''
        유저 프로파일 사진
        유저 닉네임      -> 화면에 표기되는 이름
        유저 이름        -> 실제 이름
        유저 이메일 주소 -> 회원가입할 때 사용하는 아이디
        유저 비밀번호    -> 디폴트 사용
    '''

    profile_image = models.TextField() # 프로필 이미지
    nickname = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'nickname'

    class Meta:
        # 테이블 명 정하기 가능
        db_table = 'User'