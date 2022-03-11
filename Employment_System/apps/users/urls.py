from django.urls import path, register_converter
from rest_framework_jwt.views import obtain_jwt_token

from apps.users.views import UsernameCountView, MobileCountView, UserView

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile>/count/', MobileCountView.as_view()),
    path('register/', UserView.as_view()),
    path('authorizations/', obtain_jwt_token)
]
