# q4 runs a time.sleep() which might not respond to the interrupt it will be sent

def q1(n: int) -> int:
    return n+1

def q2(n: int, m: int) -> int:
    return n**2 - m

def q3() -> 42:
    return 42

def q4(n):
    import time
    time.sleep(2)
    return