from queue import Queue
from threading import Thread, Event, Lock
from functools import wraps
from typing import List

class _RepeaterResult:

    def __init__(self, func, timer, get_nones, get_false, *args, **kwargs):
        self._func = func
        self._timer = timer
        self._get_nones = get_nones
        self._get_false = get_false
        self._queue = Queue()
        self._thread = Thread(target=self.__run, daemon=True, args=args, kwargs=kwargs)
        self._wait = Event().wait
        self._lock = Lock()
        self._running = True
        self._thread.start()

    def __run(self, *args, **kwargs):
        while self._running:
            result = self._func(*args, **kwargs)
            put_nones = bool((result is not None) or self._get_nones)
            put_non_nones = bool(result or self._get_false)
            if put_nones and put_non_nones:
                self._queue.put(result)
            self._wait(self._timer)

    def get(self) -> List:
        """Get accumulated results from queue"""
        res = []
        self._lock.acquire()
        while not self._queue.empty():
            res.append(self._queue.get())
            self._queue.task_done()
        self._lock.release()
        return res

    def stop(self):
        """Stop timer"""
        self._running = False
        self._thread.join()


def repeat_timer(timer, get_nones=False, get_false=True):
    """Launches a thread that will execute a function each 'timer' sec, 
    to get accumulated results call 'get' method, to stop timer call 'stop' method 
    of returned value

    Args:
        timer: float, delay between calls
        get_nones: bool, put 'None' values in result
        get_false: bool, put bool() == False values in result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return _RepeaterResult(func, timer, get_nones, get_false, *args, **kwargs)
    
        return wrapper
    return decorator