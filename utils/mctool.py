from mctools import PINGClient

def ping(host, port) -> dict:
    client = PINGClient(host, port)
    client.ping()

    stats = client.get_stats()

    # 遍历每一个str字段，删除其中的 \x1b[0m 字符串
    def recursive_remove_escape_sequence(obj):
        if isinstance(obj, str):
            return obj.replace("\x1b[0m", "")
        elif isinstance(obj, list):
            return [recursive_remove_escape_sequence(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: recursive_remove_escape_sequence(value) for key, value in obj.items()}
        else:
            return obj
        
    return recursive_remove_escape_sequence(stats)

if __name__ == "__main__":
    print(ping("mc.tjut.top", 25565))