from django.db import models
from django.urls import reverse


class TechnologyIcon(models.Model):
    name = models.CharField(max_length=50)
    src = models.URLField(max_length=400)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    github_link = models.URLField(max_length=200, null=True, blank=True)
    web_link = models.URLField(max_length=200, null=True, blank=True)
    technologies = models.ManyToManyField(TechnologyIcon)
    date = models.DateField(auto_now=False, auto_now_add=False)
    enterprise = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})
    