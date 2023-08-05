from fdrtd.plugins.simon.accumulators.accumulator import Accumulator


class AccumulatorStatisticsContingency(Accumulator):

    def __init__(self, _=None):
        self.samples = 0
        self.table = {}
        self.mode = None

    def serialize(self):
        return {'samples': self.samples,
                'mode': self.mode,
                'table': self.table}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorStatisticsContingency()
        accumulator.samples = dictionary['samples']
        accumulator.mode = dictionary['mode']
        accumulator.table = dictionary['table']
        return accumulator

    def add(self, other):
        self.samples += other.samples
        for histogram in other.table:
            if histogram not in self.table:
                self.table[histogram] = {}
            for item in other.table[histogram]:
                self.table[histogram][item] = self.table[histogram].get(item, 0) \
                                              + other.table[histogram][item]

    def update(self, data, count=1):
        (histogram, item) = data
        if histogram not in self.table:
            self.table[histogram] = {}
        self.table[histogram][item] = self.table[histogram].get(item, 0) + count
        self.samples = self.samples + count

    def finalize(self):
        maximum = 0
        for histogram in self.table:
            for item in self.table[histogram]:
                if self.table[histogram][item] > maximum:
                    maximum = self.table[histogram][item]
                    self.mode = (histogram, item)

    def get_samples(self):
        return self.samples

    def get_table(self):
        return self.table

    def get_mode(self):
        return self.mode
