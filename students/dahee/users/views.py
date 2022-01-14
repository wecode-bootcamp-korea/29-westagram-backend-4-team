import json
import re

from django.db import IntegrityError
from django.http import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:
            user = User(
                name = user_data["name"],
                email = user_data["email"],
                password = user_data["password"],
                phone_number = user_data["phone_number"]
            )
            
            email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$')
            password_validation = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&.]{8,}$')
            phone_number_validation = re.compile(r'\d{3}-\d{3,4}-\d{4}')
            
            if not email_validation.search(user_data["email"]):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            if not password_validation.search(user_data["password"]):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            if not phone_number_validation.search(user_data["phone_number"]):
                return JsonResponse({"message": "INVALID_PHONE_NUMBER"}, status=400)
                
            user.save()
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except IntegrityError:
            return JsonResponse({"message": "EMAIL_ALREADY_EXISTS"}, status=400)
        else:
            return JsonResponse({"message": "SUCCESS"}, status=201)