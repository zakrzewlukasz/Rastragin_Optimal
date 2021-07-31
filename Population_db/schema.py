from marshmallow import Schema, fields, post_load
from Population_db.store import Store


class StoreSchema(Schema):
     _id = fields.Int()
     parameters = fields.List(fields.Float)
     standard_deviation = fields.List(fields.Float)
     fitness = fields.Float()

     @post_load
     def make_store(self, data, **kwargs):
        return Store(**data)