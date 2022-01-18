from abc import ABC, abstractmethod
from typing import Union

from elasticsearch import AsyncElasticsearch

from models.film import FilmDetailedDTO
from models.genre import GenreDetailedDTO
from models.person import PersonDetailedDTO


T = Union[FilmDetailedDTO, GenreDetailedDTO, PersonDetailedDTO]


class AbstractElastic(ABC):
    """Абстрактный класс для работы с хранилищем ES"""

    @abstractmethod
    def __init__(self, index: str, model: T, elastic: AsyncElasticsearch):
        self.index = index
        self.model = model
        self.elastic = elastic

    @abstractmethod
    async def get_by_id(self, id: str) -> T:
        pass

    @abstractmethod
    async def get_by_params(self, **params) -> list[T]:
        pass