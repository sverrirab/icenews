FROM python:3.7

RUN pip install --no-cache-dir icenews>=1.0.6

EXPOSE 5000

CMD ["python", "-m", "icenews", "--bind", "0.0.0.0", "--port", "5000"]
