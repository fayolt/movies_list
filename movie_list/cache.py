from pymemcache.client import base

client = base.Client(('cache', 11211), encoding="utf-8")
