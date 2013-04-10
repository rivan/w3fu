from w3fu.storage import safe, Collection, Document, Property


class Worker(Document):

    id = Property('_id')
    provider_id = Property('provider_id')
    name = Property('name')

    def _new(self, provider_id, name):
        self.provider_id = provider_id
        self.name = name

    @property
    def embedded(self):
        return {'_id': self.id, 'name': self.name}


class Workers(Collection):

    _indexes = [('provider_id', {})]

    @safe()
    def update(self, worker):
        return self._c.update({'_id': worker.id},
                              {'$set': {'name': worker.name}})

    @safe(True)
    def find_provider(self, provider_id):
        return self._c.find({'provider_id': provider_id})

    @safe(True)
    def find_for_service(self, service):
        return self._c.find({'provider_id': service.provider_id,
                             '_id': {'$nin': service.worker_ids}})
