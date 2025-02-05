# Everything correct

def q1(n: int) -> int:
    return n+1

def q2(n: int, m: int) -> int:
    return n**2 - m

def q3() -> int:
    '''
    '''
    x=1
    try:
        while True:
            x+=1
    except Exception as e:
        x = 'I caught an exception! Cough, cough.'
        print(x)
    return x

def q4(n: int) -> tuple[int, str]:
    return n+1, f'n^2 is {n**2}'