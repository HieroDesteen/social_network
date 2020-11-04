from django.urls.conf import path
from rest_framework_jwt.views import obtain_jwt_token

from users.views import CreateUserAPIView, authenticate_user

urlpatterns = [
    path('signup/', CreateUserAPIView.as_view()),
    path('login/', authenticate_user),
]
