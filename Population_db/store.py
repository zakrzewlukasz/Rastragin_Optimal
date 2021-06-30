import uuid
import numpy as np


class Store:
    def __init__(self, fitness, _id: int = None):
        #self.parameters = np.array([], dtype=dou)
        #self.standard_deviation = np.array([], dtype=float)
        self.fitness = fitness
        self._id = _id or uuid.uuid4().hex
