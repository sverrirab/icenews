from fastapi import FastAPI

app = FastAPI(
    version="1.0", title="icenews", description="Simple NLP for Icelandic News"
)

# Need to import all modules here to register their api endpoints:
from .api_parse_v1 import parse
