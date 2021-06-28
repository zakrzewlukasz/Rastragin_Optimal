import uuid


class Store:
    def __init__(self, name: str, location: str, _id: str = None):
        self.name = name
        self.location = location
        self._id = _id or uuid.uuid4().hex
