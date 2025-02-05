# q1 adds 2 instead of 1, so incorrect output

def q1(n: int) -> int:
    return n+2

def q2(n: int, m: int) -> int:
    return n**2 - m

def q3() -> int:
    return 42

def q4(n: int) -> tuple[int, str]:
    return n+1, f'n^2 is {n**2}'