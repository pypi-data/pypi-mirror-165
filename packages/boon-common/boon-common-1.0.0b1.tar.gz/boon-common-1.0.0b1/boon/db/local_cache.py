#!/usr/bin/env python3

# BoBoBo

import time
from collections import namedtuple

CacheValue = namedtuple('CacheValue', ['v', 'timestamp', 'timeout'])

cache = {}


def put(k, v, timeout=None):
    cv = CacheValue(v, time.time(), timeout)
    cache[k] = cv


def get(k, default=None):
    if k in cache:
        cv = cache.get(k)
        if cv.timeout:
            if time.time() - cv.timestamp >= cv.timeout:
                del cache[k]
                return None
        return cv.v
    else:
        return default
