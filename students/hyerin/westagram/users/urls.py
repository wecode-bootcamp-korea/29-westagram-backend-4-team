from django.urls import path
from users.views import SignupView, SigninView

urlpatterns = [
    # 127.0.0.1:8000/users
    path('', SignupView.as_view()),
    path('', SigninView.as_view()),
]