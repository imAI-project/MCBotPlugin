from __future__ import annotations

import datetime

import pymongo
import pymongo.database

from . import model


COLL_SERVERS = "servers"
COLL_ONLINE_RECORDS = "online_records"


class MongoDBManager(model.AbsDatabaseManager):

    client: pymongo.MongoClient

    database: pymongo.database.Database

    def __init__(self, cfg: dict):
        self.client = pymongo.MongoClient(cfg['uri'])

        self.database = self.client[cfg['db']]

    def bind_server(self, group: int, server_addr: str):
        data = {
            "group": group,
            "server_addr": server_addr,
            "datetime": datetime.datetime.now()
        }

        self.database[COLL_SERVERS].insert_one(data)

    def get_bind_server(self, group: int) -> str:
        record = self.database[COLL_SERVERS].find_one({"group": group})
        if record:
            return record['server_addr']
        else:
            return None
    
    def get_server_list(self) -> list:
        return [server['server_addr'] for server in self.database[COLL_SERVERS].find()]
    
    def unbind_server(self, group: int):
        return self.database[COLL_SERVERS].delete_one({"group": group})
    
    def insert_server_player_record(
        self, server_addr: str, players: list, duration_seconds: int
    ):
        data = {
            "server_addr": server_addr,
            "players": players,
            "duration_seconds": duration_seconds,
            "datetime": datetime.datetime.now()
        }

        self.database[COLL_ONLINE_RECORDS].insert_one(data)

    def get_server_player_record(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        server_addr: str,
    ) -> list:
        return list(self.database[COLL_ONLINE_RECORDS].find({
            "datetime": {
                "$gte": start_time,
                "$lte": end_time
            },
            "server_addr": server_addr
        }))
    
    def count_record_time(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        server_addr: str,
    ) -> dict:
        records = self.get_server_player_record(start_time, end_time, server_addr)

        result = {}

        for record in records:
            for player in record['players']:
                if player not in result:
                    result[player] = 0
                result[player] += record['duration_seconds']
        
        return result
