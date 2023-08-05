# This file is placed in the Public Domain.
# pylint: disable=E1101,C0116,C0413,C0411


"log"


import time


from .obj import Object, save
from .dbs import Db
from .utl import fntime
from .tmr import elapsed


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def log(event):
    if not event.rest:
        _nr = 0
        dbs = Db()
        for _fn, obj in dbs.find("log"):
            event.reply("%s %s %s" % (
                                      _nr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(_fn)))
                                     )
            _nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    save(obj)
    event.reply("ok")
