import secrets as _secrets

from fdrtd.plugins.simon.caches.cache import Cache
from fdrtd.plugins.simon.caches.additive import CacheAdditive
from fdrtd.plugins.simon.caches.functional import CacheFunctional
from fdrtd.plugins.simon.microprotocols.microprotocol import Microprotocol
from fdrtd.plugins.simon.accumulators.accumulator_statistics_contingency import AccumulatorStatisticsContingency


class MicroprotocolStatisticsContingency(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.secret_key = _secrets.token_bytes(32)

        self.n = self.network.count

        self.register_cache('samples', CacheAdditive(minimum=self.n))
        self.register_cache('input', Cache())
        self.register_cache('keysx', CacheFunctional(lambda x, y: set(x).union(set(y)), self.n, self.n))
        self.register_cache('keysy', CacheFunctional(lambda x, y: set(x).union(set(y)), self.n, self.n))
        self.register_cache('checkpoint2', CacheAdditive(minimum=self.n))
        self.register_cache('checkpoint3', CacheAdditive(minimum=self.n))

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['keysx', 'keysy'], self.stage_1)
        self.register_stage(2, ['checkpoint2'], self.stage_2)
        self.register_stage(3, ['checkpoint3'], self.stage_3)

        self.input = None
        self.result_cache = AccumulatorStatisticsContingency()

        self.table = {}
        self.keysx = []
        self.keysy = []
        self.tags = {}
        self.keys = {}

    def stage_0(self, args):

        self.network.broadcast(args['input']['samples'], 'samples')

        self.table = args['input']['table']
        self.network.broadcast([*self.table.keys()], 'keysx')
        keysy = set()
        for keyx in self.table:
            keysy = set.union(keysy, self.table[keyx].keys())
        self.network.broadcast([*keysy], 'keysy')
        return 1, None

    def stage_1(self, args):
        self.keysx = args['keysx']
        self.keysy = args['keysy']
        for keyx in self.keysx:
            for keyy in self.keysy:
                s = self.table.get(keyx, {}).get(keyy, 0)
                tag = 'sum_{}_{}'.format(keyx, keyy)
                self.tags[tag] = s
                self.keys[tag] = (keyx, keyy)
                self.register_cache(tag, Cache())
        self.network.broadcast(0, 'checkpoint2')
        return 2, None

    def stage_2(self, args):
        self.register_stage(4, ['samples', *self.tags.keys()], self.stage_final)
        self.network.broadcast(0, 'checkpoint3')
        return 3, None

    def stage_3(self, args):
        for tag in self.tags:
            self.start_pipeline('SecureSum', tag, self.tags[tag])
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
            table[keyx][keyy] = args[tag]['sum']
            if args[tag]['sum'] > max:
                max = args[tag]['sum']
                mode = self.keys[tag]

        return -1, {'inputs': self.n, 'result': {
                       'samples': args['samples'],
                       'mode': mode,
                       'table': table}}
