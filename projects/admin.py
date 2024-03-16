from django.contrib import admin

from .models import Project, TechnologyIcon

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "github_link", "web_link", "display_technologies", "date", "enterprise")
    prepopulated_fields = {"slug": ("title",)}

    def display_technologies(self, obj):
        return ', '.join([technology.name for technology in obj.technologies.all()])


admin.site.register(Project, ProjectAdmin)

admin.site.register(TechnologyIcon)