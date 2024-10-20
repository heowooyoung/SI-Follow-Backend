from rest_framework.response import Response
from rest_framework import status, viewsets

from ai_result.service.ai_result_service_impl import AIResultServiceImpl


class AIResultView(viewsets.ViewSet):
    ai_result_service = AIResultServiceImpl()

    # 백로그 저장 및 가져오기
    def store_backlogs(self, request):
        user_token = request.data.get('user_token')
        project_name = request.data.get('project_name')
        result = self.ai_result_service.fetch_and_store_backlogs(user_token, project_name)
        return Response(result, status=status.HTTP_200_OK)

    def get_backlogs(self, request):
        user_token = request.data.get('user_token')  # 기존 GET을 POST로 변경
        project_name = request.data.get('project_name')
        result = self.ai_result_service.get_backlogs(user_token, project_name)
        return Response(result, status=status.HTTP_200_OK)

    # 파일 리스트 저장 및 가져오기
    def store_file_list(self, request):
        user_token = request.data.get('user_token')
        project_name = request.data.get('project_name')
        result = self.ai_result_service.fetch_and_store_file_list(user_token, project_name)
        return Response(result, status=status.HTTP_200_OK)

    def get_file_list(self, request):
        user_token = request.data.get('user_token')
        project_name = request.data.get('project_name')
        result = self.ai_result_service.get_file_list(user_token, project_name)
        return Response(result, status=status.HTTP_200_OK)

    # 테스트 리포트 저장 및 가져오기
    def store_test_reports(self, request):
        user_token = request.data.get('user_token')
        project_name = request.data.get('project_name')
        result = self.ai_result_service.fetch_and_store_test_reports(user_token, project_name)
        return Response(result, status=status.HTTP_200_OK)

    def get_test_reports(self, request):
        user_token = request.data.get('user_token')
        project_name = request.data.get('project_name')
        result = self.ai_result_service.get_test_reports(user_token, project_name)
        return Response(result, status=status.HTTP_200_OK)
