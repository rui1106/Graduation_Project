from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.index.serializers import IndexSerializer
from apps.jobs.models import JobInfo
from apps.users.models import Collection_job


class ShowIndexView(ListAPIView):
    serializer_class = IndexSerializer

    def get_queryset(self):
        return JobInfo.objects.all()


class ShowDetail(APIView):
    def get(self, request, pk):
        user_id = request.user.id
        # print('11111111111111111111', user_id)
        job = JobInfo.objects.get(id=pk)
        try:
            j = Collection_job.objects.filter(users_id = user_id, jobs_id=job.id)
            if j:
                collection = False
            else:
                collection = True
        except Exception as e:
            print(e)
            return JsonResponse({"code": 400, "message": "查询失败"})
        work = {
            "id": job.id,
            "name": job.name,
            "salary": job.salary,
            "location": job.location,
            "company": job.company,
            "degree_required": job.degree_required,
            "number": job.number,
            "request": job.request,
            "collection": collection
        }

        return JsonResponse({"code": 0, "message": "OK", "work": work})
