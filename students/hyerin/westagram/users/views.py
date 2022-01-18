import json
import re

from django.http import JsonResponse
from django.views import View

from users.models import User

# Create your views here.
class SignupView(View):
    def post(self, request):
        try: #예외처리
            data = json.loads(request.body)

            if (data["email"] == "") or (data["password"] == ""):
                return JsonResponse({"message": "ERROR_EMPTY_EMAIL_OR_PASSWORD"}, status=400)
            if re.match(r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data["email"]) == None:
                return JsonResponse({"message": "ERROR_EMAIL_NEED_@AND."}, status=400)
            if re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", data["password"]) == None:
                return JsonResponse({"message": "ERROR_REQUIRE_8_LETTER,NUMBER,SPECIAL_SYMBOLS)"}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "ERROR_EMAIL_ALREADY_EXIST"}, status=400)

            #이렇지 않은 경우 데이터 저장.
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number'],
            )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError: #try-except 예외처리
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class SigninView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)

            if (data["email"] == "") or (data["password"] == ""):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            if not User.objects.filter(password=data['password']):
                return JsonResponse({'massage': 'INVALID_USER'}, status=401)
            if User.objects.filter(email=data['email']) and User.objects.filter(password=data['password']):
                return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'massage': 'KEY_ERROR'}, status=400)