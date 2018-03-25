# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:08:24 2018

@author: Alex
"""
import sys
import math

class Error(Exception):
    def __init__(self,message,position):
        self.message = message
        self.position = position


# TODO: correctly process expressions like 2 3

def evaluate(string,stringPosition):
    # strip leading and trailing spaces
    newString=string.strip()
    stringPosition+=string.find(newString)
    string=newString
    
    
    if len(string)==0:
        raise Error('Expression expected',stringPosition)

    
      
    # make a table containing positions of operators outside brackets
    operators=[-1]*8
    openBrackets=0
    lastSymbol='#'
    for i in range(0,len(string)):
        if string[i] not in ' 01234567890.-+*/()logxy':
            raise Error('Unrecognised character "'+string[i]+'"',stringPosition+i)
        if string[i]=='(':
            openBrackets+=1
        if string[i]==')':
            openBrackets-=1
        if openBrackets<0:
            raise Error('Unexpected closing bracket', stringPosition+i)
        if openBrackets==0: # only evaluate expressions outside brackets
            if string[i]=='+' and i>0: 
                operators[0]=i            
            if string[i]=='-' and i>0:
                operators[1]=i
            if string[i]=='*': 
                operators[2]=i
            if string[i]=='/': 
                operators[3]=i
        # handle implicit multiplication
        if openBrackets==0 or (openBrackets==1 and string[i]=='(' ) :
            if  ( (lastSymbol in '0123456789)' and string[i] in '(xyl') or 
                 (lastSymbol in 'xy' and string[i] in '(')  or
                 (lastSymbol in ')' and string[i] in '01234567890.') ):
                operators[4]=i
                
        lastSymbol=string[i]
    if openBrackets>0:
        raise Error('Expecting closing bracket -',stringPosition+i+1)
    
    if len(string)>2 and string[0:3]=='log':
        if len(string)<4 or string[3] !='(':
            raise Error('Expecting opening bracket of log function',stringPosition+3)
        operators[5]=2
    if string[0] == '+':
        operators[6]=0
    if string[0] == '-':
        operators[7]=0
    
    # find the operator with least priority 
    operator=-1
    for j in reversed(range(8)):
        if operators[j]>=0:
            operator=j
    if operator in range(2,5): # need to take the right-most multiplication
        operator = operators.index(max(operators[2:5]))
    
    pos=operators[operator] #position of the operator
    
    if operator>=0: # 
       
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
        
        # process the results of evaluation

        if operator==0 : # +
            result = r1+r2
        if operator==1 : #
            result = r1-r2
        if operator==2 or operator==4: # * or implicit *
            result = r1*r2
            
        if operator==3 : #
            
            if r2 == 0:
                raise Error('Division by 0',stringPosition+pos)
            result = r1/r2
        
        if operator==5 : # log
            if r2 <= 0:
                raise Error('Log from a non-positive argument',stringPosition+4)
            result = math.log(r2)
            
        if operator==6 : #
            result = r2
        if operator==7 : #
            result = -r2
        
        return result
    
    # try to unfold the brackets
    if string[0]=='(':
        if string[-1]==')':
            s2=string[1:-1]
            result=evaluate(s2,stringPosition+1)
            return result
        else:
            raise Error('Expecting closing bracket',stringPosition+len(string))
    
    # try to find variables
    if string[0] in 'xy':
            raise Error('Not (yet) able to process a variable',stringPosition)
    
    decimalFound=False
    for i in range(len(string)):
        if string[i] not in '0123456789.':
            raise Error('Expecting a number',stringPosition+i)
        if string[i]=='.':
            if decimalFound==True:
                raise Error('Unexpected (extra) decimal point',stringPosition+i)
    try :
        return float(string)
    except Exception as e:
        raise Error('Could not evaluate expression',stringPosition)
    
    
def helpText():
    value=(
           'Simple Scientific Calculator\n'+
           'USAGE:    scalc [math expression]\n'+
           'Example:  scalc (2+3)*6' )
    return value


def scalc():

    try:
        args = sys.argv
        narg=len(args)
        if narg==1:
            value=helpText()
        elif narg>2:
            raise Error('Error: Too many command line arguments',-1)
        else:
            r = evaluate(args[1],0)
            r = round(r,9)
            value=str(r)
    except Error as e:
        #raise e # uncomment the line if need to debug the code
        if e.position<0:
            value = str(e.message)
        else:
            space=' '*e.position
            value = ( args[1]+'\n'+
                      space+'^\n'+
                      'Error: '+ str(e.message)+' at positoin '+str(e.position+1) )
                      
            
    return (value)

if __name__=='__main__':
    value=scalc()
    print(value)

    