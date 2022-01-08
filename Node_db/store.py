import uuid

class Store_node:
    def __init__(self, population_range_in, population_range_out, time,calculated, in_progress, start_time, _id: int = None):

        self.population_range_in = population_range_in
        self.population_range_out = population_range_out
        self.time = time
        self.calculated = calculated
        self.in_progress = in_progress
        self.start_time =  start_time
        self._id = _id or uuid.uuid4().hex

