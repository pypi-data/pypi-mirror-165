# -*- coding: utf-8 -*-

import os
import fcntl
import logging

logger = logging.getLogger(__name__)

CONFIG_FILE_LOCK_DIRNAME = '/var/fileLock/'
CONFIG_STRICT_FILE_LOCK_DIRNAME = '/var/fileLock/'


class FileLock(object):
    def __init__(self):
        self._f = None
        self._lockName=None
        self._dirName = CONFIG_FILE_LOCK_DIRNAME
        if not os.path.exists(self._dirName):
            os.makedirs(self._dirName)

    # @wraplog
    def acquireLock(self, lockname, blocking=False, identifier=None, expire=None, timeout=-1):
        self._lockName = lockname
        fileName = os.path.join(self._dirName,"{}.lock".format(lockname))
        self._f = open(fileName, "wb")
        try:
            if blocking:
                fcntl.flock(self._f, fcntl.LOCK_EX)
            else:
                fcntl.flock(self._f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except:
            self._f .close()
            return False

    # @wraplog
    def releaseLock(self, lockname, identifier=None):
        fileName = os.path.join(self._dirName,"{}.lock".format(lockname))
        self._f = open(fileName, "wb")
        fcntl.flock(self._f , fcntl.LOCK_UN)
        self._f .close()





class StrictFileLock(object):
    def __init__(self, semaphore):
        self._f = None
        self._lockName = None
        self._semaphore = semaphore
        if not os.path.exists(CONFIG_STRICT_FILE_LOCK_DIRNAME):
            os.makedirs(CONFIG_STRICT_FILE_LOCK_DIRNAME)

    # @wraplog
    def acquireLock(self, lockname, blocking=False, identifier=None, expire=None,  timeout=-1):
        self._lockName = lockname
        fileName = os.path.join(CONFIG_STRICT_FILE_LOCK_DIRNAME, "{}.lock".format(lockname))
        self._f = open(fileName, "wb")
        try:
            if blocking:
                fcntl.flock(self._f, fcntl.LOCK_EX)
                self._semaphore.acquire()
                return True
            else:
                fcntl.flock(self._f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                ret = self._semaphore.acquire(blocking=False)
                if not ret:
                    fcntl.flock(self._f, fcntl.LOCK_UN)
                    self._f.close()
                    return False
                else:
                    return True
        except:
            self._f .close()
            return False

    # @wraplog
    def releaseLock(self, lockname, identifier=None):
        self._semaphore.release()
        fileName = os.path.join(CONFIG_STRICT_FILE_LOCK_DIRNAME, "{}.lock".format(lockname))
        self._f = open(fileName, "wb")
        fcntl.flock(self._f , fcntl.LOCK_UN)
        self._f .close()
