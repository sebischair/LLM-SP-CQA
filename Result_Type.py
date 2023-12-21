from enum import Enum

class Result_Type(str, Enum):
    NULL = "null"
    ENTITY = "entity"
    ENTITIES = "entities"
    INT = "integer"
    BOOLEAN = "boolean"
    COUNT = "count"
