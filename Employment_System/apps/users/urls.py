from django.urls import path, register_converter
from rest_framework_jwt.views import obtain_jwt_token

from apps.users import login
from apps.users.views import UsernameCountView, MobileCountView, UserView, Collect, CancelCollect

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile>/count/', MobileCountView.as_view()),
    path('register/', UserView.as_view()),
    path('authorizations/', login.admin_jwt_token),
    path('collect/', Collect.as_view()),
    path('cancelcollect/', CancelCollect.as_view())
]
