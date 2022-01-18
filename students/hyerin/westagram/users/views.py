import json

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SigninView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            # if (data["email"] == "") or (data["password"] == ""):
            #     return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if not User.objects.filter(email=email, password=password).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'massage': 'KEY_ERROR'}, status=400)