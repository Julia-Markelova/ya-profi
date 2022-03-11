import pytest

from app.user_manager import UserManager

user_manager = UserManager()


def test_auth():
    user_manager.authorize('test', 'test')


def test_auth_wrong_creds():
    with pytest.raises(ValueError):
        user_manager.authorize('', '')
