from numpy import random
from itertools import combinations
import time
from typing import Any,Callable

def decorator(f:Callable[...,Any]):
    '''print time elapsed during <function f>'''
    def g(*args,**kwargs):
        t = time.perf_counter()
        r = f(*args,**kwargs)
        print(f'<function {f.__name__}>: time elapsed = {time.perf_counter()-t:.6f}s')
        return r
    return g

# estimate P(x>y) ∀ x~gauss(a,s),y~gauss(b,s); NOTE x-y ~ gauss(a-b,sqrt(2)*s) -> P(x>y) = (1+erf(z/sqrt(2)))/2 ~= 1/(1+np.e**(np.pi/np.sqrt(6)*z))
eval = lambda z=float: 1/(1+3.6**z)

class Population:
    def __init__(s,id:int=0, n:int=1000, mean:float=0.0, stdv:float=1.0, mean_:float=1500, stdv_:float=200, C:list[object]=[]):
        s.id = id
        s.mean = mean
        s.stdv = stdv
        s.mean_ = mean_
        s.stdv_ = stdv_
        s.k = stdv_/6
        if C:
            s.C = C
            s.n = len(C)
        else:
            s.C = [Creature(i,random.normal(mean,stdv),mean_) for i in range(n)]
            s.n = n
        
    def fullid(s) -> str:
        return f'{s.__class__.__name__}{s.id}'
    
    def __str__(s) -> str:
        if s.n < 10: return f'<class {s.fullid()}> n = {s.n}\n\t' + '\n\t'.join([str(c) for c in s.C])
        else: return f'<class {s.fullid()}> n={s.n}\n\t'+'\n\t'.join([str(s.C[i]) for i in (0,1,2,s.n//2-1,s.n//2,s.n//2+1,-3,-2,-1)])+f'\n\t...({s.n-9} more)'

    def __repr__(s) -> str:
        return f'{s.__class__.__name__}(id={s.id},stdv={s.stdv},stdv_={s.stdv_},C=['+', '.join([repr(c) for c in s.C])+'])'

    def addcreature(s,*C:object):
        s.C.extend(C)
        s.n = len(s.C)

    def play(s,a:object,b:object):
        d = (eval((b.x-a.x)/s.stdv) > random.random()) - eval((b.x_-a.x_)/s.stdv_)
        a.x_ += s.k*d
        b.x_ -= s.k*d

    @decorator
    def rrt(s, m:int=10):
        '''run round-robin-tournament <int m> times; each round, all players compete every other player once'''
        for _ in range(m):
            for a, b in combinations(s.C, 2): s.play(a, b)
    
    def rank(s, f = lambda c: c.x_):
        '''sort <list[object] s.C>; default by c.x_ ∀ <object c> ∈ s.C in increasing order'''
        s.C.sort(key = f)



class Creature:
    def __init__(s,id:int, x:float, x_:float):
        s.id = id
        s.x = x
        s.x_ = x_

    def fullid(s) -> str:
        return f'{s.__class__.__name__}{s.id}'
    
    def __str__(s) -> str:
        return f'<class {s.fullid()}> (x,x_) = ({s.x},{s.x_})'
    
    def __repr__(s) -> str:
        return f'{s.__class__.__name__}(id={s.id},x={s.x},x_={s.x_})'



if __name__ == '__main__':
    P = Population()
    P.addcreature(Creature(100,4.0,1200),Creature(101,-4.0,1200))
    P.rrt()
    P.rank()
    print(P)
