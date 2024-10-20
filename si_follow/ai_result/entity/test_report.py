from django.db import models
from ai_result.entity.project import Project


class TestReport(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    report_content = models.TextField()

    def __str__(self):
        return f"TestReport -> (Project: {self.project.project_name})"
