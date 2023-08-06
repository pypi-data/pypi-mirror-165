from typing import List, TypeVar, Generic

from pydantic import BaseModel, PositiveInt, NonNegativeInt
from pydantic.generics import GenericModel


class PageRequest(BaseModel):
    # Index of requested page (first page is 1!)
    page: PositiveInt

    # Max items per page
    size: PositiveInt


ItemT = TypeVar("ItemT")


class Page(GenericModel, Generic[ItemT]):
    # The items on this page. len(items) == 0 if total is 0. len(items) can be smaller than size.
    items: List[ItemT]

    # Index of this returned page (first page is 1!)
    page: PositiveInt

    # Max items per page (so can be more than actual number of items on last page)
    size: PositiveInt

    # Total items, all pages combined
    total: NonNegativeInt
