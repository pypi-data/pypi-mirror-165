"""
The test event store and run loop
"""
import copy
import multiprocessing
from multiprocessing import connection
from typing import Dict, List, Union
import logging

from .expectation import Expectation
from .constants import NO_MATCHING_EVENT_FOUND, EVENT_ID_KEY, EVENT_STATE_KEY
from .messages import *


class _FullEventStore:
    """This is somewhat a mirror of the event store but instead of events being removed they are
    marked as expected or deleted
    """

    ACTIVE = "Active"
    EXPECTED = "Expected"
    DELETED = "Deleted"

    def __init__(self):
        self._store = []

    def reset(self):
        self._store = []

    def get_all(self):
        return self._store

    def add_event(self, event):
        event_copy = copy.deepcopy(event)

        event_copy[EVENT_STATE_KEY] = self.ACTIVE
        self._store.append(event_copy)

    def mark_event_as_expected(self, event_id: int):
        for event in self._store:
            if event[EVENT_ID_KEY] == event_id:
                event[EVENT_STATE_KEY] = self.EXPECTED
                return

    def mark_event_as_deleted(self, event_id: int):
        for event in self._store:
            if event[EVENT_ID_KEY] == event_id:
                event[EVENT_STATE_KEY] = self.DELETED
                return


class _TestEventStore:
    def __init__(self):
        self._store = []
        self._event_id = 0
        self._full_store = _FullEventStore()

    def _test_if_event_matches_expectations(
        self, event: Dict, expectations: List[Expectation]
    ) -> bool:
        for expectation in expectations:
            if expectation.event_field_name not in event:
                return False

            event_value = event[expectation.event_field_name]
            if not expectation.comparison_function(event_value, expectation.comparison_value):
                return False

        return True

    def reset(self):
        """Reset the event store"""
        logging.info("Reset Event Store Called")

        if len(self._store) > 0:
            logging.warning(
                "There were {} events in the store when it was reset".format(len(self._store))
            )

        self._store = []
        self._event_id = 0
        self._full_store.reset()

    def get_all(self) -> List[Dict]:
        """Get all events from the store

        :return: A list of events
        """
        logging.debug(f"Event store get_all called, store: {self._store}")
        return self._store

    def get_full_event_log(self) -> List[Dict]:
        """Get all events from the store, including those that have been deleted or expected

        :return: A list of events
        """
        logging.debug(f"Event store get_full_event_log called, store: {self._full_store.get_all()}")
        return self._full_store.get_all()

    def get_all_matching(self, expectations: List[Expectation]) -> List[Dict]:
        """Get all events matching the given criteria

        :param expectations: A list of expectations
        :return: A matching event or None
        """
        matching_events = []

        for event in self._store:
            match = self._test_if_event_matches_expectations(event, expectations)

            if match:
                matching_events.append(event)

        return matching_events

    def add(self, test_event: Dict) -> int:
        """Add an event to the test store

        :param test_event: The event to add
        :return: The event id
        """
        test_event[EVENT_ID_KEY] = self._event_id
        self._event_id += 1
        self._store.append(test_event)

        logging.debug(
            f"Event store add called, event: {test_event},"
            f" there are now {len(self._store)} events in the store"
        )

        self._full_store.add_event(test_event)

        return test_event[EVENT_ID_KEY]

    def remove_expected_event(self, test_event: Dict):
        """Remove an event from the event store that has been expected and found

        :param test_event: The event to remove
        :return: None
        """
        i = -1
        for i, event in enumerate(self._store):
            if event == test_event:
                break
        else:
            return

        if i >= 0:
            del self._store[i]
            self._full_store.mark_event_as_expected(test_event["event_id"])

    def remove_matching_events(self, expectations: List[Expectation]) -> int:
        """Remove all events matching the passed in expectations

        :param expectations: The list of expectations to match against
        :return: the number of events removed
        """
        to_del = []
        for i, event in enumerate(self._store):
            match = self._test_if_event_matches_expectations(event, expectations)

            if match:
                to_del.append((i, event))

        num_events_removed = len(to_del)

        for index, event in reversed(to_del):
            del self._store[index]
            self._full_store.mark_event_as_deleted(event["event_id"])

        logging.debug(f"{num_events_removed} events removed from the store")
        return num_events_removed

    def find_first_match(self, expectations: List[Expectation]) -> Union[str, Dict]:
        """Find the first event that matches the passed in expectations

        :param expectations: A list of expectations
        :return: A matching event or None
        """
        for event in self._store:
            match = self._test_if_event_matches_expectations(event, expectations)

            if match:
                return event

        return NO_MATCHING_EVENT_FOUND


def event_store_run_loop(queue: multiprocessing.Queue, result_pipe: connection.Connection):
    """The event store process run loop

    :param queue: A multiprocessing queue which requests to perform actions are read from
    :param result_pipe: A multiprocessing pipe which found events or lists of events are placed on
                        following a get or expect request
    :return: None
    """
    event_store = _TestEventStore()
    running = True

    logging.info("Starting up test event store")

    # Note the result_pipe should only be accessed by the library code, not the web server
    # so there is no point doing things like writing to the result pipe on an add event
    try:
        while running:
            # message is assumed to be one of the messages defined in messages.py
            message = queue.get()

            message_type = message.message_type

            if message_type == ShutdownMessage.TYPE:
                logging.info("Shutting down test event store")
                running = False

            elif message_type == ResetMessage.TYPE:
                event_store.reset()
                result_pipe.send("Event Store Reset")

            elif message_type == GetAllEventsMessage.TYPE:
                result_pipe.send(event_store.get_all())

            elif message_type == GetFullEventLogMessage.TYPE:
                result_pipe.send(event_store.get_full_event_log())

            elif message_type == GetEventMessage.TYPE:
                expectations = message.expectations
                result = event_store.find_first_match(expectations)
                result_pipe.send(result)

            elif message_type == GetAllMatchingEventsMessage.TYPE:
                expectations = message.expectations
                result_pipe.send(event_store.get_all_matching(expectations))

            elif message_type == AddEventMessage.TYPE:
                test_event = message.event_fields
                event_store.add(test_event)

            elif message_type == ExpectEventMessage.TYPE:
                expectations = message.expectations
                result = event_store.find_first_match(expectations)
                result_pipe.send(result)

            elif message_type == RemoveExpectedEventMessage.TYPE:
                del_event = message.event
                event_store.remove_expected_event(del_event)

            elif message_type == DeleteMatchingEventsMessage.TYPE:
                expectations = message.expectations
                events_removed = event_store.remove_matching_events(expectations)
                result_pipe.send(events_removed)
            else:
                logging.error(f"Event Store - Unhandled message: {message_type}")
    except Exception as exc:
        logging.error(f"An unhandled exception has occurred in the event store: {exc}")
    result_pipe.close()
