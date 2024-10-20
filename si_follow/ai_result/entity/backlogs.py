from django.db import models

from ai_result.entity.project import Project


class Backlog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Backlog -> (Project: {self.project.project_name})"
