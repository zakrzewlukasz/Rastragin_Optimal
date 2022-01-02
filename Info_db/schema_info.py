from marshmallow import Schema, fields, post_load
from Info_db.store_info import Store_info

class StoreSchema_info(Schema):
     _id = fields.Int()
     instances = fields.Int()
     root = fields.Int()
     algo_start = fields.Int()
     algo_end = fields.Int()
     end = fields.Boolean()
     population_size = fields.Int()
     generation_number = fields.Int()

     @post_load
     def make_store(self, data, **kwargs):
        return Store_info(**data)