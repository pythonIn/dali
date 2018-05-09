from django.conf.urls import url, include
import views


urlpatterns = [
    url(r"^$",views.register),
    url(r"^user/register$", views.register),
    url(r"^user/registerhland", views.registerhland),
    url(r"^user/login$", views.login),

]
