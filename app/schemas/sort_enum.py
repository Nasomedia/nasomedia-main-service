from enum import Enum


class OrderSortEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SeriesSortEnum(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    ID = "id"
    TITLE = "title"
