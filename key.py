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

# Question 1: Write a function that takes an integer as input and returns its successor
def q1(n: int) -> int:
    '''
    Add one.
    '''
    return n+1
questions['q1'] = \
    Question(q1,
             kwargs={'n': 2}
             )

# Question 2: Write a function that takes integers n,m as input and returns n^2-m
def q2(n: int, m: int) -> int:
    '''
    Square n and subtract m
    '''
    return n**2 - m
questions['q2'] = \
    Question(q2,
             args=(3, 4)
             )

# Question 3: Write a function that returns the ultimate answer to the ultimate question.
def q3() -> 42:
    '''
    Return 42
    '''
    return 42
questions['q3'] = \
    Question(q3)

# Question 4: Return multiple outputs as a tuple
def q4(n: int) -> tuple[int, str]:
    return n+1, f'n^2 is {n**2}'
questions['q4'] = \
    Question(q4,
             args=(42,)
            )
