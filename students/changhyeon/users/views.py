import json
from django.shortcuts       import render
from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError 
from .validate              import validate_email, validate_password
from users.models           import Users

class SignupView(View):
  def post(self,request):
    data = json.loads(request.body) 

    try:
      name         = data["name"]
      email        = data["email"]
      password     = data["password"]
      phone_number = data["phone_number"]

      validate_email(email)       
      validate_password(password) 

      if Users.objects.filter(email = email).exists(): 
        return JsonResponse({"message": "EMAIL_AREADY_EXISTS"}, status=400)

      user = Users.objects.create(
        name         = name,
        email        = email,
        password     = password,
        phone_number = phone_number,
      )

      return JsonResponse({"message": "SUCCESS"}, status =201)

    except KeyError: 
      return JsonResponse({"message": "KEY_ERROR"}, status=400)

    except ValidationError:
      return JsonResponse({"message": "INVALID_ERROR"}, status=400)


class SigninView(View):
  def post(self,request):
    data = json.loads(request.body)
    try:
      email    = data["email"]
      password = data["password"]

      if not Users.objects.filter(email = email, password = password).exists(): 
        return JsonResponse({"message": "INVALID_USER"}, status = 401)

      return JsonResponse({"message": "SUCCESS"}, status = 200)

    except KeyError:
      return JsonResponse({"message": "KEY_ERROR"}, status = 400)
