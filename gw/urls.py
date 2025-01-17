from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    # 기본적으로 매핑할 때, gw/ url을 매핑하므로 ''를 사용한다.
]