# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:08:24 2018

@author: Alex
"""
import sys
from polynomial import polynomial

class Error(Exception):
    def __init__(self,message,position):
        self.message = message
        self.position = position
        

# Classify and sanity check the sting (allowed characters, equation or expression, variables)
# Then process the string according to the classification
def assess(string):
    
    EqualSignPos=-1
    Variable='#'
    
    for i in range(0,len(string)):
        if string[i] not in ' 01234567890.-+*/()logxy=':
            raise Error('Unrecognised character "'+string[i]+'"',i)
        if string[i] == '=':
            if EqualSignPos>=0:
                raise Error('An extra "=" character found',i)
            EqualSignPos=i
        if string[i] in 'xy':
            if Variable in 'xy' and string[i]!=Variable:
                raise Error('Seen variable "'+Variable+'" already, but an extra variable "'+string[i]+'" found',i)
            Variable=string[i]
        
    
    if EqualSignPos<0: # expression; evaluate it
        r=evaluate(string,0)
        r=str(r)
        r=r.replace('x',Variable)
        return r
        
    if EqualSignPos>=0: # equation; try to solve it
        
        p1=evaluate(string[0:EqualSignPos],0) # evaluate the left side
        p2=evaluate(string[EqualSignPos+1:],EqualSignPos+1) # evaluate the right side
        p3=p1.sub(p2) # subtract the latter from the former
        
        if Variable!='#': # equation with a variable; solve it
            return Variable+'='+str(p3.solve())
        else: # no variables; check if the equation is an identity
            if str(p3)=='0':
                return 'True'
            else:
                return 'False'

# Evaluate an expression
def evaluate(string,stringPosition):
    # strip leading and trailing spaces
    newString=string.strip()
    stringPosition+=string.find(newString)
    string=newString
     
    if len(string)==0:
        raise Error('Expression expected',stringPosition)
    
    # make a table containing positions of operators outside brackets
    # following are the operators in increasing order of priority
    # [+, -, *, /, implicit *, log, unary +, unary - ]
    opPositions=[-1]*8
    openBrackets=0
    lastSymbol='#'
    for i in range(0,len(string)):

        if string[i]=='(':
            openBrackets+=1
        if string[i]==')':
            openBrackets-=1
        if openBrackets<0:
            raise Error('Unexpected closing bracket', stringPosition+i)
        if openBrackets==0: # only evaluate expressions outside brackets
            if string[i]=='+' and i>0: 
                opPositions[0]=i            
            if string[i]=='-' and i>0:
                opPositions[1]=i
            if string[i]=='*': 
                opPositions[2]=i
            if string[i]=='/': 
                opPositions[3]=i
        # handle implicit multiplication
        if openBrackets==0 or (openBrackets==1 and string[i]=='(' ) :
            if  ( (lastSymbol in '0123456789)' and string[i] in '(xyl') or 
                 (lastSymbol in 'xy' and string[i] in '(')  or
                 (lastSymbol in ')' and string[i] in '01234567890.') ):
                opPositions[4]=i
                
        lastSymbol=string[i]
    if openBrackets>0:
        raise Error('Expecting closing bracket',stringPosition+i+1)
    
    if len(string)>2 and string[0:3]=='log':
        if len(string)<4 or string[3] !='(':
            raise Error('Expecting opening bracket of log function',stringPosition+3)
        opPositions[5]=2
    if string[0] == '+':
        opPositions[6]=0
    if string[0] == '-':
        opPositions[7]=0
    
    # find the operator with the least priority 
    operator=-1
    for j in reversed(range(8)):
        if opPositions[j]>=0:
            operator=j
    if operator in range(2,5): # need to take the right-most multiplication or division
        operator = opPositions.index(max(opPositions[2:5]))
    
    pos=opPositions[operator] #position of the operator with least priority
    if operator>=0: 
        # form and evaluate argument strings
        if operator in range(0,4): # +-*/
            s1=string[0:pos]
            s2=string[pos+1:]
            r1= evaluate(s1,stringPosition)
            r2 = evaluate(s2,stringPosition+pos+1)
            
        if operator==4: # implicit * 
            s1=string[0:pos]
            s2=string[pos:]
            r1= evaluate(s1,stringPosition)
            r2 = evaluate(s2,stringPosition+pos)

        
        if operator in range(5,8): # log or -
            s2=string[pos+1:]
            r2 = evaluate(s2,stringPosition+pos+1)
        
        # apply the operator

        if operator==0 : # +
            result = r1.add(r2)
        if operator==1 : # -
            result = r1.sub(r2)
        if operator==2 or operator==4: # * or implicit *
            result = r1.mul(r2)
            
        if operator==3 : # /
            try:
                result = r1.div(r2)
            except Exception as e:
                raise Error(e,stringPosition+pos)
        
        if operator==5 : # log
            try:
                result = r2.log()
            except Exception as e:
                raise Error(e,stringPosition+4)
            
        if operator==6 : # unary +
            result = r2
        if operator==7 : # unary -
            result = r2.umin()
        
        return result
    
    # no operators found outside of brackets
    
    # unfold the brackets
    if string[0]=='(':
        if string[-1]==')':
            s2=string[1:-1]
            result=evaluate(s2,stringPosition+1)
            return result
        else:
            raise Error('Expecting closing bracket',stringPosition+len(string))
    
    # parse variables
    if string[0] in 'xy':
        if len(string)>1:
            raise Error('Unexpected character after a variable "'+string[0]+'"',stringPosition+1)
        return polynomial([0,1])
    
    # parse numbers
    decimalFound=False
    for i in range(len(string)):
        if string[i] not in '0123456789.':
            raise Error('Expecting a number',stringPosition+i)
        if string[i]=='.':
            if decimalFound==True:
                raise Error('Unexpected (extra) decimal point',stringPosition+i)
    
    return polynomial([float(string)])
    
    # something went wrong during parsing
    raise Error('Could not evaluate expression',stringPosition)
    
    
def helpText():
    value=(
           'Simple Scientific Calculator\n'+
           'USAGE:    scalc [math expression]\n'+
           'Supported functions: +,-,*,/,log\n'+
           'Supported variables: x,y\n' +
           'Supported equations type: linear\n' +
           'Examples:  scalc (2+3)*6, scalc x+10=12-x, scalc "y(y+y)y*log(10)"\n'
           )
    return value


def scalc():

    try:
        args = sys.argv
        narg=len(args)
        if narg==1:
            output=helpText()
        elif narg>2:
            raise Error('Error: Too many command line arguments',-1)
        else:
            output = assess(args[1])
    except Error as e:
        #raise e # uncomment the line if need to debug the code
        if e.position<0:
            output = str(e.message)
        else:
            space=' '*e.position
            output = ( args[1]+'\n'+
                      space+'^\n'+
                      'Error: '+ str(e.message)+' at position '+str(e.position+1) )
                      
            
    return output

if __name__=='__main__':
    output=scalc()
    print(output)

    