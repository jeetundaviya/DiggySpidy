FROM python:3.10

WORKDIR DiggySpidy

RUN apt update && \
    apt install tor -y

RUN apt install -y wget &&\
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt install ./google-chrome-stable_current_amd64.deb -y

COPY . .

RUN pip install -r requirements.txt

CMD [ "python","diggy-spidy.py" ]