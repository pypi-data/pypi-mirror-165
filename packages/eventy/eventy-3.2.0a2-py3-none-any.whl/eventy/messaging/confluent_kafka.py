# Copyright (c) Qotto, 2021

from __future__ import annotations

import logging
import socket
import threading
from concurrent.futures import Future
from datetime import datetime
from threading import Thread, Lock
from time import sleep
from typing import Iterable, Optional
from uuid import uuid4

from confluent_kafka.admin import ClusterMetadata, TopicMetadata

from confluent_kafka import Producer, Consumer, Message, TopicPartition
from eventy.config import SERVICE_NAME
from eventy.messaging.errors import MessagingError
from eventy.messaging.store import RecordStoreWithInitialization
from eventy.record import Record
from eventy.serialization import RecordSerializer

__all__ = [
    'CKStore',
]

from eventy.trace_id import local_trace

logger = logging.getLogger(__name__)


def _message_str(message: Message) -> str:
    """
    String representation of kafka message formatted as "topic[partition]:offset".
    """
    return f'{message.topic()}[{message.partition()}]:{message.offset()}'


def _partitions_str(partitions: list[TopicPartition]) -> str:
    """
    String representation of a topic-partition list, including offsets and errors.
    """
    partitions_dict = {}
    for partition in partitions:
        if partition.topic not in partitions_dict:
            partitions_dict[partition.topic] = [partition.partition]
        else:
            partitions_dict[partition.topic].append(partition.partition)
    partitions_summary_str = ', '.join([f'{topic}{parts}' for topic, parts in partitions_dict.items()])
    partitions_complete_str = ', '.join(f'{p.topic}[{p.partition}]:{p.offset} (err:{p.error})' for p in partitions)
    return f'{partitions_summary_str}\n{partitions_complete_str}'


def _on_assign(consumer: Consumer, partitions: list[TopicPartition]) -> None:
    """
    Callback on partition assignment, logs the assigned partitions.
    """
    partitions_str = _partitions_str(partitions)
    logger.info(f"Kafka Subscribe: ASSIGNED partitions for consumer {consumer}: " + partitions_str)


def _on_revoke(consumer: Consumer, partitions: list[TopicPartition]) -> None:
    """
    Callback on partition revocation, logs the revoked partitions.
    """
    partitions_str = _partitions_str(partitions)
    logger.info(f"Kafka Subscribe: REVOKED partitions for consumer {consumer}: " + partitions_str)


def _on_lost(consumer: Consumer, partitions: list[TopicPartition]) -> None:
    """
    Callback on partition loss, logs the lost partitions.
    """
    partitions_str = _partitions_str(partitions)
    logger.info(f"Kafka Subscribe: LOST partitions for consumer {consumer}: " + partitions_str)


class CKStore(RecordStoreWithInitialization):
    """
    Kafka implementation of a record store, using Confluent kafka library
    """

    transactional_producer: Producer
    """ Kafka transactional producer, according to transactional state """
    immediate_producer: Producer
    """ Kafka immediate producer, always produce immediately """
    consumer: Consumer
    """ Kafka consumer, according to transactional state """
    poll_thread: Thread
    """ Thread for polling for messages for both producers"""

    def __init__(
        self,
        serializer: RecordSerializer,
        bootstrap_servers: list[str],
        group_id: Optional[str] = None,
        transactional_id: Optional[str] = None,
        sasl_username: Optional[str] = None,
        sasl_password: Optional[str] = None,
    ) -> None:
        """
        Create a new Kafka record store, the store will be initialized on first use, or with a direct call to initialize().

        :param RecordSerializer serializer: Record serializer (read and write)
        :param list[str] bootstrap_servers: Kafka bootstrap servers (producers and consumer)
        :param str group_id: Kafka group id (consumer), default: service name
        :param str transactional_id: Kafka transactional id for transactional producer, default is generate unique id
        :param Optional[str] sasl_username: Optional username (if SASL PLAIN kafka connection, producer and consumer)
        :param Optional[str] sasl_password: Optional password (if SASL PLAIN kafka connection, producer and consumer)
        """
        # Initialize topics to register
        super().__init__()
        # Kafka config
        self.serializer = serializer
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id or SERVICE_NAME
        self.transactional_id = transactional_id or f'{SERVICE_NAME}-{str(uuid4())}'
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        # Other attributes
        self.initialized = False
        """ Whether the store has been initialized """
        self.in_transaction = False
        """ Whether the store is in a transactional state """
        self.cancelled = False
        """ Whether the store has been cancelled """
        self._initialization_lock = Lock()
        """ Lock for initialization """

    def initialize(self) -> None:
        """
        Initialize the store if not already done.

        The store will stop polling for messages when the thread calling this method stops.
        """
        self._check_initialized()

    def _initialize_consumer_subscription(self):
        consumer_topics = [topic for topic in self.topics]
        logger.info(f"Kafka Subscribe: Initializing consumer subscription for topics {consumer_topics}")
        self.consumer.subscribe(
            consumer_topics,
            on_assign=_on_assign,
            on_revoke=_on_revoke,
            on_lost=_on_lost,
        )
        logger.debug(f"Initialized Kafka consumer.")

    def _initialize_consumer_assignment(self):
        consumer_topics = [topic for topic in self.assignments]
        logger.info(f"Kafka Assign: Initializing consumer assignment for topics {consumer_topics}: {self.assignments}")

        ck_topic_partitions: list[TopicPartition] = []
        ck_cluster_meta: ClusterMetadata = self.consumer.list_topics()

        for topic_name in consumer_topics:
            if topic_name not in ck_cluster_meta.topics:
                logger.warning(f"Topic {topic_name} not found.")
                continue
            else:
                logger.info(f"Topic {topic_name} found.")

            topic_meta: TopicMetadata = ck_cluster_meta.topics[topic_name]
            topic_offsets: Optional[list[int]] = self.assignments[topic_name][1]
            topic_since_date: Optional[datetime] = self.assignments[topic_name][0]

            if topic_offsets and len(topic_meta.partitions) != len(topic_offsets):
                logger.warning(
                    f"Topic {topic_name} has {len(topic_meta.partitions)} partitions, but {len(topic_offsets)} offsets."
                )
                continue

            for partition_id in topic_meta.partitions:
                ck_topic_partition: TopicPartition = TopicPartition(topic_name, partition_id)

                if topic_offsets:
                    ck_topic_partition.offset = topic_offsets[partition_id]
                    logger.info(f"Will assign {topic_name}[{partition_id}]:{ck_topic_partition.offset}")
                else:
                    ck_topic_partition.offset = int(topic_since_date.timestamp() * 1000)
                    ck_topic_partition = self.consumer.offsets_for_times([ck_topic_partition])[0]
                    logger.info(
                        f"Will assign {topic_name}[{partition_id}]:{ck_topic_partition.offset} "
                        f"(from date {topic_since_date})"
                    )
                ck_topic_partitions.append(ck_topic_partition)
            logger.info(f"Assigning {ck_topic_partitions}.")
            self.consumer.assign(ck_topic_partitions)
            logger.info(f"Assigned.")

    def _check_initialized(self) -> None:
        with self._initialization_lock:
            if self.initialized:
                logger.debug("Kafka store already initialized.")
                return

            logger.info(f"Will initialize Kafka producer and consumer.")

            # configs
            transactional_producer_config = {
                'bootstrap.servers': ','.join(self.bootstrap_servers),
                'transactional.id': self.transactional_id,
                'client.id': socket.gethostname(),
            }
            immediate_producer_config = {
                'bootstrap.servers': ','.join(self.bootstrap_servers),
                'client.id': socket.gethostname(),
                'enable.idempotence': 'true',
            }
            consumer_config = {
                'bootstrap.servers': ','.join(self.bootstrap_servers),
                'group.id': self.group_id,
                'client.id': socket.gethostname(),
                'enable.auto.commit': 'false',
                'auto.offset.reset': 'earliest',
                'isolation.level': 'read_committed',
            }

            # SASL authentication
            if self.sasl_username and self.sasl_password:
                for config in [
                    transactional_producer_config,
                    immediate_producer_config,
                    consumer_config,
                ]:
                    config.update(
                        {
                            'sasl_mechanism': 'PLAIN',
                            'sasl_plain_username': self.sasl_username,
                            'sasl_plain_password': self.sasl_password,
                        }
                    )

            # producers
            logger.info(f"Initializing transactional Kafka producer with config {transactional_producer_config}.")
            self.transactional_producer = Producer(transactional_producer_config)
            self.transactional_producer.init_transactions()
            logger.debug(f"Initialized transactional Kafka producer.")

            logger.info(f"Initializing immediate Kafka producer with config {immediate_producer_config}.")
            self.immediate_producer = Producer(immediate_producer_config)
            logger.debug(f"Initialized immediate Kafka producer.")

            # consumer
            logger.info(f"Initializing Kafka consumer with config {consumer_config}.")
            self.consumer = Consumer(consumer_config)
            if self.topics:
                self._initialize_consumer_subscription()
            elif self.assignments:
                self._initialize_consumer_assignment()
            else:
                logger.info(f"No subscription or assignments to initialize consumer with.")
            logger.debug(f"Initialized Kafka consumer.")

            # poll loop
            current_thread = threading.current_thread()

            def poll_loop():
                """
                Kafka requires that producers poll to actually send messages, and trigger callbacks.
                """

                while True:
                    if self.cancelled:
                        # the store was explicitly cancelled
                        finish_reason = "cancelled"
                        break
                    elif not current_thread.is_alive():
                        # the thread which called the initializer is not alive
                        finish_reason = "parent thread not alive"
                        break
                    else:
                        try:
                            immediate_polled = self.immediate_producer.poll(0.005)
                            if immediate_polled:
                                logger.debug(f"Immediate producer polled {immediate_polled} messages.")
                            transactional_polled = self.transactional_producer.poll(0.005)
                            if transactional_polled:
                                logger.debug(f"Transactional producer polled {transactional_polled} messages.")
                        except Exception as e:
                            # Exception could be temporary (e.g. kafka server not available)
                            logger.warning(f"Kafka exception in poll loop: {e}")
                            sleep(30)
                logger.warning(f"Kafka poll loop stopped. Reason: {finish_reason}.")

            self.poll_thread = Thread(
                name=f"CK-Poll-{uuid4().hex[-6:]}",
                target=poll_loop,
            )

            logger.debug(f"Will start Kafka poll loop thread.")
            self.poll_thread.start()

            self.initialized = True
            logger.debug(f"Record Store initialized.")

    def read(
        self,
        max_count: int = 1, timeout_ms: Optional[int] = None, auto_ack: bool = False
    ) -> Iterable[Record]:
        """
        Reads records from kafka, and returns them as a generator.

        :raise MessagingError: if there is an error reading from kafka.

        :param max_count: maximum number of records to fetch
        :param timeout_ms: maximum time to wait for records, in milliseconds
        :param auto_ack: whether to automatically acknowledge the records

        :return: generator of records
        """
        self._check_initialized()

        if not self.topics and not self.assignments:
            logger.debug(f"No topics configured. Returning empty list.")
            return []

        try:
            partitions_str = _partitions_str(self.consumer.assignment())
            logger.debug(f"Reading at most {max_count} records from Kafka. Current assignment is {partitions_str}.")
            messages: list[Message] = self.consumer.consume(max_count, _ms2sec_ck(timeout_ms))
            logger.debug(f"Read {len(messages)} messages from Kafka.")
        except Exception:
            # TODO: temporary errors? (are they always timeout?)
            raise MessagingError(f"Error consuming messages from kafka.")

        for message in messages:
            if message.error():
                logger.error(
                    f"Message {_message_str(message)} has error {message.error()}."
                )
                continue
            logger.debug(f"New message {_message_str(message)}.")
            try:
                # noinspection PyArgumentList
                # PyCharm is wrong, there is no payload arg in .value() method
                encoded = message.value()
                record = self.serializer.decode(encoded)
            except Exception as e:
                raise MessagingError(f"Error decoding message {_message_str(message)}.") from e
            with local_trace(correlation_id=record.correlation_id):
                # TODO: request_id could be Record.uuid, or Record.partition_key, or message offset
                logger.info(
                    f"New record {record.qualified_name} from kafka message {_message_str(message)}."
                )
                yield record
            if auto_ack:
                try:
                    self.consumer.commit(message=message, asynchronous=False)
                except Exception:
                    raise MessagingError(
                        f"Error committing message {_message_str(message)}."
                    )

    def has_reached_end_of_topics(self) -> bool:
        """
        Returns True if all topics have been consumed.
        """
        ck_topic_partitions = self.consumer.assignment()
        for ck_topic_partition in ck_topic_partitions:
            watermark = self.consumer.get_watermark_offsets(ck_topic_partition)
            position = self.consumer.position([ck_topic_partition])[0]
            if not watermark or not position or position.offset < watermark[1]:
                return False
        return True

    def ack(self, timeout_ms=None) -> None:
        """
        Acknowledges the last message read from kafka.

        If in transaction, the offsets are sent to transaction. Otherwise the consumer is committed.
        """
        self._check_initialized()

        if self.in_transaction:
            logger.info(f"Ack read messages in transaction (will send offsets to transaction).")
            try:
                self.transactional_producer.send_offsets_to_transaction(
                    self.consumer.position(self.consumer.assignment()),
                    self.consumer.consumer_group_metadata(),
                    _ms2sec_ck(timeout_ms)
                )
            except Exception:
                raise MessagingError(f"Error sending offsets to transaction.")
        else:
            logger.info(f"Ack read messages outside transaction.")
            try:
                self.consumer.commit(asynchronous=False)
            except Exception as e:
                raise MessagingError(f"Error committing message.") from e

    def _write(self, producer: Producer, record: Record, topic: str, timeout_ms=None) -> None:

        # handle callback
        future_result: Future = Future()

        def ack(err, msg):
            with local_trace(correlation_id=record.correlation_id):
                if err:
                    logger.debug(f"Produced with errors: {err}.")
                    future_result.set_exception(MessagingError(err))
                else:
                    logger.debug(f"Produced successfully.")
                    future_result.set_result(msg)

        # produce message
        logger.debug(f"Will produce record {record.qualified_name} on {topic}.")
        producer.produce(
            topic=topic,
            value=self.serializer.encode(record),
            key=record.partition_key,
            on_delivery=ack
        )

        # wait callback and handle timeout exception
        try:
            future_result.result(timeout=_ms2sec_future(timeout_ms))
        except TimeoutError:
            raise MessagingError(f"Timeout waiting for message to be produced.")
        except Exception as e:
            raise MessagingError(f"Error producing message.") from e

    def write(self, record: Record, topic: str, timeout_ms=None) -> None:
        """
        Write a record to kafka using the transactional producer, according to current transactional state.
        """
        self._check_initialized()

        if self.in_transaction:
            self._write(self.transactional_producer, record, topic, timeout_ms)
        else:
            self._write(self.immediate_producer, record, topic, timeout_ms)

    def write_now(self, record: Record, topic: str, timeout_ms=None) -> None:
        """
        Write a record to kafka using the immediate producer, independently of the eventual current transaction.
        """
        self._check_initialized()

        self._write(self.immediate_producer, record, topic, timeout_ms)

    def start_transaction(self) -> None:
        """
        Enter in a transactional state (read/write).
        """
        self._check_initialized()

        if self.in_transaction:
            raise MessagingError(f"Already in a transaction.")
        self.transactional_producer.begin_transaction()
        self.in_transaction = True

    def commit(self, timeout_ms: Optional[int] = None) -> None:
        """
        Commit the current transaction.
        """
        self._check_initialized()

        if not self.in_transaction:
            raise MessagingError(f"Not in a transaction.")
        self.transactional_producer.commit_transaction(_ms2sec_ck(timeout_ms))
        logger.info(f"Committed transaction.")
        self.in_transaction = False

    def abort(self, timeout_ms: Optional[int] = None) -> None:
        """
        Abort the current transaction.

        Messages written in the transaction will be discarded. Offsets read in the transaction will be discarded.
        """
        self._check_initialized()

        if not self.in_transaction:
            raise MessagingError(f"Not in a transaction.")
        self.transactional_producer.abort_transaction(_ms2sec_ck(timeout_ms))
        logger.info(f"Aborted transaction.")
        self.in_transaction = False

    def __del__(self):
        if self.initialized:
            logger.info(f"Closing consumer.")
            try:
                self.consumer.close()
            except Exception:
                logger.warning(f"Error closing consumer.")
            logger.info(f"Waiting poll thread to join.")
            self.cancelled = True
            try:
                self.poll_thread.join()
            except Exception as e:
                logger.warning(f"Error joining poll thread: {e}.")


def _ms2sec_ck(timeout_ms: Optional[int]) -> float:
    """
    Convert milliseconds (integer) to seconds (float) for Confluent Kafka API.

    :param timeout_ms: timeout in milliseconds, None for no timeout
    :return: timeout in seconds, -1 for no timeout
    >>> _ms2sec_ck(None)
    -1.0
    >>> _ms2sec_ck(0)
    0.0
    >>> _ms2sec_ck(500)
    0.5
    """
    timeout_sec = -1.0
    if timeout_ms is not None:
        timeout_sec = timeout_ms / 1000
    return timeout_sec


def _ms2sec_future(timeout_ms: Optional[int]) -> Optional[float]:
    """
    Convert milliseconds (integer) to seconds (float) for the Future API.

    :param timeout_ms: timeout in milliseconds, None for no timeout
    :return: timeout in seconds, None for no timeout
    >>> _ms2sec_future(None)
    >>> _ms2sec_future(0)
    0.0
    >>> _ms2sec_future(500)
    0.5
    """
    timeout_sec = None
    if timeout_ms is not None:
        timeout_sec = timeout_ms / 1000
    return timeout_sec
