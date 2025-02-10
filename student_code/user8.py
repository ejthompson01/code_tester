# has incorrect syntax in q4

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

def q4(