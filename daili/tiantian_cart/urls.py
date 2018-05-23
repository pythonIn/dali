from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^cart$',views.cart),
    url(r"^add(\d+)_(\d+)$", views.add)
]
