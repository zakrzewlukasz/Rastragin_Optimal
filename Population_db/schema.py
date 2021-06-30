from marshmallow import Schema, fields, post_load
from Population_db.store import Store

class InnerSchema(Schema):
     foo = fields.Int()
     fo = fields.Int()

class StoreSchema(Schema):
     _id = fields.Int()
     parameters = []
     standard_deviation = []
     fitness = fields.Float()

     @post_load
     def make_store(self, data, **kwargs):
        return Store(**data)