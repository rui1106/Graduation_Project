from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

from apps.index.serializers import IndexSerializer
from apps.jobs.models import JobInfo


class ShowIndexView(ListAPIView):
    serializer_class = IndexSerializer

    def get_queryset(self):
        return JobInfo.objects.all()