from pydantic import BaseModel, Field, ValidationError, validator
from typing import List

from .similar import important_words
from .server import app

_MAX_LENGTH = 2000


class ParseInput(BaseModel):
    input_string: str = Field(
        None, alias="in", description="Icelandic text for analysis."
    )

    @validator("input_string")
    def input_string_length(cls, v):
        if v is None or len(v) == 0:
            raise ValidationError(f"Missing 'in' data.")
        if len(v) >= _MAX_LENGTH:
            raise ValidationError(
                f"Input too large - current maximum is {_MAX_LENGTH} characters."
            )
        return v


class ParseOutput(BaseModel):
    important_words: List[str] = Field(None, description="List of lemmas")


@app.post(
    "/v1/parse", description="Very simple lemmatization", response_model=ParseOutput
)
def parse(*, data: ParseInput):
    return ParseOutput(important_words=important_words(data.input_string))
