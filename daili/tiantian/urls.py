from django.conf.urls import url, include
import views


urlpatterns = [

    url(r"^register$", views.register),
    url(r"^registerhland", views.registerhland),
    url(r"^login$", views.login),
    url(r"^register_judge/", views.register_judge),
    url(r"^loginhland", views.login_hland),
    url(r"^info", views.info),
    url(r"^order", views.order),
    url(r"^site", views.site),
    url(r"^logout",views.logout)

]
