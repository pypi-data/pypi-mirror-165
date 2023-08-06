# -*- coding: utf-8 -*-
import copy

from manoutils.config.defualtConfig import configItems


class ConfigManager(object):
    configs = dict()
    def __init__(self):
        self.loadConfigJsonItmes(configItems=configItems)

    def makeConfigName(mod, sub_mod="", desc=""):
        if sub_mod:
            return "{}_{}_{}".format(mod.upper(), sub_mod.upper(), desc.upper())
        else:
            return "{}_{}".format(mod.lower(), desc.lower())

    def getConfigItem(self, name=None, defaultVal=""):
        if not name:
            return copy.deepcopy(ConfigManager.configs)
        else:
            return ConfigManager.configs.get(name, defaultVal)

    def setConfigItem(self, name, value):
        setattr(self, name, value)
        ConfigManager.configs.update({name: value})

    def getManoIp(self):
        return self.getConfigItem("MANO_IP")

    def getManoPort(self):
        return self.getConfigItem("MANO_PORT")

    def setManoIp(self, ip):
        self.setConfigItem("MANO_IP", ip)

    def setManoPort(self, port):
        self.setConfigItem("MANO_PORT", port)

    def loadConfigFile(self):
        pass

    def loadConfigJsonItmes(self,configItems):
        for name, value in configItems.items():
            self.setConfigItem(name=name, value=value)


configMgr = ConfigManager()
