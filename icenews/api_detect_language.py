import logging
import pycld2

from pydantic import BaseModel, Field

from .server import app

_MAX_LENGTH = 2000

logger = logging.getLogger(__name__)


class DetectLanguageResponse(BaseModel):
    language: str = Field(..., description="Detected language")
    reliable: bool = Field(..., description="Is detected language reliable?")


class DetectLanguageRequest(BaseModel):
    input_string: str = Field(
        ...,
        description="Icelandic text for analysis.",
        min_length=1,
        max_length=_MAX_LENGTH,
    )


@app.post(
    "/v1/detect_language",
    description="Detect the language of the input text",
    response_model=DetectLanguageResponse,
)
def v1_detect_language(*, data: DetectLanguageRequest):
    is_reliable, _, details = pycld2.detect(data.input_string)
    lang1, _, _ = details
    _, language, _, _ = lang1
    return DetectLanguageResponse(language=language, reliable=is_reliable)
