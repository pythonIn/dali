from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^cart$',views.cart),
    url(r"^add(\d+)_(\d+)$", views.add),
    url(r'^mend(\d+)_(\d+)$', views.mend),
    url(r'^cart_del(\d+)$', views.cart_del)
]
