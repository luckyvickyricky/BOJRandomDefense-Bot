# 파이썬 기본 이미지
FROM python:3.10-slim

# Poetry 버전 설정 (원하는 버전으로 변경 가능)
ENV POETRY_VERSION=2.1.2
ENV PATH="/root/.local/bin:${PATH}"

# 시스템 패키지 업데이트 및 Poetry 설치
RUN apt-get update && apt-get install -y curl build-essential \
    && pip install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# 작업 폴더 생성 및 설정
WORKDIR /app

# pyproject.toml과 poetry.lock 파일을 컨테이너로 복사
COPY pyproject.toml poetry.lock* ./

# Poetry가 가상환경을 만들지 않도록 설정하고 의존성 설치
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 소스 코드 파일들을 컨테이너 내부로 복사
COPY . .

# 봇이 사용할 환경변수 (DISCORD_TOKEN)는 실행 시 넘겨줌
ENV DISCORD_TOKEN=""

# 컨테이너 실행 시 자동으로 봇이 시작 (Poetry를 통해 실행)
CMD ["poetry", "run", "python", "bot.py"]



# docker build -t random-defense-bot .
# docker run -d --env-file=.env random-defense-bot
