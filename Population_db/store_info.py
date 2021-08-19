import uuid

class Store_info:
    def __init__(self, instances, algo_start, algo_end, end, population_size, generation_number, _id: int = None):

        self.instances = instances
        self.algo_start = algo_start
        self.algo_end = algo_end
        self.end = end
        self.population_size = population_size
        self.generation_number = generation_number
        self._id = _id or uuid.uuid4().hex
