import secrets as _secrets

from fdrtd.plugins.simon.caches.cache import Cache
from fdrtd.plugins.simon.caches.additive import CacheAdditive
from fdrtd.plugins.simon.caches.functional import CacheFunctional
from fdrtd.plugins.simon.microprotocols.microprotocol import Microprotocol
from fdrtd.plugins.simon.accumulators.accumulator_statistics_contingency import AccumulatorStatisticsContingency


class MicroprotocolStatisticsContingencyVertical(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.secret_key = _secrets.token_bytes(32)

        self.register_cache('input', Cache())
        self.register_cache('keysx', Cache())
        self.register_cache('keysy', Cache())
        self.register_cache('checkpoint2', CacheAdditive(minimum=2))
        self.register_cache('checkpoint3', CacheAdditive(minimum=2))

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['keysx', 'keysy'], self.stage_1)
        self.register_stage(2, ['checkpoint2'], self.stage_2)
        self.register_stage(3, ['checkpoint3'], self.stage_3)

        self.input = None
        self.result_cache = AccumulatorStatisticsContingency()

        self.dictionary = {}
        self.inverted = {}
        self.keysx = []
        self.keysy = []
        self.keys = {}

    def stage_0(self, args):

        self.dictionary = args['input']['dictionary']
        self.inverted = {}
        for key in self.dictionary:
            value = self.dictionary[key]
            if value not in self.inverted:
                self.inverted[value] = []
            self.inverted[value].append(key)

        if self.network.myself == 0:
            self.network.broadcast(list(self.inverted.keys()), 'keysx')

        if self.network.myself == 1:
            self.network.broadcast(list(self.inverted.keys()), 'keysy')

        return 1, None

    def stage_1(self, args):

        self.keysx = args['keysx']
        self.keysy = args['keysy']

        for keyx in self.keysx:
            for keyy in self.keysy:
                tag = 'psisize_{}_{}'.format(keyx, keyy)
                self.keys[tag] = (keyx, keyy)
                self.register_cache(tag, Cache())

        self.network.broadcast(0, 'checkpoint2')
        return 2, None

    def stage_2(self, args):
        self.register_stage(4, [*self.keys.keys()], self.stage_final)
        self.network.broadcast(0, 'checkpoint3')
        return 3, None

    def stage_3(self, args):
        for key in self.keys:
            keyx, keyy = self.keys[key]
            if self.network.myself == 0:
                private_set = self.inverted[keyx]
            else:
                private_set = self.inverted[keyy]
            self.start_pipeline('SetIntersectionSize', key, [private_set])
        return 4, None

    def stage_final(self, args):

        table = {}
        mode = None
        max = -1
        for tag in args:
            if tag == 'stage':
                continue
            if tag == 'samples':
                continue
            keyx, keyy = self.keys[tag]
            if keyx not in table:
                table[keyx] = {}
            table[keyx][keyy] = args[tag]['size_intersection']
            if args[tag]['size_intersection'] > max:
                max = args[tag]['size_intersection']
                mode = self.keys[tag]

        return -1, {'inputs': 2, 'result': {'mode': mode, 'table': table}}
