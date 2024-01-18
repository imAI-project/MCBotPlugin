from __future__ import annotations

from . import rth
from .dao import model

class Application:
    rth: rth.RoutineHost

    dao: model.AbsDatabaseManager

    cfg: dict

    def __init__(self):
        pass

    def start(self):
        self.rth.schedule()