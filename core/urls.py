from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fixtures", views.fixtures, name="fixtures"),
    path("predict/<int:fixture_id>/", views.predict, name="predict"),
]
