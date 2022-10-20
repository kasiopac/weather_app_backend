from django.contrib import admin
from django.urls import path, include
from register import views as r_views
from weatherapp import views as w_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", w_views.index, name="index"),
    path("mycity/", w_views.mycity, name="mycity"),
    path("register/", r_views.register, name="register"),
    path("", include("django.contrib.auth.urls")),
]
