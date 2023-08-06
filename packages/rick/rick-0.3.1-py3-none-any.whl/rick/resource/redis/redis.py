import pickle

import redis

from rick.crypto import Fernet256
from rick.resource import CacheInterface


class RedisCache(CacheInterface):
    """
    Implements basic cache operations on a Redis backend

    Data is serialized using pickle. To access actual Redis-specific funcions, the client is available via client()
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: list of optional parameters

        Available parameters:
            host='localhost'
            port=6379,
            db=0
            password=None
            socket_timeout=None,
            socket_connect_timeout=None
            socket_keepalive=None
            socket_keepalive_options=None
            connection_pool=None
            unix_socket_path=None,
            encoding='utf-8'
            encoding_errors='strict'
            charset=None
            errors=None,
            decode_responses=False
            retry_on_timeout=False
            ssl=False
            ssl_keyfile=None
            ssl_certfile=None
            ssl_cert_reqs='required'
            ssl_ca_certs=None
            max_connections=None
            single_connection_client=False
            health_check_interval=0
        """
        self._serialize = pickle.dumps
        self._deserialize = pickle.loads
        self._prefix = None
        self._redis = redis.Redis(**kwargs)

    def get(self, key):
        if self._prefix is not None:
            key = key + self._prefix
        v = self._redis.get(key)
        if v is None:
            return None
        return self._deserialize(v)

    def set(self, key, value, ttl=None):
        if self._prefix is not None:
            key = key + self._prefix
        value = self._serialize(value)
        return self._redis.set(key, value, ex=ttl)

    def has(self, key):
        if self._prefix is not None:
            key = key + self._prefix
        return self._redis.exists(key)

    def remove(self, key):
        if self._prefix is not None:
            key = key + self._prefix
        return self._redis.unlink(key)

    def purge(self):
        return self._redis.flushdb()

    def client(self) -> redis.Redis:
        return self._redis

    def close(self):
        self._redis.close()
        self._redis = None

    def set_prefix(self, prefix):
        self._prefix = prefix

    def __del__(self):
        self._redis.close()
        self._redis = None


class CryptRedisCache(RedisCache):

    def __init__(self, key=None, **kwargs):
        """
        :param key_list: base64-encode key (256 bit)
        :param kwargs: list of optional parameters

        Available parameters:
            host='localhost'
            port=6379,
            db=0
            password=None
            socket_timeout=None,
            socket_connect_timeout=None
            socket_keepalive=None
            socket_keepalive_options=None
            connection_pool=None
            unix_socket_path=None,
            encoding='utf-8'
            encoding_errors='strict'
            charset=None
            errors=None,
            decode_responses=False
            retry_on_timeout=False
            ssl=False
            ssl_keyfile=None
            ssl_certfile=None
            ssl_cert_reqs='required'
            ssl_ca_certs=None
            max_connections=None
            single_connection_client=False
            health_check_interval=0
        """
        if key is None:
            raise ValueError("Empty fernet encryption key")
        super().__init__(**kwargs)
        self._crypt = Fernet256(key)
        self._serialize = self._serializer
        self._deserialize = self._deserializer

    def _serializer(self, data):
        if data is not None:
            return self._crypt.encrypt(pickle.dumps(data))
        return data

    def _deserializer(self, data):
        if data is not None:
            return pickle.loads(self._crypt.decrypt(data))
        return data
