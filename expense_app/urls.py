from django.urls import path

from .views import (
    create_expense,
    edit,
    delete,
    login_view,
    registeration_view,
    logout_view,
)

urlpatterns = [
    path("home", create_expense, name="home"),
    path("edit/<int:id>", edit, name="edit"),
    path("delete/<int:id>", delete, name="delete"),
    path("accounts/register", registeration_view, name="register"),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout", logout_view, name="logout"),
]
