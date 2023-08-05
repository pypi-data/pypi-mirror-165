# -*- coding: utf-8 -*-
from threading import Thread, Event
import _thread

TIMEOUT_MAX = _thread.TIMEOUT_MAX
TIMEOUT_MIN = 1


class BlockingRunner:
    _event = None
    _queue = None

    def start(self, queue, *args, **kwargs):
        self._queue = queue
        if self._event is None or self._event.is_set():
            self._event = Event()
        self._main_loop()

    def shutdown(self, *args, **kwargs):
        self._event.set()

    def _main_loop(self):
        wait_seconds = TIMEOUT_MAX
        while True:
            self._event.wait(wait_seconds)
            self._event.clear()
            wait_seconds = self._queue._process()  # noqa

    def wakeup(self):
        self._event.set()


class BackgroundRunner(BlockingRunner):
    def start(self, queue, *args, **kwargs):
        self._queue = queue
        if self._event is None or self._event.is_set():
            self._event = Event()

        self._thread = Thread(target=self._main_loop, name='delay_queue')
        self._thread.start()

    def shutdown(self, *args, **kwargs):
        super(BackgroundRunner, self).shutdown(*args, **kwargs)
        self._thread.join()
        del self._thread
