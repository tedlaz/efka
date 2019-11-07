FROM python:alpine

RUN pip install hug && \
    mkdir osyk

COPY . /osyk

RUN chmod +x /osyk/start.sh

WORKDIR /osyk

EXPOSE 8000

CMD ["/osyk/start.sh"]