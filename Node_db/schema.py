from marshmallow import Schema, fields, post_load
from Node_db.store import Store_node
from datetime import datetime

class StoreSchema_node(Schema):
     _id = fields.Int()
     population_range_in = fields.Int()
     population_range_out = fields.Int()
     time = fields.Float()
     calculated = fields.Boolean()
     in_progress = fields.Boolean()
     start_time= fields.DateTime()


     @post_load
     def make_store(self, data, **kwargs):
        return Store_node(**data)
