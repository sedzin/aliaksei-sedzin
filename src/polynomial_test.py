# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 20:52:48 2018

@author: Alex
"""
from polynomial import polynomial


P1=polynomial([10])
print('Polynomial P1:',P1)

P3=P1.log()
print('Log(P1)      :',P3)


P1=polynomial([1,1])
P2=polynomial([1,1])
print('Polynomial P1:',P1)
print('Polynomial P2:',P2)

P3=P1.add(P2)
print('P1+P2        :',P3)

P3=P1.mul(P2)
print('P1*P2        :',P3)

P3=P1.div(P2)
print('P1/P2        :',P3)

P3=P1.umin()
print('-P1          :',P3)

P3=P2.solve()
print('Solution of P2=0 :',P3)

