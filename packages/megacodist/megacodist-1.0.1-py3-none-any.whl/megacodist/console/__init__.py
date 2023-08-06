"""This module exposes some useful APIs to work with and extend traditional
console programming.
"""

from threading import Thread, Event
from time import sleep


class WaitPromptingThrd(Thread):
    """Instances of this class wrtie a waiting message while an operation
    is performing in another thread. As long as an instance of this class
    is alive, avoid wrtiting to the console. Typically you have to create
    an instance passing the 'event' argument at least, call 'start' method,
    and set the event when waiting is no longer needed then call 'join'
    method, meanwhile this object writes a waiting message to the console.
    """
    def __init__(
            self,
            event: Event,
            *,
            n: int = 3,
            waitMsg: str = 'Waiting',
            endMsg: str = '',
            daemon: bool | None = None) -> None:
        """Initializes an instance of this class.

        'event', of type threading.Event, specifies when to quit this thread.
        'n' specifies number of dots in waiting message.
        'waitMsg' specifies the message while waiting, defaults to
        'Waiting'. 'endMsg' specifies the message when event is set.
        """
        super().__init__(name='WaitMsgThrd', daemon=daemon)
        self._n = n
        """Specifies number of dots in waiting message."""
        self._waitMsg = waitMsg
        """Specifies the message while waiting."""
        self._endMsg = endMsg
        """Specifies the message when event is set."""
        self._event = event
        """Specifies when to quit this thread."""
    
    def run(self) -> None:
        maxMsgLen = len(self._waitMsg) + self._n
        while True:
            print(end='\r', flush=True)
            print(' ' * maxMsgLen, end='\r', flush=True)
            print(self._waitMsg, end='', flush=True)
            sleep(0.5)
            if self._event.is_set():
                break
            for idx in range(self._n):
                print('.', end='', flush=True)
                sleep(0.5)
                if self._event.is_set():
                    break
            else:
                continue
            break
        print(end='\r', flush=True)
        print(' ' * maxMsgLen, end='\r', flush=True)
        print(self._endMsg, end='', flush=True)
