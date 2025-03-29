# 파이썬 기본 이미지
FROM python:3.10-slim

# 작업 폴더 생성 및 설정
WORKDIR /app

# 로컬의 requirements.txt를 컨테이너 내부로 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --upgrade pip && pip install -r requirements.txt

# 소스 코드 파일들을 컨테이너 내부로 복사
COPY . .

# 봇이 사용할 환경변수 (TOKEN) 설정 (실행할 때 넘겨줌)
ENV DISCORD_TOKEN=""

# 컨테이너 실행 시 자동으로 봇이 시작
CMD ["python", "bot.py"]


# docker build -t BOJRandomDefense-Bot .
# docker run --env-file=.env BOJRandomDefense-Bot