"""Encoding process."""
# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC


class EncodingDoneObservable:

    """Encoding done observable."""

    def __init__(self):
        self._observers = set()

    def notify_observers(self):
        """Notify observers to finish."""
        for observer in self._observers:
            observer.finish()

    def register_observer(self, observer):
        """Register observer."""
        if isinstance(observer, EncodingDoneObserver):
            self._observers.add(observer)
        else:
            raise TypeError('Not ProcessDoneObserver type')


class EncodingDoneObserver(ABC):

    """Encoding Done Observer interface."""

    @abstractmethod
    def finish(self):
        """This method shall be implemented."""
