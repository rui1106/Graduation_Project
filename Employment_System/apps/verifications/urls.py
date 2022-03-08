from django.urls import path

from apps.verifications.views import SMSCodeView

urlpatterns = [
    path('sms_codes/<mobile>/', SMSCodeView.as_view()),
]