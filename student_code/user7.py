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
        try:
            x+=1
        except Exception as e:
            x = 'I got canceled.'
            print(x)
    return x

def q4(n: int) -> tuple[int, str]:
    return n+1, f'n^2 is {n**2}'