import json, bcrypt, jwt
from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError 
from .validate              import validate_email, validate_password
from users.models           import Users
from my_settings            import SECRET_KEY

class SignupView(View):
  def post(self,request):
    data = json.loads(request.body) 

    try:
      name            = data["name"]
      email           = data["email"]
      password        = data["password"]
      phone_number    = data["phone_number"]
      hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

      validate_email(email)       
      validate_password(password) 

      if Users.objects.filter(email = email).exists(): 
        return JsonResponse({"message": "EMAIL_AREADY_EXISTS"}, status=400)

      user = Users.objects.create(
        name         = name,
        email        = email,
        password     = hashed_password.decode('utf-8'),
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

      if not Users.objects.filter(email = email).exists(): 
        return JsonResponse({"message": "INVALID_USER"}, status = 401)
      
      valid_password = Users.objects.get(email=email).password.encode('utf-8')

      if not bcrypt.checkpw(password.encode('utf-8'), valid_password):
        return JsonResponse({'message': "INVALID_USER"}, status = 401)
      
      access_token = jwt.encode({'email':email}, SECRET_KEY, algorithm='HS256')

      return JsonResponse({"accesS_token": access_token}, status = 200)

    except KeyError:
      return JsonResponse({"message": "KEY_ERROR"}, status = 400)

