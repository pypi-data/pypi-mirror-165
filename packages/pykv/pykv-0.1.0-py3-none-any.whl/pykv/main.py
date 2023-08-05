from datetime import datetime, timedelta
from threading import Lock


class _KV:
    def __init__(self, k, v, ttl):
        self.k = k
        self.v = v

        self.create_time = datetime.now()
        self.ttl = ttl

    @property
    def expiration(self):
        return self.create_time + timedelta(seconds=self.ttl)

    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.expiration

    def __str__(self) -> str:
        return f"<{self.k}: {self.v}> - ttl: <{self.ttl}s> - expiration: <{self.expiration}>"

    def __call__(self):
        return self.v


class KV:
    def __init__(self, name):
        self.name = name

        self.kv = dict()
        self._lock = Lock()

    def get(self, k):
        v = self.kv.get(k)

        if v is None:
            return
        
        if v.is_expired:
            with self._lock:
                del self.kv[k]
        
        return v()

    def put(self, k, v, ttl=60*60*2):
        _kv = _KV(k, v, ttl=ttl)

        with self._lock:
            self.kv[k] = _kv

    def __str__(self) -> str:
        return f"{self.kv}"
