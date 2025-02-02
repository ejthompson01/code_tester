# Code for timeouts adapted from:
# https://stackoverflow.com/questions/492519/timeout-on-a-function-call

from typing import Callable

import sys
import threading
import _thread as thread

from datetime import datetime as dt

class StudentFunction:
    '''
    Class to run and report on an individual function
    '''
    __slots__ = (
        'fun',
        'timeout_secs',
        'args',
        'kwargs',
        'result',
        'start_time',
        'stop_time',
        'runtime',
        'clean_exit'
    )
    def __init__(self,
                 fun: Callable,
                 timeout_secs: float = None,
                 args: tuple = None,
                 kwargs: dict = None
                 ):
        self.fun = fun
        self.timeout_secs = timeout_secs
        self.args = args or ()
        self.kwargs = kwargs or {}
        return
    
    def run_fun(self) -> None:
        '''
        Run the function and record details (see __slots__ for now)
        '''
        def interrupt() -> None:
            '''
            Sends a KeyboardInterrupt to the main thread.
            Not guaranteed to work on all systems or in all cases!
            '''
            print(f'Interrupt sent when {self.fun.__name__} ran more than {self.timeout_secs} secs.', flush=True)
            thread.interrupt_main()
            return
        
        self.clean_exit = False
        if self.timeout_secs:
            timer = threading.Timer(self.timeout_secs, interrupt)
            timer.start()
        try:
            self.start_time = dt.now()
            self.result = self.fun(*self.args, **self.kwargs)
            self.clean_exit = True
        except KeyboardInterrupt:
            self.result = f'Error: Timed out after {self.timeout_secs} secs.'
        except Exception as e:
            self.result = f'Error: {e}'
        finally:
            self.stop_time = dt.now()
            self.runtime = (self.stop_time - self.start_time)
            if self.timeout_secs:
                timer.cancel()
        return