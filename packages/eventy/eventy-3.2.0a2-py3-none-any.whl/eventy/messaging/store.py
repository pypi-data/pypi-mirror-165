# Copyright (c) Qotto, 2021

from __future__ import annotations

import logging
from abc import ABC
from datetime import datetime
from enum import Enum
from typing import Iterable, Optional, Dict, Callable

from eventy.messaging.errors import MessagingError
from eventy.record import Record

__all__ = [
    'RecordStore',
    'Cursor',
    'RecordWriteStore',
    'RecordStoreWithInitialization',
]

from eventy.trace_id import local_trace

logger = logging.getLogger(__name__)


class Cursor(Enum):
    """
    Read cursor
    """

    BEGIN = 0
    ACKNOWLEDGED = 1
    CURRENT = 2


class RecordWriteStore:
    def write(self, record: Record) -> None:
        raise NotImplementedError

    def with_peek(self, peek_function: Callable[[Record], None]) -> 'RecordWriteStore':
        class WithPeek(RecordWriteStore):
            def __init__(self, write_store: 'RecordWriteStore'):
                self.write_store = write_store

            def write(self, record: Record) -> None:
                with local_trace(correlation_id=record.correlation_id):
                    peek_function(record)
                self.write_store.write(record)

        return WithPeek(self)


class RecordStore:
    """
    A RecordStore is a transactional read and write store
    """

    def __init__(self):
        self.topics: Dict[str, Cursor] = dict()
        self.assignments: dict[str, tuple[Optional[datetime], Optional[list[int]]]] = dict()

    def register_topic(self, topic: str, cursor: Cursor = Cursor.ACKNOWLEDGED):
        """
        Register an automatic subscription to a topic.

        In some implementation this cannot be used simultaneously with register_assignment.
        """
        if topic in self.topics:
            raise MessagingError(f"Topic {topic} was already registered.")
        if self.assignments:
            raise MessagingError(f"Assignment already set, cannot register topics.")
        self.topics[topic] = cursor

    def register_assignment(self, topic: str, since_date: datetime = None, offsets: list[int] = None):
        """
        Register a manual assignment to a topic.

        In some implementation this cannot be used simultaneously with register_topic.
        """
        if topic in self.assignments:
            raise MessagingError(f"Assignment already set for topic {topic}.")
        if self.topics:
            raise MessagingError(f"Topic already registered, cannot set assignment.")
        if not since_date and not offsets:
            raise MessagingError(f"Either since_date or offsets must be provided.")
        if since_date and offsets:
            raise MessagingError(f"Only one of since_date or offsets can be provided.")
        self.assignments[topic] = (since_date, offsets)

    def has_reached_end_of_topics(self) -> bool:
        """
        Returns True if all topics have been consumed and not records are currently available to read.
        """
        raise NotImplementedError

    def read(
        self,
        max_count: int = 1,
        timeout_ms: Optional[int] = None,
        auto_ack: bool = False
    ) -> Iterable[Record]:
        """
        Fetch between 0 and max_count records
        """
        raise NotImplementedError

    def ack(self, timeout_ms=None) -> None:
        """
        Acknowledge all fetched records
        """
        raise NotImplementedError

    def write(self, record: Record, topic: str, timeout_ms=None) -> None:
        """
        Add to current transaction if a transaction was started,
        and write immediately otherwise
        """
        raise NotImplementedError

    def write_now(self, record: Record, topic: str, timeout_ms=None) -> None:
        """
        Write immediately otherwise, even if a transaction was started
        """
        raise NotImplementedError

    def start_transaction(self) -> None:
        """
        Start a new transaction
        """
        raise NotImplementedError

    def commit(self, timeout_ms: Optional[int] = None) -> None:
        """
        Ack all consumed records, and produce all records added to transaction
        """
        raise NotImplementedError

    def abort(self, timeout_ms: Optional[int] = None) -> None:
        """
        Roll back to previously acknowledged record, discard records in current transaction
        """
        raise NotImplementedError


class RecordStoreWithInitialization(RecordStore, ABC):
    def initialize(self) -> None:
        raise NotImplementedError
