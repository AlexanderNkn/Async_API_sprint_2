import uuid
from typing import Optional

from .base import BaseModel
from .genre import GenreShortDTO, GenreShortResponse
from .person import PersonShortDTO, PersonShortResponse


class FilmShortResponse(BaseModel):
    """Film with title and imdb_rating, without details."""
    uuid: uuid.UUID
    imdb_rating: float
    title: str


class FilmDetailedResponse(BaseModel):
    """Film details with title, imdb_rating, description, persons, genres."""
    uuid: uuid.UUID
    title: str
    imdb_rating: float
    description: Optional[str]
    genre: list[GenreShortResponse]
    actors: list[PersonShortResponse]
    writers: list[PersonShortResponse]
    directors: list[PersonShortResponse]


class FilmDetailedDTO(BaseModel):
    """Film details received from elasticsearch."""
    id: uuid.UUID
    imdb_rating: float
    genre: list[GenreShortDTO]
    title: str
    description: Optional[str]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    directors_names: Optional[list[str]]
    actors: list[PersonShortDTO]
    writers: list[PersonShortDTO]
    directors: list[PersonShortDTO]
