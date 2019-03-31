FROM python:3.7

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir icenews>=1.0.3 gunicorn>=19.9.0

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "icenews.__main__:app"]
