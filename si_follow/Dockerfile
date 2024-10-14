FROM python:3.10

WORKDIR /app

# 필요시 패키지 설치 활성화 (MySQL 관련된 패키지가 필요한 경우)
# RUN apt-get update && apt-get install -y \
#     build-essential
#     libmysqlclient-dev \
#     pkg-config
#     && rm -rf /var/lib/apt/lists/*

# requirements.txt 파일 복사 및 패키지 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

#ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
# wait-for-it.sh 스크립트 복사
COPY wait-for-it.sh /app/wait-for-it.sh
# 전체 프로젝트 파일 복사 (여기서 si_follow 포함됨)
COPY . /app/

# wait-for-it.sh 및 manage.py에 실행 권한 부여
RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/manage.py

# ENV PYTHONUNBUFFERED 1

# Django 서버 실행
CMD ["/app/wait-for-it.sh", "db:3306", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]