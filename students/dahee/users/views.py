import json

from django.http import JsonResponse
from django.views import View

from users.models import User

class SignInView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        try:
            user_email    = user_data["email"]
            user_password = user_data["password"]

            if not User.objects.filter(email=user_email).exists() \
                or not User.objects.filter(password=user_password).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            return JsonResponse({"message": "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)