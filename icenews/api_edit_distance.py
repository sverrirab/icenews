import logging

from nltk import edit_distance
from pydantic import BaseModel, Field

from .server import app

_MAX_LENGTH = 2000

logger = logging.getLogger(__name__)


class EditDistanceResponse(BaseModel):
    edit_distance: int = Field(..., description="Edit distance between inputs")


class EditDistanceRequest(BaseModel):
    a: str = Field(
        ..., description="Icelandic text A.", min_length=1, max_length=_MAX_LENGTH,
    )
    b: str = Field(
        ..., description="Icelandic text B.", min_length=1, max_length=_MAX_LENGTH,
    )


@app.post(
    "/v1/edit_distance",
    description="Calculate edit distance between inputs",
    response_model=EditDistanceResponse,
)
def v1_edit_distance(*, data: EditDistanceRequest):
    return EditDistanceResponse(edit_distance=edit_distance(data.a, data.b))
