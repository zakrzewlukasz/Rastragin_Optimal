import uuid

class Store_info:
    def __init__(self, instances, algo_start, algo_end, _id: int = None):

        self.instances = instances
        self.algo_start = algo_start
        self.algo_end = algo_end
        self._id = _id or uuid.uuid4().hex
