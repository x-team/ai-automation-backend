from typing import List, Optional

from pydantic import BaseModel


class X(BaseModel):
    """X Axis."""

    label: str
    header_column: str


class Y(BaseModel):
    """Y Axis."""

    label: str
    header_column: str


class Values(BaseModel):
    """Values."""

    header_column: str


class Data(BaseModel):
    """Data."""

    x: Optional[X] = None
    y: Optional[Y] = None
    values: Optional[Values] = None


class Chart(BaseModel):
    """Chart."""

    type: str
    title: str
    data: Data


class Slide(BaseModel):
    """Slide."""

    title: str
    slide_type: str
    bullet_points: Optional[List[str]] = None
    description: Optional[str] = None
    chart: Optional[Chart] = None
    image_url: Optional[str] = None


class Slideshow(BaseModel):
    """Slideshow."""

    slides: List[Slide]
