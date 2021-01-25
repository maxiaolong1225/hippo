from django.urls import path,include,re_path
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token,verify_jwt_token


urlpatterns = [
    path('login/', obtain_jwt_token),
    path('verify/', refresh_jwt_token ), # 校验并生成新的token
    # path('verify/',verify_jwt_token ), # 只校验token
]