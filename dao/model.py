import abc
import datetime


class AbsDatabaseManager(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def bind_server(self, group: int, server_addr: str):
        pass

    @abc.abstractmethod
    def get_bind_server(self, group: int) -> str:
        pass

    @abc.abstractmethod
    def get_server_list(self) -> list:
        pass

    @abc.abstractmethod
    def unbind_server(self, group: int):
        pass

    @abc.abstractmethod
    def insert_server_player_record(
        self, server_addr: str, players: list, duration_seconds: int
    ):
        pass

    @abc.abstractmethod
    def get_server_player_record(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        server_addr: str,
    ) -> list:
        pass

    @abc.abstractmethod
    def count_record_time(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        server_addr: str,
    ) -> dict:
        """
        根据时段内所有记录，统计每个玩家的在线时长
        """
        pass
