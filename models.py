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


class User(BaseModel):
    id: Union[PydanticObjectId, None] = Field(alias='_id')
    name: str
    surname: str

    class Config:
        fields = {'id': {'exclude_defaults': True}}


class Book(BaseModel):
    title: str
    author: str
    id: Union[PydanticObjectId, None] = Field(alias='_id')
    isRent: Union[bool, None] = False
    person: Union[User, None] = None

    class Config:
        fields = {'id': {'exclude_defaults': True}}
        # json_encoders = {BsonObjectId: str}
