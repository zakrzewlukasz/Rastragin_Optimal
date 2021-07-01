import uuid
import numpy as np


class Store:
    def __init__(self, fitness, parameters, standard_deviation, _id: int = None):

        self.parameters = parameters
        self.standard_deviation = standard_deviation
        self.fitness = fitness
        self._id = _id or uuid.uuid4().hex
