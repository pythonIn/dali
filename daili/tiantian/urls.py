from django.conf.urls import url, include
import views


urlpatterns = [
    url(r"^$",views.register),
    url(r"^user/register$", views.register),
    url(r"^user/registerhland", views.registerhland),
    url(r"^user/login$", views.login),
    url(r"^user/register_judge/", views.register_judge),
    url(r"^user/loginhland", views.login_hland),
    url(r"^user/info", views.info),
    url(r"^user/order", views.order),
    url(r"^user/site", views.site)

]
