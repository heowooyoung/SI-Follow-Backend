from ai_result.entity.backlogs import Backlog
from ai_result.entity.file_list import FileList
from ai_result.entity.project import Project
from ai_result.entity.test_report import TestReport
from ai_result.repository.ai_result_repository import AIResultRepository


class AIResultRepositoryImpl(AIResultRepository):

    # 백로그 저장
    def save_backlogs(self, account_id, project_name, backlog_data):
        project, _ = Project.objects.get_or_create(account_id=account_id, project_name=project_name)
        Backlog.objects.filter(project=project).delete()  # 기존 백로그 삭제
        Backlog.objects.create(project=project, description=backlog_data)

    # 백로그 조회
    def get_backlogs(self, account_id, project_name):
        project = Project.objects.get(account_id=account_id, project_name=project_name)
        backlogs = Backlog.objects.filter(project=project)
        return {'project_name': project_name, 'backlogs': [backlog.description for backlog in backlogs]}

    # 파일 리스트 저장
    def save_files(self, account_id, project_name, file_list):
        project, _ = Project.objects.get_or_create(account_id=account_id, project_name=project_name)
        FileList.objects.filter(project=project).delete()  # 기존 파일 삭제
        FileList.objects.create(project=project, file_name=file_list)

    # 파일 리스트 조회
    def get_files(self, account_id, project_name):
        project = Project.objects.get(account_id=account_id, project_name=project_name)
        files = FileList.objects.filter(project=project)
        return {'project_name': project_name, 'files': [file.file_name for file in files]}

    # 테스트 리포트 저장
    def save_test_reports(self, account_id, project_name, test_reports):
        project, _ = Project.objects.get_or_create(account_id=account_id, project_name=project_name)
        TestReport.objects.filter(project=project).delete()  # 기존 리포트 삭제
        TestReport.objects.create(project=project, report_content=test_reports)

    # 테스트 리포트 조회
    def get_test_reports(self, account_id, project_name):
        project = Project.objects.get(account_id=account_id, project_name=project_name)
        test_report = TestReport.objects.get(project=project)
        return {'project_name': project_name, 'test_report': test_report.report_content}

