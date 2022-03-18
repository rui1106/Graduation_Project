import json

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.users.models import Collection_job


class ShowCollect(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        page = request.GET.get("page")
        page_size = request.GET.get("page_size")
        print(user_id, page, page_size)
        u_works = []
        try:
            users = Collection_job.objects.filter(users_id=user_id)
            print(users)
            for user in users:
                # print('1111111111111', user)
                u_works.append(user.jobs)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "message": "获取失败"})
        paginator = Paginator(u_works, page_size)
        # print(paginator)
        try:
            page_works = paginator.page(page)
        except EmptyPage:
            # 如果page_num不正确，默认给用户400
            return JsonResponse({'code': 400,
                                 'message': 'page数据出错'})
        total_page = paginator.num_pages
        print(page_works, total_page)
        works = []
        for work in page_works:
            works.append({
                "id": work.id,
                "name": work.name,
                "salary": work.salary,
                "location": work.location,
                "company": work.company,
                "degree_required": work.degree_required,
                "number": work.number,
            })
        return JsonResponse({"code": 0, "message": "OK", "results": works, 'count': total_page})
