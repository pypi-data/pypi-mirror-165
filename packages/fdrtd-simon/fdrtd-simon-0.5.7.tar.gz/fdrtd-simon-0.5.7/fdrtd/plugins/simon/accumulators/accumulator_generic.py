from fdrtd.plugins.simon.accumulators.accumulator import Accumulator


class AccumulatorGeneric(Accumulator):

    def __init__(self, _=None):
        self.data = None

    def serialize(self):
        return self.data

    @staticmethod
    def deserialize(data):
        accumulator = AccumulatorGeneric()
        accumulator.data = data
        return accumulator

    def add(self, other):
        self.data = other.data
        return self

    def update(self, data):
        self.data = data

    def finalize(self):
        pass

    def get_data(self):
        return self.data
