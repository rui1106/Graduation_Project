import hashlib
import json
import os
import re
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from apps.users.models import User, Collection_job
from apps.users.serializers import CreateUserSerializer, UserSerializer
from utils.image_qiniu import upload_image_to_qiniu


class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = CreateUserSerializer


class UsernameCountView(APIView):
    """
    用户名数量
    """

    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()
        data = {
            'username': username,
            'count': count
        }

        return JsonResponse(data)


class MobileCountView(APIView):
    """判断手机号是否已注册"""

    def get(self, request, mobile):
        # 查询数据库
        count = User.objects.filter(phone=mobile).count()
        # 构造响应数据
        data = {
            'mobile': mobile,
            'count': count
        }
        # 响应
        return Response(data)


class Collect(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.body
        data_dict = json.loads(data)
        job_id = data_dict.get("job_id")

        try:
            Collection_job.objects.create(jobs_id=job_id, users_id=user_id)
        except Exception as e:
            print(e)
            return Response({"code": 400, "errmsg": "收藏失败"})
        return JsonResponse({"code": 0, "message": "收藏成功"})


class CancelCollect(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.body
        data_dict = json.loads(data)
        job_id = data_dict.get("job_id")

        try:
            job = Collection_job.objects.get(jobs_id=job_id, users_id=user_id)
            job.delete()
        except Exception as e:
            print(e)
            return Response({"code": 400, "errmsg": "取消收藏失败"})
        return JsonResponse({"code": 0, "message": "取消收藏成功"})


class GetCenter(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)


class Upload(APIView):
    def post(self, request):
        image = request.FILES.get("file")
        print(image)

        file_hash = hashlib.md5()
        file_hash.update((image.name + time.ctime()).encode("utf-8"))
        file_name = file_hash.hexdigest() + image.name[image.name.rfind('.'):]
        # avatar_url = file_name
        path_file_name = './upload/' + file_name
        print(path_file_name)
        print(os.getcwd())
        # 用新的随机的名字当作图片的名字
        # image.save(path_file_name)
        with open(path_file_name, 'wb') as f1:
            for i in image.chunks():
                f1.write(i)
        # 将图片上传到七牛云
        qiniu_avatar_url = upload_image_to_qiniu(path_file_name, file_name)
        print(qiniu_avatar_url)
        print(file_name)
        print(image)

        return JsonResponse({"code": 0, "file_url": qiniu_avatar_url})


class ChangeImg(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        data = request.body
        data_dict = json.loads(data)
        file_url = data_dict.get("file_url")
        try:
            user = User.objects.get(id=user_id)
            user.avatar_url = file_url
            user.save()
            return JsonResponse({"code": 0, "message": "OK", "avatar_url": user.avatar_url})
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "message": "修改失败"})


# 修改个人信息
class ChangeInfo(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_id = request.user.id
        data = request.body
        data_dict = json.loads(data)
        username = data_dict.get("username")
        phone = data_dict.get("phone")
        email = data_dict.get("email")
        sex = data_dict.get("sex")
        # print(user_id, username, phone, email, sex)

        if re.match('1[3-9]\d{9}', phone):
            return JsonResponse({'code': 400, 'errmsg': "手机号格式错误"})

        if not email:
            return JsonResponse({'code': 400, 'errmsg': '邮箱地址不能为空'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400, 'errmsg': '邮箱地址格式错误'})
        try:
            User.objects.filter(id=user_id).update(
                username=username,
                phone=phone,
                email=email,
                sex=sex
            )
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "message": "修改失败"})
        return JsonResponse({"code": 0, "message": "OK"})


class ChangePwd(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # user_id = request.user.id
        data = request.body
        data_dict = json.loads(data)
        password = data_dict.get("old_password")
        new_password = data_dict.get("new_password")
        new_password2 = data_dict.get("new_password2")

        print(password, new_password, new_password2)

        if not all([password, new_password, new_password2]):
            return JsonResponse({"code": 400, "message": "参数不全"})

        result = request.user.check_password(password)
        if not result:
            return JsonResponse({'code': 400,
                                 'message': '原始密码不正确'})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400,
                                 'message': '密码最少8位,最长20位'})

        if new_password != new_password2:
            return JsonResponse({'code': 400,
                                 'message': '两次输入密码不一致'})

        # 修改密码
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 400, 'errmsg': '修改密码失败'})
        return JsonResponse({"code": 0, "message": "OK"})
