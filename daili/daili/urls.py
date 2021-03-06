#coding=utf-8
"""daili URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^user/", include('tiantian.urls')),
    url(r"^", include('tiantian_page.urls')),
    url(r'^cart/', include('tiantian_cart.urls')),
    url(r'^tiantian_order/', include('tiantian_order.urls')),

# 或直接包含到此ｈａｙｓｔａｃｋ框架中使用默认的上下文，不用写ｇｏｏｄｓｖｉｅｗｓ与额外添加上下文试图
    # url(r'^search/', include('haystack.urls'))
]
