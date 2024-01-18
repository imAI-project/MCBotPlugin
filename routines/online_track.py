from __future__ import annotations
import logging

import func_timeout

from .. import rth, app
from ..utils import mctool


class OnlinePlayerTrackRoutine(rth.Routine):

    last_track_ts: int = 0

    def __init__(self, ap: app.Application):
        super().__init__(ap, 10, 60, True)

    def run(self):
        servers = self.ap.dao.get_server_list()
        logging.debug(f"[MCBot] 服务器列表: {servers}, 记录在线玩家..")

        for server in servers:
            @func_timeout.func_set_timeout(10)
            def wrapper(server):
                server_ip = server.split(":")[0]
                server_port = server.split(":")[1] if len(server.split(":")) > 1 else 25565

                info = mctool.ping(server_ip, server_port)

                players = info['players']['sample'] if 'sample' in info['players'] else []

                players = [
                    player[0]
                    for player in players
                ]

                if players:
                    self.ap.dao.insert_server_player_record(server, players, self.duration)

            try:
                wrapper(server)
            except func_timeout.exceptions.FunctionTimedOut:
                logging.warn(f"[MCBot] Ping server: {server} 超时.")
            except:
                logging.exception(f"[MCBot] Ping server: {server} 失败.")