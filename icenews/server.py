from fastapi import FastAPI

app = FastAPI(
    version="1.0", title="icenews", description="Simple NLP for Icelandic News"
)

# Need to import all modules here to register their api endpoints:
from .api_detect_language import v1_detect_language  # noqa: E402, F401
from .api_edit_distance import v1_edit_distance  # noqa: E402, F401
from .api_important_words import v1_important_words, v1_parse  # noqa: E402, F401
