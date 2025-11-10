import numpy as np
from numpy import random
import json



# estimate P(x>y) ∀ x~gauss(a,s),y~gauss(b,s); NOTE x-y ~ gauss(a-b,sqrt(2)*s) -> P(x>y) = (1+erf(z/sqrt(2)))/2 ~= 1/(1+e^(-kz))
eval = lambda a=float,b=float,s=float: 1/(1+np.e**(np.pi/np.sqrt(6)*(b-a)/s))



class Population:
    def __init__(s,id:int=0, n:int=100, mean:float=0.0, stdv:float=1.0, mean_:float=1200, stdv_:float=200, C:list[object]=[]):
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
        if s.n < 7: return f'<class {s.fullid()}> n = {s.n}\n\t' + '\n\t'.join([str(c) for c in s.C])
        else: return f'<class {s.fullid()}> n = {s.n}\n\t' + '\n\t'.join([str(s.C[i]) for i in range(6)]) + f'\n\t... ({s.n-6} more)'

    def __repr__(s) -> str:
        return f'{s.__class__.__name__}(id={s.id},stdv={s.stdv},stdv_={s.stdv_},C=['+', '.join([repr(c) for c in s.C])+'])'

    def addcreature(s,*C:object):
        for c in C:
            s.C.append(c)
            s.n += 1

    def play(s,a:object,b:object):
        e = eval(a.x_,b.x_,s.stdv_) # expected value P(x_>y_) ∀ x_~gauss(a,s), y_~gauss(b,s)
        t = random.random() < eval(a.x,b.x,s.stdv) # actual value proportioned by P(x>y) ∀ x~gauss(a,s), y~gauss(b,s)
        a.x_ += s.k*(t-e)
        b.x_ -= s.k*(t-e)

    def rrt(s, m:int=10):
        '''run round-robin-tournament <int m> times; each round, all players compete every other player once'''
        for _ in range(m):
            for i in range(s.n):
                for j in range(i): s.play(s.C[i],s.C[j])
    
    def rank(s, f = lambda c: c.x_):
        '''sort creatures; default smallest to largest'''
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
    for c in P.C: print(c)