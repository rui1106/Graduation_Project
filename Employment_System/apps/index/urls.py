from django.urls import path

from apps.index.views import ShowIndexView, ShowDetail

urlpatterns = [
    path('showindex/', ShowIndexView.as_view()),
    path('showservice/', ShowIndexView.as_view()),
    path('detail/<id>/', ShowDetail.as_view())
]
