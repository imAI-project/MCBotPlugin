from __future__ import annotations

import logging
import os
import sys
import shutil
import traceback
import datetime
import json

import yaml

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

from . import rth
from . import app
from .routines import online_track
from .dao import mongo
from .utils import mctool


# 注册插件
@register(
    name="MCBotPlugin",
    description="为 Minecraft 服务器群提供服务",
    version="0.1",
    author="RockChinQ",
)
class MCBotPlugin(Plugin):
    ap: app.Application

    config: dict

    def __init__(self, plugin_host: PluginHost):
        logging.info("[MCBot] 检查配置文件..")
        if not os.path.exists("mcbot.yaml"):
            # 拷贝 plugins/MCBotPlugin/mcbot-template.yaml 到当前目录
            shutil.copyfile(
                os.path.join(os.path.dirname(__file__), "mcbot-template.yaml"),
                "mcbot.yaml",
            )
            logging.critical("[MCBot] 请修改 mcbot.yaml 后重启 QChatGPT.")

            raise Exception("[MCBot] 已生成配置文件，请修改 mcbot.yaml 后重启 QChatGPT.")
        else:
            logging.info("[MCBot] 构建实例..")

            with open("mcbot.yaml") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)

            ap = app.Application()

            mongodb = mongo.MongoDBManager(self.config["database"]["mongo"])

            ap.dao = mongodb

            online_track_routine = online_track.OnlinePlayerTrackRoutine(ap)

            routines = [online_track_routine]

            routine_host = rth.RoutineHost(routines)

            ap.rth = routine_host

            self.ap = ap

            ap.start()

    def _check_priority(self, sender_id: int, is_admin: bool):
        if 'inherit' in self.config['admin'] and is_admin:
            return True
        elif sender_id in self.config['admin']:
            return True
        
        return False

    @on(GroupCommandSent)
    def on_group_command_sent(
        self,
        event: EventContext,
        launcher_id: int,
        sender_id: str,
        command: str,
        params: list[str],
        is_admin: bool,
        **kwargs
    ):
        
        reply_text = ""
        try:
            if command == "bind":

                if self._check_priority(
                    sender_id,
                    is_admin
                ):
                    event.prevent_default()
                    if len(params) == 1:
                        self.ap.dao.bind_server(launcher_id, params[0])
                        reply_text = "绑定成功。"
                    else:
                        reply_text = "参数错误。"
            elif command == "unbind":

                if self._check_priority(
                    sender_id,
                    is_admin
                ):
                    event.prevent_default()
                    self.ap.dao.unbind_server(launcher_id)
                    reply_text = "解绑成功。"
            elif command == "status":
                event.prevent_default()
                bind_server = self.ap.dao.get_bind_server(launcher_id)

                if bind_server:
                    server_addr = bind_server.split(":")[0]
                    server_port = bind_server.split(":")[1] if len(bind_server.split(":")) > 1 else 25565
                    
                    stats = mctool.ping(server_addr, server_port)

                    players = stats['players']['sample'] if 'sample' in stats['players'] else []
                    players = [
                        player[0]
                        for player in players
                    ]

                    player_str = '\n'.join(players)

                    reply_text = f"""{stats['description']}
版本: {stats['version']['name']}
在线玩家: \n{player_str}"""
                else:
                    reply_text = "未绑定服务器。"
            elif command == "time":
                event.prevent_default()
                period = 24*60

                if len(params) == 1:
                    period = int(params[0])

                start = datetime.datetime.now() - datetime.timedelta(minutes=period)
                end = datetime.datetime.now()
                
                start_str = start.strftime("%Y-%m-%d %H:%M")
                end_str = end.strftime("%Y-%m-%d %H:%M")

                online_time = self.ap.dao.count_record_time(
                    start,
                    end,
                    self.ap.dao.get_bind_server(launcher_id)
                )

                online_time = sorted(online_time.items(), key=lambda x: x[1], reverse=True)

                reply_text = f"在线时长统计: \n{start_str} - {end_str}\n\n" + '\n'.join([
                    f"{player}: {int(time/60)} 分钟"
                    for player, time in online_time
                ])

        except Exception as e:
            reply_text = f"操作失败: {e}"
            traceback.print_exc()
        
        event.add_return(
            "reply",
            [
                "[MCBot] "+reply_text
            ]
        )

    # 插件卸载时触发
    def __del__(self):
        pass
