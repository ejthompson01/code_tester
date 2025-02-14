# Code for timeouts adapted from:
# https://stackoverflow.com/questions/492519/timeout-on-a-function-call

from typing import Callable
import threading
import _thread as thread
from datetime import datetime as dt

class StudentFunction:
    '''
    Class to run and store info about an individual function.

    As this is still in development, please inspect the variables
    defined in __slots__ as well as the README.md for more information.
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
                 args: tuple = None,
                 kwargs: dict = None,
                 timeout_secs: float = None
                 ):
        self.fun = fun
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.timeout_secs = timeout_secs
        return
    
    def run_fun(self) -> None:
        '''
        Runs the function this class wraps.

        As this is still in development, please inspect the variables
        defined in __slots__ as well as the README.md for more information.
        '''
        def interrupt() -> None:
            '''
            Sends a KeyboardInterrupt to the main thread and sets self.interrupted to True.
            Even if the interrupt is not recognized, the self.interrupted property seems to be
            reliably set to True. More test cases welcome!
            '''
            self.interrupted = True
            print(f'Interrupt sent when {self.fun.__name__} ran more than {self.timeout_secs} secs.', flush=True)
            thread.interrupt_main()
            return
        
        # The function has not yet been interrupted nor exited cleanly
        self.interrupted = False
        self.clean_exit = False

        # If a timeout was provided, starts a timer after which
        # the interupt() function will be called.
        if self.timeout_secs:
            timer = threading.Timer(self.timeout_secs, interrupt)
            timer.start()
        try:
            # Record the start time
            self.start_time = dt.now()
            
            # Run the function
            self.result = self.fun(*self.args, **self.kwargs)
            
            # This flag is meant to indicate that the function
            # exited cleanly. In some cases interrupt() might be called
            # but this flag will be set to True anyway. 
            # We check again in the finally block.
            self.clean_exit = True
        
        # The intention is that if the code timed out, a KeyboardInterrupt
        # was sent. It is non-trivial to ensure that this interrupt will
        # always be sent/caught as expected, so be careful!
        except KeyboardInterrupt:
            self.result = f'Error: Timed out after {self.timeout_secs} secs.'

        # If any other error occurred in the user code, assign it to self.result
        except Exception as e:
            self.result = f'Error: {e}'

        # Clean up
        finally:
            # If the self.interrupted flag was set,
            # then make sure self.clean_exit is False.
            if self.interrupted:
                self.clean_exit = False
            
            # Record the stop time and record the total runtime.
            self.stop_time = dt.now()
            self.runtime = (self.stop_time - self.start_time)

            # Cancel the pending interrupt if a timeout was provided.
            if self.timeout_secs:
                timer.cancel()
        return
