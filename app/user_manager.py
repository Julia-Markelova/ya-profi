from typing import Dict

import pandas as pd

from app.model import User


class UserManager:
    def __init__(self):
        self._users: Dict[str, User] = {
            'test': User(id=0, login='test', password='test')
        }
        self._user_id_to_data = {}

    def add_data(self, user_id, data: pd.DataFrame):
        self._user_id_to_data[user_id] = data

    def authorize(self, login: str, password: str) -> User:
        user = self._users.get(login, None)
        if user is None:
            raise ValueError
        if user.password != password:
            raise ValueError
        return user
