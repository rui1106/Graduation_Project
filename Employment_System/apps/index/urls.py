from django.urls import path

from apps.index.views import ShowIndexView

urlpatterns = [
    path('showindex/', ShowIndexView.as_view()),
    path('showservice/', ShowIndexView.as_view())
]
