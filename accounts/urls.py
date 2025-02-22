from django.urls import path,include
from .views import indexView

from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("logout", LogoutView.as_view(next_page="/"), name="logout"),
    path("login/", indexView, name="authentication"),
    # path("register/", RegisterPage.as_view(), name="register"),
    path("api/v1/",include("accounts.api.v1.urls")),
]