from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ai_result.controller.views import AIResultView

# DefaultRouter 설정
router = DefaultRouter()
router.register(r'ai_result', AIResultView, basename='ai_result')

# URL 패턴 정의
urlpatterns = [
    path('', include(router.urls)),

    path('backlogs', AIResultView.as_view({'post': 'store_backlogs'}), name='airesult-store-backlogs'),
    path('backlogs/get', AIResultView.as_view({'post': 'get_backlogs'}), name='airesult-get-backlogs'),
    path('file-list', AIResultView.as_view({'post': 'store_file_list'}), name='airesult-store-file-list'),
    path('file-list/get', AIResultView.as_view({'post': 'get_file_list'}), name='airesult-get-file-list'),
    path('test-reports', AIResultView.as_view({'post': 'store_test_reports'}), name='airesult-store-test-reports'),
    path('test-reports/get', AIResultView.as_view({'post': 'get_test_reports'}), name='airesult-get-test-reports'),
]
