# Everything correct

def q1(n: int) -> int:
    return n+1

def q2(n: int, m: int) -> int:
    return n**2 - m

def q3() -> int:
    '''
    '''
    x=1
    while True:
        x+=1
    return x

def q4(n: int) -> tuple[int, str]:
    return n+1, f'n^2 is {n**2}'