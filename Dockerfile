FROM ubuntu

WORKDIR DiggySpidy

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    python3.10 python3-pip python3.10-dev tor

RUN apt-get install -y wget &&\
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt-get install ./google-chrome-stable_current_amd64.deb -y

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3.10","diggy-spidy.py" ]