FROM python:3.7

RUN pip install --no-cache-dir icenews==$VERSION

EXPOSE 5000

CMD ["python", "-m", "icenews", "--bind", "0.0.0.0", "--port", "5000"]
