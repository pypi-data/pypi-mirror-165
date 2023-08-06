import json
import redis
from typing import List
from dataclasses import dataclass


@dataclass
class WorkerLogLine:
    message: str
    created_ms: int

    def to_str(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {
            "message": self.message,
            "created_ms": self.created_ms
        }

    @staticmethod
    def from_str(s: str):
        d = json.loads(s)
        return WorkerLogLine(
            d["message"],
            d["created_ms"]
        )


class WorkerLogStore(object):
    LOG_RETENTION_COUNT = 1000

    def __init__(self, redis_url: str, key_prefix: str, worker_id: str):
        self.db = redis.from_url(redis_url)
        self.key = f"{key_prefix}.worker_logs.{worker_id}"

    def log(self, log_line: WorkerLogLine):
        self.db.rpush(self.key, log_line.to_str())

    def get_logs(self) -> List[WorkerLogLine]:
        log_lines = []
        for item in self.db.lrange(self.key, 0, -1):
            log_lines.append(WorkerLogLine.from_str(item.decode()))
        return log_lines

    def trim_logs(self):
        self.db.ltrim(self.key, -WorkerLogStore.LOG_RETENTION_COUNT, -1)


class WorkerLogStoreFactory(object):
    def __init__(self, redis_url: str, key_prefix: str):
        self.redis_url = redis_url
        self.key_prefix = key_prefix

    def build(self, worker_id) -> WorkerLogStore:
        return WorkerLogStore(
            self.redis_url,
            self.key_prefix,
            worker_id
        )
