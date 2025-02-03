
from typing import Callable
from types import ModuleType
import inspect

from src.student import StudentFunction

# WEIRD GLOBAL BADNESS [_]!!!
import key

class Professor:
    DFLT_TIMEOUT_MULT = 2
    
    #__slots__ = ()
    
    def __init__(self):
        self.results: dict[str, StudentFunction] = {}
        self.timeouts: dict[str, float] = {}

        for qid, q in key.questions.items():
            self.results[qid] = StudentFunction(q.fun, None, q.args, q.kwargs)
            self.results[qid].run_fun()
            
            # HELD FIXED FOR TESTING [_]
            self.timeouts[qid] = 5
        return
    
    # Do we need getters? Information flow should be Prof -> Student
    def get_args(self, qid: str) -> tuple:
        return self.results[qid].args
    
    def get_kwargs(self, qid: str) -> dict:
        return self.results[qid].kwargs