import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app(db_env="ubersante_test")
    return app
