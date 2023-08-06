# -*- coding: utf-8 -*-
import logging

from manoutils.operator.RedisOperator import RedisOperator
from manoutils.config.ConfigManager import configMgr

logger = logging.getLogger(__name__)


class TokenClient(object):
    def __init__(self):
        self._opr = RedisOperator()
        self._redis_key = ""

    def getToken(self, exsysId, exsysType):
        self.setExsysTokenKey(exsysId=exsysId, exsysType=exsysType)
        return self._opr.getString(self._redis_key)

    def checkToken(self, exsysId, exsysType, token):
        self.setLocalsysTokenKey(exsysId=exsysId, exsysType=exsysType)
        if not token:
            return False
        if self._opr.getString(self._redis_key) == token:
            return True
        else:
            return False

    def setExsysTokenKey(self, exsysId, exsysType):
        localSystemType = configMgr.getConfigItem("LOCAL_SYS_TYPE")
        localSystemType = localSystemType if localSystemType else "NFVO"
        if exsysType.lower() == "oss":
            self._redis_key = "TOKEN_{}_2_{}_{}".format(localSystemType, "cmoss".upper(), exsysId)
        else:
            self._redis_key = "TOKEN_{}_2_{}_{}".format(localSystemType, exsysType.upper(), exsysId)

    def setLocalsysTokenKey(self, exsysId, exsysType):
        localSystemType = configMgr.getConfigItem("LOCAL_SYS_TYPE")
        localSystemType = localSystemType if localSystemType else "NFVO"
        if exsysType.lower() == "oss":
            self._redis_key = "TOKEN_{}_2_{}_{}".format("cmoss".upper(), localSystemType, exsysId)
        else:
            self._redis_key = "TOKEN_{}_2_{}_{}".format(exsysType.upper(), localSystemType, exsysId)