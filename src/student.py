# Code for timeouts adapted from:
# https://stackoverflow.com/questions/492519/timeout-on-a-function-call

from typing import Callable
from types import ModuleType
import inspect

import threading
import _thread as thread

from datetime import datetime as dt

class StudentFunction:
    '''
    Class to run and store info about an individual function.
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
        'clean_exit',
        'interrupted'
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
            Sends a KeyboardInterrupt to the main thread and sets self.interrupted to True.
            Not guaranteed to work on all systems or in all cases!
            '''
            self.interrupted = True
            print(f'Interrupt sent when {self.fun.__name__} ran more than {self.timeout_secs} secs.', flush=True)
            thread.interrupt_main()
            return
        
        # Function has not yet been interrupted nor exited cleanly
        self.interrupted = False
        self.clean_exit = False

        # Start the timer if requested
        if self.timeout_secs:
            timer = threading.Timer(self.timeout_secs, interrupt)
            timer.start()
        try:
            # Record the start time and run the function
            self.start_time = dt.now()
            self.result = self.fun(*self.args, **self.kwargs)
            
            # Function exited cleanly (perhaps! If it caught and ignored an interrupt it did not)
            self.clean_exit = True
        except KeyboardInterrupt:
            self.result = f'Error: Timed out after {self.timeout_secs} secs.'
        except Exception as e:
            self.result = f'Error: {e}'
        finally:
            # [_] TEMP flag for silenced interrupts
            if self.interrupted:
                self.clean_exit = float('nan')

            # Record the stop and runtimes
            self.stop_time = dt.now()
            self.runtime = (self.stop_time - self.start_time)
            # Cancel the pending interrupt
            if self.timeout_secs:
                timer.cancel()
        return
