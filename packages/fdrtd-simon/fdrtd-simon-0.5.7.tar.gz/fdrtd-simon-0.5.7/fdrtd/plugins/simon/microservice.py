import uuid as _uuid
import time as _time

from fdrtd.plugins.simon.task import TaskSimon
from fdrtd.plugins.simon.sync_api import SyncApi


class MicroserviceSimon:

    def __init__(self):
        self.tasks = {}
        self._the_cache = []

    def get_task(self, task_id):
        if task_id in self.tasks:
            return self.tasks.get(task_id)
        else:
            return None

    def create_task(self, microprotocol, network, parameters=None, task_id=None, parent=None):

        if task_id is None:
            task_id = str(_uuid.uuid4())

        if parameters is None:
            parameters = {}

        task = TaskSimon(self, network, microprotocol, parameters, task_id, parent)

        for item in self._the_cache:
            if item['task_id'] == task_id:
                task.peer_to_peer(item['body'])

        self.tasks[task_id] = task
        return task

    def join_task(self, invitation, network):

        task_id = invitation['task_id']

        task = TaskSimon(self, network, invitation['microprotocol'], invitation['parameters'], task_id, invitation['parent'])

        for item in self._the_cache:
            if item['task_id'] == task_id:
                task.peer_to_peer(item['body'])

        self.tasks[task_id] = task
        return task

    def peer_to_peer(self, callback, body):
        if callback in self.tasks:
            self.tasks[callback].peer_to_peer(body)
        else:
            self._the_cache.append({'task_id': callback, 'body': body})
        return None

    def compute(self, microprotocol, data, network):
        sync_api = SyncApi(network['nodes'][0])
        if network['myself'] == 0:
            task = self.create_task(microprotocol, network)
            invitation = task.invite()
            sync_api.send_broadcast(invitation, network['uuid'])
        else:
            invitation = sync_api.wait_for_broadcast(network['uuid'])
            task = self.join_task(invitation, network)
        task.input(data)
        task.start()
        result = task.result()
        while result is None:
            _time.sleep(0.02)
            result = task.result()
        return result
