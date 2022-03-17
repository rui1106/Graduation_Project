from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.index.serializers import IndexSerializer
from apps.jobs.models import JobInfo


class ShowIndexView(ListAPIView):
    serializer_class = IndexSerializer

    def get_queryset(self):
        return JobInfo.objects.all()


class ShowDetail(APIView):
    def get(self, request, id):
        job = JobInfo.objects.get(id=id)
        work = {
            "id": job.id,
            "name": job.name,
            "salary": job.salary,
            "location": job.location,
            "company": job.company,
            "degree_required": job.degree_required,
            "number": job.number,
            "request": job.request
        }

        return JsonResponse({"code": 0, "message": "OK", "work": work})
