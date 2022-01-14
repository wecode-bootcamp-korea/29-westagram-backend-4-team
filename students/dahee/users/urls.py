from django.urls import path

from users.views import UserView

urlpatterns = [
    path('/sign_up', UserView.as_view()),
]