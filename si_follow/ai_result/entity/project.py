from django.db import models

from account.entity.account import Account


# 이미 정의된 Account 모델 사용

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"Project -> {self.project_name} (Account: {self.account.id})"
