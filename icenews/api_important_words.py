import logging

from pydantic import BaseModel, Field
from typing import List

from .similar import important_words
from .server import app

_MAX_LENGTH = 2000

logger = logging.getLogger(__name__)


class ParseOutput(BaseModel):
    important_words: List[str] = Field(..., description="List of lemmas")


class ParseInput(BaseModel):
    input_string: str = Field(
        ...,
        description="Icelandic text for analysis.",
        min_length=1,
        max_length=_MAX_LENGTH,
    )


# Strange things happen with error handling when using alias - splitting up into two input models
class ParseInputDeprecated(BaseModel):
    input_string: str = Field(
        ...,
        description="Icelandic text for analysis.",
        min_length=1,
        max_length=_MAX_LENGTH,
        alias="in",
    )


@app.post(
    "/v1/important_words",
    description="Find lemmas of important words",
    response_model=ParseOutput,
)
def v1_important_words(*, data: ParseInput):
    return ParseOutput(important_words=important_words(data.input_string))


@app.post(
    "/v1/parse",
    description="Find lemmas of important words",
    response_model=ParseOutput,
    deprecated=True,
)
def v1_parse(*, data: ParseInputDeprecated):
    logger.info(f"parse: {repr(data.input_string)}")
    return ParseOutput(important_words=important_words(data.input_string))
