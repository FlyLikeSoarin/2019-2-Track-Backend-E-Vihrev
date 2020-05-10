from collections import OrderedDict


class LRUCache():
    def __init__(self, capacity=10):
        self.capacity=capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key, last=False)
            return self.cache[key]
        else:
            return ''

    def set(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key, last=False)
        if len(self.cache) > self.capacity:
            self.cache.popitem()

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]


class LFUCacheEntry():
    def __init__(self, data):
        self.data = data
        self.freq = 0

    def increment_freq(self):
        self.freq += 1


class LFUCache():
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.cache[key].increment_freq()
            return self.cache[key].data
        else:
            return ''

    def set(self, key, value):
        if len(self.cache) >= self.capacity and key not in self.cache:
            key_to_remove = sorted(self.cache.items(), key=(lambda item: item[1].freq))[-1]
            self.remove(key_to_remove)
        self.cache[key] = LFUCacheEntry(value)

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]
