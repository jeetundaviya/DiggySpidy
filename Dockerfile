FROM ubuntu:20.04

WORKDIR DiggySpidy

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.10 python3-pip python3.10-dev tor

RUN apt-get install -y wget &&\
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt-get install ./google-chrome-stable_current_amd64.deb -y

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3.10","diggy-spidy.py" ]