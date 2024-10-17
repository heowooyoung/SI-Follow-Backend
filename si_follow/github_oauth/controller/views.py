from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from account.repository.profile_repository_impl import ProfileRepositoryImpl
from account.service.account_service_impl import AccountServiceImpl
from github_oauth.serializer.github_oauth_url_serializer import GithubOauthUrlSerializer
from github_oauth.service.github_oauth_service_impl import GithubOauthServiceImpl
from redis_service.redis_service_impl import RedisServiceImpl


class GithubOauthView(viewsets.ViewSet):
    githubOauthService = GithubOauthServiceImpl.getInstance()
    redisService = RedisServiceImpl.getInstance()
    accountService = AccountServiceImpl.getInstance()
    profileRepository = ProfileRepositoryImpl.getInstance()

    # GitHub 로그인 URL 생성
    def githubOauthURI(self, request):
        try:
            url = self.githubOauthService.githubLoginAddress()
            print(f"url: {url}")
            serializer = GithubOauthUrlSerializer(data={'url': url})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error generating GitHub OAuth URL: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Access Token 요청 및 사용자 정보 처리
    def githubAccessTokenURI(self, request):
        print("githubAccessTokenURI()")

        # POST 요청에서 'code' 값 가져오기
        code = request.data.get('code')

        if not code:
            return JsonResponse({'error': 'Code is missing'}, status=400)

        print(f"Received code: {code}")

        try:
            # 1. Access Token 요청
            accessToken = self.githubOauthService.requestAccessToken(code)
            print(f"Access token: {accessToken}")

            # 2. Access Token으로 사용자 정보 요청
            user_info = self.githubOauthService.requestUserInfo(accessToken)
            email = user_info.get('email')

            if not email:
                return JsonResponse({'error': 'Email not found in user info'}, status=400)

            # 3. Profile 조회 (이메일로 찾기)
            profile = self.profileRepository.findByEmail(email)

            # 4. Profile이 없으면 새로운 Account 생성 및 Profile 생성
            if not profile:
                print(f"Profile not found for email: {email}, creating new account and profile.")

                # GitHub OAuth로 로그인한 사용자이므로 loginType을 "GitHub"으로 설정
                account = self.accountService.create("GitHub", "User")
                self.profileRepository.create(email=email, account=account)

            # 5. Redis에 Access Token과 이메일 저장
            redis_token_response = self.redisAccessToken(email, accessToken)
            print(f"Redis token response: {redis_token_response}")
            if redis_token_response.status_code != 200:
                return JsonResponse({'error': 'Failed to store token in Redis'},
                                    status=redis_token_response.status_code)

            # 6. Redis에서 발급된 userToken 가져오기
            user_token = redis_token_response.data.get('userToken')

            # 7. userToken만 프론트엔드에 반환
            return JsonResponse({'userToken': user_token}, status=200)

        except Exception as e:
            print(f"Error during GitHub OAuth flow: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # 프론트엔드에서 userToken으로 사용자 정보와 accessToken 요청 시 처리
    def getUserInfo(self, request):
        print("getUserInfo()")

        # POST 요청에서 'userToken' 값 가져오기
        user_token = request.data.get('user_token')

        if not user_token:
            return JsonResponse({'error': 'User token is missing'}, status=400)

        try:
            # 1. Redis에서 userToken으로 accessToken 조회
            stored_data = self.redisService.get_value_by_key(user_token)

            if not stored_data or 'access_token' not in stored_data:
                return JsonResponse({'error': 'Access token not found in Redis'}, status=404)

            access_token = stored_data['access_token']

            # 2. accessToken으로 GitHub 사용자 정보 요청
            user_info = self.githubOauthService.requestUserInfo(access_token)

            # 3. 사용자 정보와 함께 accessToken도 반환
            return JsonResponse({
                'user_info': user_info,
                'access_token': access_token
            }, status=200)

        except Exception as e:
            print(f"Error retrieving user info: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    # Redis에 Access Token 저장 (별도의 메서드로 분리)
    def redisAccessToken(self, email, accessToken):
        try:
            # Redis에 Access Token과 함께 userToken 저장
            return self.redisService.generate_and_store_access_token(self.profileRepository, email, accessToken)
        except Exception as e:
            print(f"Error generating/storing access token in Redis: {e}")
            return JsonResponse({'error': 'Failed to store access token'}, status=500)

    # Redis에서 토큰 삭제 (로그아웃 처리)
    def dropRedisTokenForLogout(self, request):
        try:
            userToken = request.data.get('userToken')
            redis_response = self.redisService.delete_access_token(userToken)
            return redis_response
        except Exception as e:
            print(f"Error during Redis token deletion: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)
