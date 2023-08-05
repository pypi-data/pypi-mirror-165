from fdrtd.plugins.simon.accumulators.accumulator import Accumulator


class AccumulatorGenericDictionary(Accumulator):

    def __init__(self, _=None):
        self.dictionary = {}

    def serialize(self):
        return {'dictionary': self.dictionary}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorGenericDictionary()
        accumulator.dictionary = dictionary['dictionary']
        return accumulator

    def add(self, other):
        self.dictionary = {**self.dictionary, **other}

    def update(self, data):
        key, value = data
        self.dictionary[key] = value

    def finalize(self):
        pass

    def get_dictionary(self):
        return self.dictionary
