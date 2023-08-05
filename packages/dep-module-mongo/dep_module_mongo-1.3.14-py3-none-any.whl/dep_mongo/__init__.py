"""Dep mongo module."""

from typing import Dict, Optional, List, TypeVar

from dataclasses import dataclass, field
from beanie import (
    Document as MongoDocument,
    Indexed,
    After,
    View,
    Link,
    DeleteRules,
    PydanticObjectId,
    Insert,
    Replace,
    Before,
    BulkWriter,
    SaveChanges,
    Delete,
    WriteRules,
    UnionDoc,
    Granularity,
    TimeSeriesConfig,
    ValidateOnSave,
    operators,
    executors,
    exceptions,
    after_event,
    free_fall_migration,
    iterative_migration,
    before_event,
    init_beanie,
)
from motor.motor_asyncio import (
    AsyncIOMotorClient as Client,  # noqa
    AsyncIOMotorDatabase as Database,  # noqa
)

from spec.types import Module, Environment


class Document(MongoDocument):
    """Document. TODO: add CRUD here later ?"""

    pass


@dataclass
class Mongo(Module):
    """Mongo module."""

    models: List = field(default_factory=list)

    host: str = 'localhost'
    port: int = 27017
    database: str = 'test'
    user: str = 'test'
    password: str = 'test'

    connection_extra: Dict = field(default_factory=dict)

    __client__: Client = None

    def default_connection_params(self) -> Dict:
        """Default mongo connection params."""

        params = {
            'socketTimeoutMS': '10000',
            'connectTimeoutMS': '10000',
            'ssl': 'true',
        }

        if not self.app.spec.status.on_k8s and self.app.spec.environment in (
            # Environment.unknown,
            Environment.testing,
            Environment.develop,
            Environment.stage,
        ):
            params.update({
                'socketTimeoutMS': '100',
                'connectTimeoutMS': '100',
                'ssl': 'false',
            })

        return params

    def get_uri(self) -> str:
        """Get connection uri."""
        params = self.default_connection_params()
        params.update(self.connection_extra)
        raw_opts = '&'.join(f'{_pn}={_pv}' for _pn, _pv in params.items())

        base_uri = 'mongodb://{user}:{password}@{host}:{port}'.format(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
        )

        return f'{base_uri}/{self.database}?{raw_opts}'

    async def prepare(self, scope):
        """Prepare mongo."""
        uri = self.get_uri()
        self.__client__ = Client(uri)
        await init_beanie(
            database=self.__client__[self.database],
            document_models=self.models,
        )

    async def health(self, scope) -> bool:
        """Prepare mongo."""
        status = await self.__client__[self.database].command('ping')
        return status and 'ok' in status




__all__ = (
    'Mongo',
    'Document',
    'Indexed',
    'After',
    'View',
    'Link',
    'DeleteRules',
    'PydanticObjectId',
    'Insert',
    'Replace',
    'Before',
    'BulkWriter',
    'SaveChanges',
    'Delete',
    'WriteRules',
    'UnionDoc',
    'Granularity',
    'TimeSeriesConfig',
    'ValidateOnSave',
    'operators',
    'executors',
    'exceptions',
    'after_event',
    'free_fall_migration',
    'iterative_migration',
    'before_event',
)