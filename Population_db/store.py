import uuid


class Store:
    def __init__(self, fitness, _id: int = None):
        self.parameters = []
        self.standard_deviation = []
        self.fitness = fitness
        self._id = _id or uuid.uuid4().hex
