FROM python:3.10.19-alpine

LABEL maintainer="Pooya(PAT) <pooya144@gmail.com>"\
      description="A TODO Django Project Running on Alpine Linux Image"\
      version="1.0"

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]