from abc import ABC, abstractmethod


class AIResultService(ABC):

    @abstractmethod
    def fetch_and_store_backlogs(self, user_token, project_name):
        pass

    @abstractmethod
    def get_backlogs(self, user_token, project_name):
        pass

    @abstractmethod
    def fetch_and_store_file_list(self, user_token, project_name):
        pass

    @abstractmethod
    def get_file_list(self, user_token, project_name):
        pass

    @abstractmethod
    def fetch_and_store_test_reports(self, user_token, project_name):
        pass

    @abstractmethod
    def get_test_reports(self, user_token, project_name):
        pass