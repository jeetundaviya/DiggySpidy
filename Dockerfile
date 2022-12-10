FROM python:3.10

RUN apt update && \
    apt install wget tor libffi-dev libssl-dev libxml2-dev libxslt-dev libjpeg-dev libfreetype6-dev zlib1g-dev net-tools vim -y

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt install ./google-chrome-stable_current_amd64.deb -y

COPY . /DiggySpidy

# Project Files and Settings
ARG PROJECT=DiggySpidy
# ARG PROJECT_DIR=/var/www/${PROJECT}
# RUN mkdir -p $PROJECT_DIR
# WORKDIR $PROJECT_DIR
WORKDIR $PROJECT

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "./WebApp/manage.py"]

CMD ["runserver", "0.0.0.0:8000"]