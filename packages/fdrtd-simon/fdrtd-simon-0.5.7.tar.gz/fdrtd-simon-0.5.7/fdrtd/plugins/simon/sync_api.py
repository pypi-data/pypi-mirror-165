from representation import Api


class SyncApi(Api):

    def join_barrier(self, parties, party, uuid):
        ms = self.create(plugin="Sync", microservice='Barrier')
        sync = ms.create(uuid=uuid)
        sync.arrive(party=party)
        while sync.arrived() < parties:
            pass
        sync.depart(party=party)
        while sync.departed() < parties:
            pass
        return sync.reset()

    def send_broadcast(self, message, uuid):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        return ms.send(uuid=uuid, message=message)

    def receive_broadcast(self, uuid):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        rec = ms.receive(uuid=uuid)
        if rec is None:
            return None
        return self.download(rec)

    def clear_broadcast(self, uuid):
        ms = self.create(plugin="Sync", microservice='Broadcast')
        return ms.delete(uuid=uuid)

    def wait_for_broadcast(self, uuid):
        response = None
        while not response:
            response = self.receive_broadcast(uuid=uuid)
        return response
