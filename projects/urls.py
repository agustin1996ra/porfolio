from django.contrib import admin
from django.urls import path
from .views import ProjectsListView, ProjectsDetailView, home

urlpatterns = [
    path('', home, name='home'),
    path('projects/', ProjectsListView.as_view(), name="proyectos"),
    path('projects/<slug:slug>', ProjectsDetailView.as_view(), name='project_detail'),
]

