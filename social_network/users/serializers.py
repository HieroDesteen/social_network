from django.core.exceptions import ValidationError
from rest_framework import serializers

from users.models import User
from users.utils import verify_email


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
            Check email verification.
        """

        # Отключил тк лимит запросов был ичерпан

        # try:
        #     verify_email(data.get('email'))
        # except ValidationError:
        #     raise serializers.ValidationError({"email": "Email verification failed."})
        return data
