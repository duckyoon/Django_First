"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from gw import views

#from gw import views

urlpatterns = [
    # path() 는 url과 뷰를 매핑하는 장고의 함수
    # path(url 경로, 호출할 뷰 함수)
    path("admin/", admin.site.urls),
    
    # gw/ url이 요청되면 views.index를 호출하라는 매핑을 추가
    # viwes.index는 views.py 파일의 index함수를 의미
    #path("gw/", views.index), # 경로를 설정하면 해당 views.py 파일에 index 함수를 추가해야함.
    
    path('gw/', include('gw.urls')),
    
    # [url 분리]
    # from gw import views
    # path("gw/", views.index)
    # 위의 방법은 url 매핑을 추가할 때마다 config/urls.py 파일을 수정해야 한다.
    # 해당 파일은 프로젝트 전반적은 url을 관리하는 파일로, 앱별 url은 url 분리하여 별도로 관리한다.
    # => include 사용
    
    # path('gw/', include('gw.urls'))
    # gw/로 시작하는 페이지를 요청하면 gw/urls.py 파일의 매핑 정보를 읽어서 처리하게 함.
    # gw내에 urls.py 파일을 생성한다.
    
    path('common/', include('common.urls')),
    
    path('', views.index, name='index') # '/'에 해당하는 path 설정
]
