import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignInView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:
            user_email    = user_data["email"]
            user_password = user_data["password"].encode('utf-8')

            user = User.objects.get(email = user_email)

            if not bcrypt.checkpw(
                user_password, 
                user.password.encode('utf-8')
                ):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            access_token = jwt.encode({"user_id": user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({"access_token": access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

class SignUpView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:          
            user_email        = user_data["email"]
            user_password     = user_data["password"]
            user_phone_number = user_data["phone_number"]

            REGEX_EMAIL        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&.]{8,}$'
            REGEX_PHONE_NUMBER = '\d{3}-\d{3,4}-\d{4}'

            if not re.match(REGEX_EMAIL, user_email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)
            if not re.match(REGEX_PASSWORD, user_password):
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
            if not re.match(REGEX_PHONE_NUMBER, user_phone_number):
                return JsonResponse({"message": "INVALID_PHONE_NUMBER"}, status=400)
            if User.objects.filter(email=user_email).exists():
                return JsonResponse({"message": "EMAIL_ALREADY_EXISTS"}, status=400)

            encoded_password         = user_password.encode('utf-8')
            salt                     = bcrypt.gensalt()
            decoded_hashed_password  = bcrypt.hashpw(encoded_password, salt).decode('utf-8')

            user = User(
                name         = user_data["name"],
                email        = user_email,
                password     = decoded_hashed_password,
                phone_number = user_phone_number
            )

            user.save()
            return JsonResponse({"message": "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)