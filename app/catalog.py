from typing import Dict
from typing import List
from typing import Optional

from app.model import Category
from app.model import CategoryInfo
from app.model import Product


class Catalog:
    def __init__(self):
        self._products: Dict[int, Product] = {}
        self._categories: Dict[int, Category] = {}
        self._category_id_to_sub_categories_ids: Dict[int, List[int]] = {}

    def get_product_id(self) -> int:
        return len(self._products)

    def get_category_id(self) -> int:
        return len(self._categories)

    def is_product_exists(self, product_id: int) -> bool:
        product = self._products.get(product_id)
        return product is not None

    def is_category_exists(self, category_id: int) -> bool:
        category = self._products.get(category_id)
        return category is not None

    def is_category_empty(self, category_id: int) -> bool:
        children = self._category_id_to_sub_categories_ids.get(category_id)
        return children is not None

    def add_product(self, product: Product):
        self._products[product.id] = product

    def get_products(self) -> List[Product]:
        return list(self._products.values())

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def update_product(self, product: Product):
        self._products[product.id] = product

    def get_products_by_parameters(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None,
            category_name: Optional[str] = None
    ) -> List[Product]:
        pass

    def delete_product_by_id(self, product_id: int):
        del self._products[product_id]

    def add_category(self, category: Category):
        self._categories[category.id] = category
        if self._category_id_to_sub_categories_ids.get(category.parent_id) is None:
            self._category_id_to_sub_categories_ids[category.parent_id] = [category.id]
        else:
            self._category_id_to_sub_categories_ids[category.parent_id].append(category.id)

    def get_categories(self) -> List[CategoryInfo]:
        return self._resolve_subcategories(*self._category_id_to_sub_categories_ids.keys())

    def _resolve_subcategories(self, *sub_categories_ids) -> List[CategoryInfo]:
        result = []
        for cat_id in sub_categories_ids:
            category = self._categories[cat_id]
            result.append(
                CategoryInfo(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    sub_categories=self._resolve_subcategories(*self._category_id_to_sub_categories_ids[cat_id])
                )
            )
        return result

    def get_category_by_id(self, category_id: int) -> Category:
        return self._categories.get(category_id)

    def update_category(self, category: Category):
        self._categories[category.id] = category

    def get_categories_by_parameters(
            self,
            name: Optional[str] = None,
            description: Optional[str] = None
    ) -> List[Category]:
        pass

    def delete_category_by_id(self, category_id: int):
        del self._categories[category_id]
        del self._category_id_to_sub_categories_ids[category_id]
        for c_id in self._category_id_to_sub_categories_ids:
            if category_id in self._category_id_to_sub_categories_ids[c_id]:
                self._category_id_to_sub_categories_ids[c_id].remove(category_id)
