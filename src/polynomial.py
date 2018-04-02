# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 20:26:51 2018

@author: Alex
"""
import math

class polynomial():
    
    precisionDigits=9
    precision=0.1**precisionDigits
    
    def __init__(self,coef=[0]):
        self.degree=len(coef)-1
        self.coef=coef
        self.findDegree()
        
    def iszero(self):
        for i in range(self.degree+1):
            if abs(self.coef[i])>=self.precision:
                return False
        return True 
    
    def findDegree(self):
        d=len(self.coef)-1
        while d>0 and abs(self.coef[d])<self.precision:
            d-=1
        self.coef=self.coef[0:d+1]
        self.degree=d   
        
    def add(self,v):
        degree=max(v.degree,self.degree)
        coef=[0]*(degree+1)
        for i in range(v.degree+1):
            coef[i]+=v.coef[i]
        for i in range(self.degree+1):
            coef[i]+=self.coef[i]
        return polynomial(coef)

    def sub(self,v):
        return self.add(v.umin())
    
    def mul(self,v):
        coef=[0]*(v.degree+self.degree+1)
        for i in range(v.degree+1):
            for j in range(self.degree+1):
                coef[i+j]+=v.coef[i]*self.coef[j]
        return polynomial(coef)
        
    def div(self,d):    
        if d.iszero():
            raise Exception('Division by 0')    
        q=polynomial()
        r=self    
        while not r.iszero() and r.degree>=d.degree :
            coef=[0]*(r.degree-d.degree+1)
            coef[-1]=r.coef[r.degree]/d.coef[d.degree]
            t=polynomial(coef)
            q=q.add(t)
            r=r.sub(t.mul(d))
        if not r.iszero():
            raise Exception('Non-zero reminder while dividing polynomials')
        return q
    
    # unary minus
    def umin(self):
        coef=[0]*(self.degree+1)
        for i in range(self.degree+1):
            coef[i]=-self.coef[i]
        return polynomial(coef)
   
    def log(self):
        if self.degree>0:
            raise Exception('Can not take log from a polynomial')
        if self.coef[0]<=0:
            raise Exception('Log from a non-positive argument')
        coef=math.log(self.coef[0])
        return polynomial([coef])
       
    def solve(self):
        if self.degree>1:
            if self.coef[0]==0:
                return('0')
            return ('Not found (not able to solve non-linear equations)')
        
        if (self.degree==0 and self.coef[0]==0):
            return 'Any (any value is a valid solution)'
        if self.degree==0 and self.coef[0]!=0:
            return 'None (no solution exists)'
               
        return str(polynomial([-self.coef[0]/self.coef[1]]) )      
    
    # convert into a string like "3x^2-3x+1"
    def string(self):
        s=''
        sign=''   
        if self.degree>=0:
            for i in range(self.degree+1):
                c=round(self.coef[i],self.precisionDigits)
                if c==int(c):
                    c=int(c)
                if c!=0 or self.degree==0:
                    s=sign+s
                    
                    if i==1:
                        s='x'+s
                    elif i>1: 
                        s='x^'+str(i)+s    
                    
                    a=abs(c)
                    if i==0 or a!=1: 
                        s=str(a)+s
    
                    
                    if c<0:
                        sign='-'
                    else: 
                        sign='+'
                
            if sign=='-':
                s='-'+s
        if s=='': #all coefficients are very small, so s is empty
            s='0'
        return s

    def __str__(self):
        return self.string()    
    
    def __repr__(self):
        return self.string()    
    
    def __eq__(self,other):
        
        if self.degree!=other.degree:
            return False
        else:
            i=0
            while i<=self.degree:
                if abs(self.coef[i]-other.coef[i])>self.precision: 
                    return False
                i=i+1
            return True
        
        