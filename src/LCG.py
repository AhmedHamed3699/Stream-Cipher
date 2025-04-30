
class LCG:
    def __init__(self, seed=42, a=7, c=0, m=127):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state
    
    def n_next(self, n):
        return [self.next() for _ in range(n)]