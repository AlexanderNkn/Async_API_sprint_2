from typing import Optional

import elasticsearch.exceptions
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from orjson import loads as orjson_loads

from models.base import orjson_dumps
from services.AbstractClasses import AbstractElastic, T

from .utils import get_body

OBJ_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class BaseService(AbstractElastic):
    def __init__(self, index: str, model: T, elastic: AsyncElasticsearch, redis: Redis) -> None:
        self.index = index
        self.model = model
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, id: str) -> T:
        redis_key = self.redis_key(id)
        obj = await self._obj_from_cache(redis_key)
        if not obj:
            try:
                doc = await self.elastic.get(index=self.index, id=id)
            except elasticsearch.exceptions.NotFoundError:
                obj = None
            else:
                obj = self.model(**doc['_source'])
                await self._put_obj_to_cache(redis_key, obj)

        return obj

    async def get_by_params(self, **params) -> list[T]:
        body = get_body(**params)
        redis_key = self.redis_key(body)
        obj_list = await self._list_from_cache(redis_key)
        if not obj_list:
            try:
                doc = await self.elastic.search(body=body, index=self.index)
            except elasticsearch.exceptions.NotFoundError:
                obj_list = None
            else:
                obj_list = [self.model(**_doc['_source']) for _doc in doc['hits']['hits']]
                await self._put_list_to_cache(redis_key, obj_list)

        return obj_list

    def redis_key(self, params):
        return hash(self.index + orjson_dumps(params))

    async def _obj_from_cache(self, redis_key: str) -> Optional[T]:
        data = await self.redis.get(redis_key)
        if not data:
            return None

        obj = self.model.parse_raw(data)
        return obj

    async def _list_from_cache(self, redis_key: str) -> Optional[list[T]]:
        data = await self.redis.get(redis_key)
        if not data:
            return None

        obj = [self.model.parse_raw(_data) for _data in orjson_loads(data)]
        return obj

    async def _put_obj_to_cache(self, redis_key: str, obj: T):
        await self.redis.set(redis_key, obj.json(), expire=OBJ_CACHE_EXPIRE_IN_SECONDS)

    async def _put_list_to_cache(self, redis_key: str, obj_list: list[T]):
        await self.redis.set(redis_key, orjson_dumps(obj_list, default=self.model.json),
                             expire=OBJ_CACHE_EXPIRE_IN_SECONDS)
