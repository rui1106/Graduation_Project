from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from apps.users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """注册序列化器"""
    sms_code = serializers.CharField(label="验证码", write_only=True)
    token = serializers.CharField(label="token", read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone', 'sms_code', 'token']
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
                "max_length": 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate(self, attrs):
        redis_conn = get_redis_connection("verify_codes")
        mobile = attrs['phone']
        print(mobile)
        real_sms_code = redis_conn.get("sms_%s" % mobile)
        print(real_sms_code)

        if real_sms_code is None or attrs['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError("验证码错误")

        return attrs

    def create(self, validated_data):
        del validated_data["sms_code"]
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        # print(token)

        return user
