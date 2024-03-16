from django.views.generic import ListView, DetailView
from django.shortcuts import render
from .models import Project


def home(request):
    pagina_actual = 'home'
    return render(request, 'home.html', {'pagina_actual': pagina_actual})


class ProjectsListView(ListView):
    model = Project
    template_name = "projects_list.html"

class ProjectsDetailView(DetailView):
    model = Project
    template_name = "project_detail.html"
