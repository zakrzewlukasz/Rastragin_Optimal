from marshmallow import Schema, fields, post_load
from Population_db.store_info import Store_info

class StoreSchema_info(Schema):
     _id = fields.Int()
     instances = fields.Int()
     algo_start = fields.Int()
     algo_end = fields.Int()

     @post_load
     def make_store(self, data, **kwargs):
        return Store_info(**data)