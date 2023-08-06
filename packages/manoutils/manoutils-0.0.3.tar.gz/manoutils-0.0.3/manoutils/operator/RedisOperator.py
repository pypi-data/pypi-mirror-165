# -*- coding: utf-8 -*-
import redis
import json
import logging
import time

from rediscluster import StrictRedisCluster
from rediscluster import RedisCluster
from rediscluster.connection import ClusterConnectionPool
from manoutils.config.ConfigManager import configMgr

logger = logging.getLogger(__name__)


def retry(retry_times=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retry_time = 0
            while retry_time < retry_times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retry_time += 1
                    time.sleep(delay)
                    logger.warning('Error:operate redis has error: %s', e)
                    RedisOperator().getPool(need_reconnect=True)
            else:
                raise Exception("operate redis error with retry %s times" % retry_times)

        return wrapper

    return decorator


class RedisOperator(object):
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(RedisOperator, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init__(self):
        self.conn = None
        self.pool = None
        self.getPool()
        self.getConn()

    def getNodes(self):
        nodes = []
        REDIS_ADDR = configMgr.getConfigItem("REDIS_ADDR")
        if not REDIS_ADDR:
            raise Exception("Redis address is null!")
        addrs = configMgr.REDIS_ADDR.split(' ')
        for addr in addrs:
            node = addr.split(':')
            nodes.append({'host': node[0], 'port': node[1]})
        return nodes

    def getPool(self, need_reconnect=False):
        REDIS_PASSWD = configMgr.getConfigItem("REDIS_PASSWD")
        if self.pool and not need_reconnect:
            self.pool = self.pool
            return self.pool
        nodes = self.getNodes()
        if len(nodes) == 1:
            node = nodes[0]
            self.pool = redis.ConnectionPool(host=node["host"], port=node["port"], password=REDIS_PASSWD, db=0)
        elif len(nodes) > 1:
            self.pool = ClusterConnectionPool(startup_nodes=nodes, password=REDIS_PASSWD,
                                              socket_connect_timeout=2)
        return self.pool

    def getConn(self):
        nodes = self.getNodes()
        pool = self.getPool()
        if len(nodes) == 1:
            self.conn = redis.Redis(connection_pool=pool)
        elif len(nodes) > 1:
            self.conn = RedisCluster(connection_pool=pool)
        return self.conn

    @retry(retry_times=10, delay=1)
    def isKeyExists(self, key):
        ret = self.conn.exists(key)
        return ret

    @retry(retry_times=20, delay=2)
    def getKeys(self, subkey):
        try:
            keys = self.conn.keys(subkey)
            return keys
        except Exception as e:
            self.conn = RedisOperator().conn
            raise e

    @retry(retry_times=10, delay=1)
    def delKey(self, key):
        ret = self.conn.delete(key)
        return ret

    @retry(retry_times=10, delay=1)
    def setString(self, key, value, time=None):
        if time:
            ret = self.conn.setex(name=key, time=time, value=value)
        else:
            ret = self.conn.set(name=key, value=value)
        return ret

    @retry(retry_times=10, delay=1)
    def getString(self, key):
        ret = ""
        if self.conn.exists(key):
            ret = self.conn.get(key).decode()
        return ret

    @retry(retry_times=10, delay=1)
    def getJson(self, key):
        ret = self.conn.get(key).decode()
        try:
            return json.loads(ret)
        except Exception as e:
            ret_json = ret.replace("'", "\"")
            return eval(ret_json)

    def getJsons(self, subkey):
        entities = []
        keys = self.getKeys(subkey)
        if not keys:
            return entities
        for k in keys:
            entity = self.getJson(k)
            entities.append(entity)
        return entities

    @retry(retry_times=10, delay=1)
    def setHash(self, name, key, value):
        ret = self.conn.hset(name, key, value)
        return ret

    @retry(retry_times=10, delay=1)
    def getHash(self, name, key=None):
        if key:
            ret = self.conn.hget(name, key)
        else:
            ret = self.conn.hgetall(name)
        return ret

    @retry(retry_times=10, delay=1)
    def delHash(self, name, key=None):
        if key:
            ret = self.conn.hdel(name, key)
        else:
            ret = self.conn.delete(name)
        return ret

    def get_nfvo_alarmseq(self):
        key = 'NfvoAlarmSeq'
        msgseq = 1
        if self.isKeyExists(key):
            msgseq = int(self.getJson(key)) + 1
        self.setString(key, str(msgseq))
        return msgseq

    @retry(retry_times=20, delay=2)
    def ttl(self, name):
        count = self.conn.ttl(name)
        if count or count == 0:
            return int(count)
        else:
            return 0
