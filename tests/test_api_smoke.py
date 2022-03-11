from http import HTTPStatus

import pytest

from main import flask_app


@pytest.fixture()
def application():
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app


@pytest.fixture()
def client(application):
    return application.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_auth(client):
    response = client.post('/login', data={'login': 'test', 'password': 'test'})
    assert response.status_code == HTTPStatus.OK