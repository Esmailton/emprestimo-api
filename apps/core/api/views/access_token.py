from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


class GenerateTokenView(APIView):
    def get(self, request):
        username = fake.user_name()
        password = fake.password()
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
