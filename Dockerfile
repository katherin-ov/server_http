FROM python:3.13-slim


RUN apt-get update && apt-get install -y \
    apache2-utils \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY . .

RUN curl -sSL https://install.python-poetry.org | python3 -


CMD python src/server/httpd.py -w 8 & \
    sleep 3 && \
    ab -n 50000 -c 100 -r http://127.0.0.1:8080/httptest/wikipedia_russia.html
