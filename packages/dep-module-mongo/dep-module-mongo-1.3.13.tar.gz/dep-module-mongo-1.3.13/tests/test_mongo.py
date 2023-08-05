"""Tesg mongo module."""

import asgi_lifespan
import asyncio
import pytest

from spec.types import App, JSONResponse, load_spec

from dep_mongo import Mongo, Document


class Doc(Document):

    field: str


@pytest.fixture
def app(monkeypatch) -> App:
    """Mock app."""

    monkeypatch.setenv('ENVIRONMENT', 'testing')

    app = App()
    app.spec = load_spec()

    @app.route('/')
    async def home(request):  # noqa
        return JSONResponse({'status': 'ok'})

    yield app


@pytest.fixture
def module() -> Mongo:
    """Mongo module."""
    return Mongo(database='test', models=[Doc])


def test_activate(app, module):
    """Test activate."""

    module.inject(app=app)

    async def lifespan():
        """Async asgi module calling."""

        async with asgi_lifespan.LifespanManager(app):
            # assert module is mock_app.modules['mongo']
            # assert not module.enabled
            pass

    asyncio.run(lifespan())


'''
import asyncio

import pytest  # noqa

from spec.ext.fixtures import *  # noqa
from pymongo import MongoClient
from pymongo.database import Database
from temp import DEFAULT_URI, Mongo

from asgi_lifespan import LifespanManager
from pytest_mock_resources import create_mongo_fixture


mongo = create_mongo_fixture()


@fixture
def mock_client(mongo) -> MongoClient:
    """Mock mongo client."""

    # return MongoClient(**mongo.pmr_credentials.as_mongo_kwargs())
    from temp import DEFAULT_URI
    return MongoClient(DEFAULT_URI)


@fixture
def mock_db(mock_client) -> Database:
    """Mock mongo db."""
    return mock_client['test']


@fixture
def mock_module(mocker, mock_db, mock_client) -> Mongo:  # noqa
    """Mock mongo module."""
    mocker.patch('dep_mongo.get_client', return_value=mock_client)
    module = Mongo(uri=DEFAULT_URI)
    yield module


def test_activate(app: App, mock_module: Mongo):
    """Test activate."""

    mock_module.inject(app=app)

    async def lifespan():
        """Async asgi module calling."""

        async with LifespanManager(app):
            module: Mongo = app.modules['mongo']

            assert mock_module.active
            assert mock_module.client
            assert mock_module.engine

            collection = module.collection('test_collection')

            print(collection)
            # assert collection is not None

            # to_insert = [{"name": "John"}, {"name": "Viola"}]

            # collection.insert_many(to_insert)

            # TODO: after fix event loop err

            # result = collection.find().sort("name")
            # returned = [row for row in result]
            # assert returned == to_insert

            # TODO: after try add CRUD provider
            # TODO + tests

    asyncio.run(lifespan())
'''
