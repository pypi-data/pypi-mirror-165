"""Dep redis module."""

import aioredis

from typing import Dict, Optional
from dataclasses import dataclass

from spec.types import Module, Environment # noqa


@dataclass
class Redis(Module):
    """redis module."""

    host: str = 'localhost'

    db: int = 0
    port: int = 6379
    username: Optional[str] = None
    password: Optional[str] = None

    encoding_errors: str = "strict"
    decode_responses: bool = False
    retry_on_timeout: bool = False
    max_connections: Optional[int] = None

    __store__: aioredis.Redis = None

    def default_redis_kw(self) -> Dict:
        """Default redis kw."""
        return {
            'port': self.port,
            'username': self.password,
            'password': self.password,
            'encoding_errors': self.encoding_errors,
            'decode_responses': self.decode_responses,
            'retry_on_timeout': self.retry_on_timeout,
            'max_connections': self.max_connections,
        }

    def create_client(self, override_kw: Dict = None) -> aioredis.Redis:
        """Create redis client."""
        client_kw = self.default_redis_kw()
        if override_kw:
            client_kw.update(override_kw)

        client_kw.update({'db': self.db})
        return aioredis.from_url(url=f'redis://{self.host}', **client_kw)

    async def prepare(self, scope):
        """Prepare redis."""
        self.__store__ = self.create_client()

    async def health(self, scope) -> bool:
        """Health redis."""
        try:
            await self.__store__.ping()
            return True
        except aioredis.RedisError as _redis_exc:
            return False


__all__ = ('Redis', )
