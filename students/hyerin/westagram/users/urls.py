from django.urls import path

urlpatterns = [
    path('/signin', SigninView.as_view())
]