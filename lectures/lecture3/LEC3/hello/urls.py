from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test", views.test, name="test"),
    path("render_test", views.render_test, name="render_test"),
    path("<str:name>", views.greet, name="greet")
]