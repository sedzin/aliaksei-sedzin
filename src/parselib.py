# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 15:17:19 2018

@author: Alex
"""


from polynomial import polynomial
from error import Error

class Parser:
    def __init__(self,string):
        
        self.allowedVariables='xyabcd'
        self.spaceCharacters=' \t'
        self.string = string
        
       
        self.i = 0
        self.variable = ''
        self.isEquation = False
        
    def getCurrent(self)    :
        return self.string[self.i:self.i+1] or '#'
        
    def getPrevious(self):
        return self.string[self.i-1:self.i] or '#'
        
    def hasCurrent(self):
        return self.i<len(self.string)
    
    def advance(self):
        self.i=self.i+1
     
    def skipSpaces(self):
        while self.getCurrent() in self.spaceCharacters:
            self.advance()
        return
    
    def checkInput(self):
        # sanity check input string
        for j in range(len(self.string)):
            if self.string[j] not in '1234567890.-+*/()log='+self.allowedVariables+self.spaceCharacters:
                raise Error('Unrecognised character "'+self.string[j]+'"',j)
        
    def evaluate(self):
        self.checkInput()
        result=self.parseEquation()
        if self.hasCurrent():
            raise Error('Unexpected expression',self.i)
            
        if self.isEquation:
            solution=result.solve()
            if self.variable !='': # variables found; try to solve
                return self.variable+'='+str(solution)
            else: # no variables; check if the equation is an identity
                if str(result)=='0':
                    return 'True'
                else:
                    return 'False'
            
        else: # we deal with an expression
            output=str(result)
            output=output.replace('x',self.variable)
            return output
            
    def parseEquation(self):
        result = self.parseExpression()
        while True:
            self.skipSpaces()
            if self.getCurrent()=='=':
                if self.isEquation==True:
                    raise Error('An extra = sign found',self.i)
                self.isEquation=True
                self.advance()
                result=result.sub(self.parseExpression())
            else:
                break
        
        #if self.isEquation
        return result

    def parseExpression(self):
        return self.parseAddAndSub()
        
    def parseAddAndSub(self):
        result = self.parseMulAndDiv()
        while True:
            self.skipSpaces()
            char=self.getCurrent()
            if char in '+-':
                self.advance()
                self.skipSpaces()
                if self.getCurrent() in '+-':
                    raise Error('Expression expected',self.i)
            
            if char=='+':
                result=result.add(self.parseMulAndDiv())
            elif char=='-':
                result=result.sub(self.parseMulAndDiv())
            else:
                break
        return result
    
    def parseMulAndDiv(self):
        result = self.parseBrackets()
        while True:
            self.skipSpaces()
            if self.getCurrent()=='*':
                self.advance()
                result=result.mul(self.parseBrackets())
            
            #implicit multiplication         
            elif ( ( self.getPrevious() in '0123456789)' and self.getCurrent() in '(l'+self.allowedVariables) or
            (self.getPrevious() in self.allowedVariables and self.getCurrent() in '(') or
            (self.getPrevious() in ')' and self.getCurrent() in '01234567890.') ):

                result=result.mul(self.parseBrackets())
            
            elif self.getCurrent()=='/':
                pos=self.i
                self.advance()
                dividor=self.parseBrackets()
                try:
                    result=result.div(dividor)
                except Exception as e:
                    raise Error(str(e),pos)
            else:
                break
        return result
    
    def parseBrackets(self):
        self.skipSpaces()
        if self.getCurrent()=='(':
            self.advance()
            r=self.parseExpression()
            self.skipSpaces()
            if self.getCurrent()!=')':
                raise Error('Expecting closing bracket',self.i)
            self.advance()
            return r  
        return self.parseLog()

    def parseLog(self):
        self.skipSpaces()
        if self.string[self.i:self.i+3]=='log':
            self.i=self.i+3
            pos=self.i
            if not self.hasCurrent() or self.getCurrent()!='(':
               raise Error('Expecting opening bracket of log function',self.i)
            r=self.parseExpression()
            try:
                return r.log()
            except Exception as e:
                raise Error(str(e),pos+1)          
        return self.parseUmin()
          
    def parseUmin(self):
        self.skipSpaces()
        if self.getCurrent() in '+-':
            char=self.getCurrent()
            self.advance()
            self.skipSpaces()
            if self.getCurrent() in '(01234567890l.'+self.allowedVariables:
                p=self.parseBrackets()
                if char=='-':
                    return p.umin()
                else:
                    return p
            else:
                raise Error('Expression expected',self.i)  
        return self.parseVariables()
      
    def parseVariables(self):
        self.skipSpaces()
        if self.getCurrent() in self.allowedVariables:
            if self.variable and self.getCurrent()!=self.variable:
                raise Error('Seen "'+self.variable+'" already, but an extra variable "'+self.getCurrent()+'" found',self.i)
            self.variable=self.getCurrent()
            self.advance()
            return polynomial([0,1])
        return self.parseNumbers()
    
    def parseNumbers(self):
        self.skipSpaces()
        decimalFound=False
        numberString=''
        while self.getCurrent() in '01234567890.':
            if self.getCurrent()=='.':
                if decimalFound==True:
                    raise Error('Unexpected decimal point',self.i)
                decimalFound=True
            numberString +=self.getCurrent()
            self.advance()

        if numberString=='.':
            raise Error('Expecting a number',self.i)
            
        if numberString=='':
            raise Error('Expression expected',self.i)
            
        return polynomial([float(numberString)])