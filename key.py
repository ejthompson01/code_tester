from typing import Callable

questions = {}

class Question:
    def __init__(self,
                 fun: Callable,
                 args: tuple = None,
                 kwargs: dict = None
                 ):
        self.fun = fun
        self.args = args or ()
        self.kwargs = kwargs or {}
        return

def q1(n: int) -> int:
    '''
    Add one.
    '''
    return n+1
questions['q1'] = \
    Question(q1,
             kwargs={'n': 2}
             )

def q2(n: int, m: int) -> int:
    '''
    Square n and subtract m
    '''
    return n**2 - m
questions['q2'] = \
    Question(q2,
             args=(3, 4)
             )

def q3() -> 42:
    'Return 42'
    return 42
questions['q3'] = \
    Question(q3)
