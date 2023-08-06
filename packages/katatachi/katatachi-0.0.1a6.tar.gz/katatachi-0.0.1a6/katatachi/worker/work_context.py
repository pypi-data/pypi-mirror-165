import logging

from katatachi.content import ContentStore
from katatachi.interface.worker import MetadataStore
from katatachi.interface.worker import WorkContext
from katatachi.utils import now_ms
from .metadata_store import MetadataStoreFactory
from .worker_log_store import WorkerLogStoreFactory, WorkerLogLine


class WorkContextImpl(WorkContext):
    def __init__(
        self,
        worker_id: str,
        content_store: ContentStore,
        metadata_store_factory: MetadataStoreFactory,
        worker_log_store_factory: WorkerLogStoreFactory,
    ):
        worker_log_store = worker_log_store_factory.build(worker_id)

        class WorkerLogStoreHandler(logging.Handler):
            def emit(self, record):
                message = self.format(record)
                worker_log_store.log(WorkerLogLine(message, now_ms()))

        # still need the prefix to globally configure logging for all katatachi workers
        self._logger = logging.getLogger(f"katatachi.worker.{worker_id}")
        self._logger.addHandler(WorkerLogStoreHandler())
        self._content_store = content_store
        self._metadata_store = metadata_store_factory.build(worker_id)

    def logger(self) -> logging.Logger:
        return self._logger

    def content_store(self) -> ContentStore:
        return self._content_store

    def metadata_store(self) -> MetadataStore:
        return self._metadata_store


class WorkContextFactory(object):
    def __init__(
        self,
        content_store: ContentStore,
        metadata_store_factory: MetadataStoreFactory,
        worker_log_store_factory: WorkerLogStoreFactory
    ):
        self.content_store = content_store
        self.metadata_store_factory = metadata_store_factory
        self.worker_log_store_factory = worker_log_store_factory

    def build(self, worker_id: str) -> WorkContext:
        return WorkContextImpl(
            worker_id=worker_id,
            content_store=self.content_store,
            metadata_store_factory=self.metadata_store_factory,
            worker_log_store_factory=self.worker_log_store_factory
        )
