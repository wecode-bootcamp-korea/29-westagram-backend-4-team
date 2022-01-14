from django.urls import path
from .views      import SignupView #SinginView

urlpatterns = {
  path('signup', SignupView.as_view()),
  # path("signin", SignInView.as_view()),
}