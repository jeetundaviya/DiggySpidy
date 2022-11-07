FROM python:3.10

WORKDIR DiggySpidy

RUN apt update && \
    apt install wget tor -y

RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt install ./google-chrome-stable_current_amd64.deb -y

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

CMD [ "python","diggy-spidy.py" ]