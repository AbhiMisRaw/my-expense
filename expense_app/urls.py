from django.urls import path

from .views import index, create_expense, edit, delete

urlpatterns = [
    path("home", create_expense, name="home"),
    path("edit/<int:id>", edit, name="edit"),
    path("delete/<int:id>", delete, name="delete"),
]
