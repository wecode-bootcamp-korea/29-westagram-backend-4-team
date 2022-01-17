import json
from django.shortcuts       import render
from django.http            import JsonResponse
from django.views           import View
from .validate              import validate_email, validate_password
from users.models           import Users
from django.core.exceptions import ValidationError 

class SignupView(View):
  def post(self, request):
    try:
      data         = json.loads(request.body)
      name         = data["name"]
      email        = data["email"]
      password     = data["password"]
      phone_number = data["phone_number"]

      try: #이메일이나 패스워드가 전달되지 않을 경우
        validate_email(email)
        validate_password(password)
      except ValidationError:
        return JsonResponse({"message": "KEY_ERROR"}, status =400)

      if Users.objects.filter(email=email).exists(): # 중복된 email이 존재할 때
        return JsonResponse({"message": "ALREADY_EXISTS"}, status=400)

      Users.objects.create(
        name         = name,
        email        = email,
        password     = password,
        phone_number = phone_number,
        )
      return JsonResponse({"message": "SUCCESS"}, status= 201)

    except:
      return JsonResponse({"message": "KEY_ERROR"}, status = 400)


class SigninView(View):
  def post(self,request):
    data = json.loads(request.body)
    try:
      email = data["email"]
      password= data["password"]
      if not Users.objects.filter(email =email, password= password).exists(): #계정이나 비밀번호를 잘못 입력한 경우
        return JsonResponse({"message": "INVALID_USER"}, status = 401)

      return JsonResponse({"message": "SUCCESS"}, status = 200)

    except:
      return JsonResponse({"message": "KEY_ERROR"}, status = 400)

