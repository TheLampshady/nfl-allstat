"""Reusable Observer/PubSub pattern classes.
"""
import logging


class Event(object):
    pass


class Observable(object):
    """Implementation of the observable design pattern to measure progress"""
    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        """Add an observer to keep track of progress"""
        self.observers.append(observer)

    def publish(self, **attrs):
        """Add an publish event to keep track of progress"""
        e = Event()
        e.source = self
        for k, v in attrs.iteritems():
            setattr(e, k, v)
        for fn in self.observers:
            fn.observeEvent(e)


class Observer(object):
    def observeEvent(self, event):
        """To be overridden as needed by subclass."""
        logging.debug('Observed event: %s', event)