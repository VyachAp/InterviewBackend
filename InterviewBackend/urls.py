"""InterviewBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from interview.api.user import UserLogin, UserVerify, UserDetail
from news_aggregator.views import scrape, parse_zp
from interview.urls import router


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("scrape/", scrape, name="scrape"),
    path("user/<int:id>/", UserDetail.as_view(), name='user'),
    path('login/', UserLogin.as_view(), name='login'),
    path('verify/', UserVerify.as_view(), name='verify'),
    path('parse_zp/', parse_zp, name="parse_zp")
]
