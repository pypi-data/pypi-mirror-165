
from queue import Queue
from threading import Thread
from typing import Callable, Any, Type, Optional

def _cls_name(obj: Type[object]) -> str:
    return obj.__class__.__name__

class MessageThread:
    """Runs a thread with queue of messages"""
    def print(self, *args, **kwargs):
        """Print function used for printing out, is standard python print() by default"""
        if not self.__msg_handler.is_alive():
            raise RuntimeError(f"'{_cls_name(self)}' messaging thread is not alive")
        self.__msg_queue.put((args, kwargs)) 

    def __init__(self, print_func: Optional[Callable[..., Any]] = None) -> None:
        self.__msg_queue = Queue()
        self.__print = print_func if print_func is not None else print
        self.__msg_handler = Thread(target=self.__msg_ouput, daemon=True)
        self.__msg_handler.start()
        

    def __msg_ouput(self):
        while True:
            args, kwargs = self.__msg_queue.get()
            self.__print(*args, **kwargs)
            self.__msg_queue.task_done()

    def join(self):
        """Wait for all messages to print out"""
        self.__msg_queue.join()
