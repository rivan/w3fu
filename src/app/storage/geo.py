from w3fu.storage import safe, Collection, Document, Property


class IpRange(Document):

    begin = Property('a')
    end = Property('b')

    def _new(self, begin, end):
        self.begin = begin
        self.end = end

    def has_ip(self, ip):
        return self.begin <= ip <= self.end


class Place(Document):

    id = Property('_id')
    ext_id = Property('ext_id', hidden=True)
    name = Property('name')
    pattern = Property('pattern', hidden=True)
    region = Property('region')
    district = Property('district')
    ranges = Property('ranges', hidden=True)

    def _new(self, ext_id, name, region, district):
        self.ext_id = ext_id
        self.name = name
        self.pattern = name.lower()
        self.region = region
        self.district = district

    def has_ip(self, ip):
        for range in self.ranges:
            if range.has_ip(ip):
                return True
        return False


class Places(Collection):

    _indexes = [('ext_id', {'unique': True}),
               ('pattern', {}),
               ('ranges.a', {})]

    @safe()
    def replace_ranges(self, ext_id, ranges):
        raw = [range.raw for range in ranges]
        return self._c.update({'ext_id': ext_id}, {'$set': {'ranges': raw}},
                              safe=True)['n']

    @safe(True)
    def find_ip(self, ip):
        doc = self._c.find_one({'ips.a': {'$lte': ip}}).sort('ranges.a', -1)
        if doc is not None and doc.has_ip(ip):
            return doc
        return None

    @safe(True)
    def find_pattern(self, pattern):
        return self._c.find({'pattern': {'$regex': '^' + pattern.lower()}}
                            ).sort('pattern').limit(10)

    @safe(True)
    def find_name(self, name):
        return self._c.find_one({'pattern': name.lower()})
