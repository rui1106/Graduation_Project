from django.urls import path

from apps.jobs.views import ShowCollect

urlpatterns = [
    path('showcollect/', ShowCollect.as_view()),
]
