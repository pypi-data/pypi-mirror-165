import numpy as _numpy

from fdrtd.plugins.simon.caches.cache import Cache
from fdrtd.plugins.simon.microprotocols.microprotocol import Microprotocol


class MicroprotocolSecureMatrixMultiplication(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.register_cache('input', Cache())
        self.register_cache('dimX', Cache())
        self.register_cache('dimY', Cache())
        self.register_cache('intermediateV', Cache())
        self.register_cache('intermediateW', Cache())
        self.register_cache('final', Cache())

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['dimX', 'dimY'], self.stage_1)
        self.register_stage(2, ['intermediateV'], self.stage_2)
        self.register_stage(3, ['intermediateW'], self.stage_3)
        self.register_stage(4, ['final'], self.stage_4)

        self.M = None
        self.n = self.p = self.q = 0
        self.v = None

    def stage_0(self, args):
        self.M = _numpy.array(args['input'])
        self.network.broadcast(self.M.shape, 'dimX' if self.network.myself == 0 else 'dimY')
        return 1, None

    def stage_1(self, args):
        self.p = args['dimX'][0]
        self.n = args['dimX'][1]
        if args['dimY'][0] != args['dimX'][1]:
            raise RuntimeError("matrix shapes not compatible")
        self.q = args['dimY'][1]

        if self.network.myself == 0:
            xt = self.M.transpose()
            q, r = _numpy.linalg.qr(xt, mode='complete')
            g = int((self.p*self.n)/(self.p+self.q))
            z = q[:, self.p:self.p+g]
            self.v = _numpy.identity(self.n) - _numpy.matmul(z, z.transpose())
            self.network.broadcast(self.v.tolist(), 'intermediateV')

        return 2, None

    def stage_2(self, args):

        if self.network.myself == 1:
            v = args['intermediateV']
            w = _numpy.matmul(v, self.M)
            self.network.broadcast(w.tolist(), 'intermediateW')

        return 3, None

    def stage_3(self, args):

        if self.network.myself == 0:
            w = args['intermediateW']
            result = _numpy.matmul(self.M, w)
            self.network.broadcast(result.tolist(), 'final')

        return 4, None

    def stage_4(self, args):
        return -1, {'inputs': 2,  # self.n,
                    'result': {
                        'product': args['final']}}
