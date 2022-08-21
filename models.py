from pydantic import BaseModel, Field
from typing import Union
from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class Person(BaseModel):
    name: str
    book_id: Union[PydanticObjectId, None] = None


class Book(BaseModel):
    title: str
    author: str
    id: Union[PydanticObjectId, None] = Field(alias='_id')
    isRent: Union[bool, None] = False
    person: Union[Person, None] = None

    class Config:
        fields = {'id': {'exclude': True}}
