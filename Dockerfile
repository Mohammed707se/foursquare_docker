FROM python:3.9


WORKDIR /app


COPY scraper.py .


RUN pip install requests


RUN mkdir -p /app/data


ENTRYPOINT ["python", "scraper.py"]
