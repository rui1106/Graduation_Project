import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from apps.users.models import User, Collection_job
from apps.users.serializers import CreateUserSerializer


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