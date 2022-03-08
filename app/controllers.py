from typing import List

from app.catalog import Catalog
from app.model import Product


def add_product(catalog: Catalog, name, description, category_id) -> Product:
    # if not catalog.is_category_exists(category_id):
    #     raise ValueError(f'No such category {category_id}')
    product = Product(
        id=catalog.get_product_id(),
        name=name,
        description=description,
        category_id=category_id,
    )
    catalog.add_product(product)
    return product


def get_products(catalog: Catalog) -> List[Product]:
    return catalog.get_products()


def get_product_by_id(catalog: Catalog, product_id: int) -> Product:
    if not catalog.is_product_exists(product_id):
        raise ValueError(f'No such product {product_id}')
    return catalog.get_product_by_id(product_id)

