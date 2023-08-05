import numpy as _numpy

from fdrtd.plugins.simon.caches.cache import Cache
from fdrtd.plugins.simon.microprotocols.microprotocol import Microprotocol


class MicroprotocolStatisticsRegressionOLSVertical(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.register_cache('input', Cache())
        self.register_cache('final', Cache())

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['final'], self.stage_1)

    def stage_0(self, args):
        if self.network.myself == 0:
            x = _numpy.array(args['input'])
            xt = x.transpose()
            n = _numpy.matmul(xt, x)
            ninv = _numpy.linalg.inv(n)
            mp = _numpy.matmul(ninv, xt)
            self.start_pipeline('SecureMatrixMultiplication', 'final', [mp.tolist()])
        else:
            self.start_pipeline('SecureMatrixMultiplication', 'final', [[[x] for x in args['input']]])
        return 1, None

    def stage_1(self, args):
        return -1, {'inputs': 2,  # self.n,
                    'result': {
                        'mle': args['final']['product']}}
