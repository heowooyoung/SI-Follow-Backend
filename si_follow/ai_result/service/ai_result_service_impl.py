from ai_result.repository.ai_result_repository_impl import AIResultRepositoryImpl
from ai_result.service.ai_result_service import AIResultService
from redis_service.redis_service_impl import RedisServiceImpl
import requests

from si_follow import settings


class AIResultServiceImpl(AIResultService):
    def __init__(self):
        self.ai_result_repository = AIResultRepositoryImpl()
        self.redis_service = RedisServiceImpl.getInstance()
        self.fast_api_url = settings.FAST_API_URL


    # 백로그 저장
    def fetch_and_store_backlogs(self, user_token, project_name):
        stored_data = self.redis_service.get_value_by_key(user_token)
        if 'account_id' not in stored_data:
            return {'error': '유효하지 않은 user_token'}

        account_id = stored_data['account_id']
        response = requests.post(f'{self.fast_api_url}/get-backlogs', json={
            'user_token': user_token,
            'project_name': project_name
        })
        if response.status_code == 200:
            backlog_data = response.json().get('backlog')
            self.ai_result_repository.save_backlogs(account_id, project_name, backlog_data)
            return {'message': '백로그 저장 완료'}
        return {'error': '백로그 가져오기 실패'}

    # 백로그 조회
    def get_backlogs(self, user_token, project_name):
        stored_data = self.redis_service.get_value_by_key(user_token)
        if 'account_id' not in stored_data:
            return {'error': '유효하지 않은 user_token'}

        account_id = stored_data['account_id']
        return self.ai_result_repository.get_backlogs(account_id, project_name)

    # 파일 리스트 저장
    def fetch_and_store_file_list(self, user_token, project_name):
        stored_data = self.redis_service.get_value_by_key(user_token)
        if 'account_id' not in stored_data:
            return {'error': '유효하지 않은 user_token'}

        account_id = stored_data['account_id']
        response = requests.post(f'{self.fast_api_url}/get-file-list', json={
            'user_token': user_token,
            'project_name': project_name
        })
        if response.status_code == 200:
            file_list = response.json().get('file_list')
            self.ai_result_repository.save_files(account_id, project_name, file_list)
            return {'message': '파일 리스트 저장 완료'}
        return {'error': '파일 리스트 가져오기 실패'}

    # 파일 리스트 조회

    def get_file_list(self, user_token, project_name):
        stored_data = self.redis_service.get_value_by_key(user_token)
        if 'account_id' not in stored_data:
            return {'error': '유효하지 않은 user_token'}

        account_id = stored_data['account_id']
        return self.ai_result_repository.get_files(account_id, project_name)

    # 테스트 리포트 저장
    def fetch_and_store_test_reports(self, user_token, project_name):
        stored_data = self.redis_service.get_value_by_key(user_token)
        if 'account_id' not in stored_data:
            return {'error': '유효하지 않은 user_token'}

        account_id = stored_data['account_id']
        response = requests.post(f'{self.fast_api_url}/get-test-reports', json={
            'user_token': user_token,
            'project_name': project_name
        })
        if response.status_code == 200:
            test_reports = response.json().get('test_reports')
            self.ai_result_repository.save_test_reports(account_id, project_name, test_reports)
            return {'message': '테스트 리포트 저장 완료'}
        return {'error': '테스트 리포트 가져오기 실패'}

    # 테스트 리포트 조회
    def get_test_reports(self, user_token, project_name):
        stored_data = self.redis_service.get_value_by_key(user_token)
        if 'account_id' not in stored_data:
            return {'error': '유효하지 않은 user_token'}

        account_id = stored_data['account_id']
        return self.ai_result_repository.get_test_reports(account_id, project_name)

