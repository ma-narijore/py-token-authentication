from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if len(attrs['password']) <= 5:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Both username and password are required")

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "is_staff", "password")
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True}
        }


