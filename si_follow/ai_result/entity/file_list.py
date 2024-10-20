from django.db import models

from ai_result.entity.project import Project


class FileList(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"File -> {self.file_name} (Project: {self.project.project_name})"
