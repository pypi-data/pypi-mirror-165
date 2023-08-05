# PyKV
PyKV is a key-value storage in the memory, it is simple and fast.

## Requirements
Python3.8+

## Installation
```bash
$ pip install pykv
```

## Example
```python
$ python
>>> from pykv import KV
>>> kv = KV(name="kv-app")
>>> kv.put("key1", "value1")        # the key1 default expires after 2 hours
>>> kv.get("key1")
'value1'
>>>
>>> kv.put("key2", "value2", ttl=5) # the key2 expires after 5 second
>>> kv.get("key2")                  # the key2 is deleted and return None after 5 second
>>>
```
