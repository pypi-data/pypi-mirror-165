import math as _math
import numpy as _numpy

from fdrtd.plugins.simon.caches.cache import Cache
from fdrtd.plugins.simon.microprotocols.microprotocol import Microprotocol


class MicroprotocolStatisticsRegressionLogitVertical(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.register_cache('input', Cache())
        self.register_cache('final', Cache())

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['final'], self.stage_1)

    def stage_0(self, args):
        if self.network.myself == 0:
            n = len(args['input'])
            m = len(args['input'][0])
            regressor = [[1, *row] for row in args['input']]
            x = _numpy.array(regressor)
            xt = x.transpose()
            w0 = [0.0 for i in range(m+1)]
            mu = [1.0 / _math.exp(-sum(w0[k] * x[i][k] for k in range(m+1))) for i in range(n)]
            s = _numpy.diag(mu)

            xts = _numpy.matmul(xt, s)
            xtsx = _numpy.matmul(xts, x)
            xtsxi = _numpy.linalg.inv(xtsx)
            xtsxixt = _numpy.matmul(xtsxi, xt)

            sx = _numpy.matmul(s, x)
            sxw = _numpy.matmul(sx, w0)

            sxwymu = sxw + _numpy.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1]) - mu

            self.w1 = _numpy.matmul(xtsxixt, sxwymu)

            #n = _numpy.matmul(xt, x)
            #ninv = _numpy.linalg.inv(n)
            #mp = _numpy.matmul(ninv, xt)
            #self.start_pipeline('SecureMatrixMultiplication', 'final', [mp.tolist()])
        else:
            pass
            #self.start_pipeline('SecureMatrixMultiplication', 'final', [[[x] for x in args['input']]])
        return 1, None

    def stage_1(self, args):
        return -1, {'inputs': 2,  # self.n,
                    'result': {
                        'mle': self.w1
                    #    args['final']['product']
                    }}
