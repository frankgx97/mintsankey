FROM python:3.9.12-slim-bullseye

WORKDIR /app
COPY . .

RUN apt update \
&& apt install -y build-essential python-dev\
&& pip install --no-cache-dir -r requirements.txt \
&& apt remove build-essential -y \
&& apt autoremove -y 

EXPOSE 80

CMD cd /app \
&& exec gunicorn wsgi:app \
    --bind 0.0.0.0:80 \
    --timeout 240 \
    --log-level debug \
    --workers 2