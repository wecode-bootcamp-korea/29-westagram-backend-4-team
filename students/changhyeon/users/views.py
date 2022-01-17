import json
from django.shortcuts       import render
from django.http            import JsonResponse
from django.views           import View
from .validate              import validate_email, validate_password
from users.models           import Users
from django.core.exceptions import ValidationError 

class SignupView(View):
  def post(self,request):
    data = json.loads(request.body) #python dictionary

    try:
      name         = data["name"]
      email        = data["email"]
      password     = data["password"]
      phone_number = data["phone_number"]

      validate_email(email) #이메일 검사
      validate_password(password) #비밀번호 검사

      if Users.objects.filter(email = email).exists(): 
        return JsonResponse({"message": "EMAIL_AREADY_EXISTS"}, status=400)

      user = Users.objects.create(
        name         =  name,
        email        =  email,
        password     = password,
        phone_number = phone_number,
      )

      return JsonResponse({"message": "SUCCESS"}, status =201)

    except KeyError: 
      return JsonResponse({"message": "KEY_ERROR"}, status=400)

    except ValidationError:
      return JsonResponse({"message": "KEY_ERROR"}, status=400)

