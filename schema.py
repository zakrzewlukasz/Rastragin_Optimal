from marshmallow import Schema, fields, post_load
from store import Store


class StoreSchema(Schema):
     _id = fields.Str()
     name = fields.Str()
     location = fields.Str()

     @post_load
     def make_store(self, data, **kwargs):
        return Store(**data)