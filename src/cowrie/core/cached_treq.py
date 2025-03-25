import treq
import cachetools
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import defer
import time

from twisted.python import log

# In-memory cache with 15 minute TTL
cache = cachetools.TTLCache(maxsize=1000, ttl=900)

def _cache_key(method, url, params=None, data=None):
    return f"{method.upper()}:{url}:{params}:{data}"

@inlineCallbacks
def get(url, **kwargs):
    key = _cache_key("GET", url, kwargs.get("params"), kwargs.get("data"))
    if key in cache:
        log.msg(f"Cache hit for {url}")
        returnValue(cache[key])
    log.msg(f"Cache miss for {url}")
    response = yield treq.get(url, **kwargs)
    cache[key] = response
    returnValue(response)

@inlineCallbacks
def post(url, **kwargs):
    key = _cache_key("POST", url, kwargs.get("params"), kwargs.get("data"))
    if key in cache:
        log.msg(f"Cache hit for {url}")
        returnValue(cache[key])
    log.msg(f"Cache miss for {url}")
    response = yield treq.post(url, **kwargs)
    cache[key] = response
    returnValue(response)

@inlineCallbacks
def collect(response, collect, **kwargs):
    content = yield treq.collect(response, collect)
    returnValue(content)
