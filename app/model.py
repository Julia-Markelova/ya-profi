from dataclasses import dataclass
from typing import List
from typing import Type
from typing import TypeVar
from typing import Union

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Product:
    id: int
    name: str
    description: str
    category_id: int


@dataclass_json
@dataclass
class Category:
    id: int
    name: str
    description: str
    parent_id: int


@dataclass
@dataclass_json
class CategoryInfo:
    id: int
    name: str
    description: str
    sub_categories: List['CategoryInfo']


T = TypeVar('T')


def serialize(data: T) -> dict:
    return type(data).schema().dump(data)


def deserialize(data_type: Type[T], json_data: Union[str, dict]) -> T:
    if isinstance(json_data, str):
        return data_type.schema().loads(json_data)
    elif isinstance(json_data, dict):
        return data_type.schema().load(json_data)
    else:
        raise ValueError(f'Wrong type of json data: `str` or `dict` expected but {type(json_data)} given.')
