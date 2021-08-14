FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get update && apt-get install -y libgirepository1.0-dev

CMD [ "python3", "Noel.py" ]
