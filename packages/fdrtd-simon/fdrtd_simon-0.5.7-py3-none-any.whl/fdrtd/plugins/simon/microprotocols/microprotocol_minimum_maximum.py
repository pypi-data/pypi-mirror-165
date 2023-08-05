from fdrtd.plugins.simon.caches.cache import Cache
from fdrtd.plugins.simon.caches.functional import CacheFunctional
from fdrtd.plugins.simon.caches.additive import CacheAdditive
from fdrtd.plugins.simon.microprotocols.microprotocol import Microprotocol


class MicroprotocolMinimumMaximum(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.n = self.network.count

        self.intermediate = 0

        self.register_cache('input', Cache())
        self.register_cache('samples', CacheAdditive(minimum=self.n))
        self.register_cache('minimum', CacheFunctional(lambda x, y: x if x < y else y, minimum=self.n))
        self.register_cache('maximum', CacheFunctional(lambda x, y: x if x > y else y, minimum=self.n))

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['samples', 'minimum', 'maximum'], self.stage_1)

    def stage_0(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        self.network.broadcast(args['input']['minimum'], 'minimum')
        self.network.broadcast(args['input']['maximum'], 'maximum')
        return 1, None

    def stage_1(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'samples': args['samples'],
                        'minimum': args['minimum'],
                        'maximum': args['maximum']}}
