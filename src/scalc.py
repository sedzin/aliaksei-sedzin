# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:08:24 2018

@author: Alex
"""
import sys
import math


def evaluate(string,stringPosition):
    if len(string)==0:
        raise Exception('Expression expected at position '+str(stringPosition))
   
    # skip leading spaces
    i=0
    while i<len(string) and string[i]==' ':
        i=i+1
    if i>0:
        result=evaluate(string[i:],i)
        return result
    
    # TODO:
    
    # make a table with operators in one go
    
    # take the operator with least priority and execute it recursively
    
    # if no operators found try to unfold the brackets
    
    # if no brackets found interpet as a variable or a number
    
    
    openBrackets=0
    
    for i in range(0,len(string)):
        if string[i]=='(':
            openBrackets+=1
        if string[i]==')':
            openBrackets-=1
        if openBrackets<0:
            raise Exception ('Unexpected closing bracket at position '+str(stringPosition+i))
        if openBrackets==0 and string[i]=='+' and i>0: # check if the + is not leading
            s1=string[0:i]
            s2=string[i+1:]
            result=evaluate(s1,stringPosition)+evaluate(s2,stringPosition+i+1)
            # break the loop
            return result 
        
        if openBrackets==0 and string[i]=='-' and i>0: # check if the - is not leading
            s1=string[0:i]
            s2=string[i+1:]
            result=evaluate(s1,stringPosition)-evaluate(s2,stringPosition+i+1)
            # break the loop
            return result 
    
    # try to find * and / and implicit multiplication.
    # TODO: need to find rightmost operation
    openBrackets=0
    lastSymbol='#'
    for i in range(len(string)):
        if string[i]=='(':
            openBrackets+=1
        if string[i]==')':
            openBrackets-=1
        if openBrackets<0:
            raise Exception ('Unexpected closing bracket at position '+str(stringPosition+i))
        
       
        if openBrackets==0 and string[i]=='*':
            s1=string[0:i]
            s2=string[i+1:]
            result=evaluate(s1,stringPosition)*evaluate(s2,stringPosition+i+1)
            # break the loop
            return result 
        
        if openBrackets==0 and string[i]=='/':
            s1=string[0:i]
            s2=string[i+1:]
                        
            r2=evaluate(s2,stringPosition+i+1)
            if r2==0:
                raise Exception ('Division by 0 at position '+str(stringPosition+i))
            r1=evaluate(s1,stringPosition)
            result=r1/r2
            # break the loop
            return result 
        
   
        
        if openBrackets==0 or (openBrackets==1 and string[i]=='(' ) :
            if  ( (lastSymbol in '0123456789)' and string[i] in '(xyl') or 
                 (lastSymbol in 'xy' and string[i] in '(') ):
                s1=string[0:i]
                s2=string[i:]
                result=evaluate(s1,stringPosition)*evaluate(s2,stringPosition+i)
                return result
        
        
        
        
        lastSymbol=string[i]
    # try to find matching brackets 
    
    if string[0]=='(':
        openBrackets=1
        for i in range(1,len(string)):
            if string[i]=='(':
                openBrackets+=1
            if string[i]==')':
                openBrackets-=1
            if openBrackets<0:
                raise Exception ('Unexpected closing bracket at position '+str(stringPosition+i))
            if openBrackets==0:
                s1=string[1:i]
                result=evaluate(s1,stringPosition+1)
                # break the loop
                return result 
    
    # try to find log function
    if len(string)>2 and string[0:3]=='log':
        
        openBrackets=0
        for i in range(3,len(string)):
            if string[i]=='(':
                openBrackets+=1
            if string[i]==')':
                openBrackets-=1
            if openBrackets<0:
                raise Exception ('Unexpected closing bracket at position '+str(stringPosition+i))
            if openBrackets==0:
                s1=string[4:i]
                
                result=evaluate(s1,stringPosition+4)
                if result<=0:
                    raise Exception ('Log of a negative argument at position '+str(stringPosition))
                # break the loop
                result=math.log(result)
                return result 
    
    
    
    # try to find leading + or -
    openBrackets=0
    if string[0]=='-' or string[0]=='+':
        s1=string[1:]
        result=evaluate(s1,stringPosition+1)
        if string[0]=='-':
            result=-result
        return result     

    # no operations found, must be a number
    try :
        result=float(string)
        return float(string)
    except Exception as e:
        raise Exception('Could not evaluate expression at position '+str(stringPosition))
    
    



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
            raise Exception('Too many arguments. Please remove whitespaces from the input expression or use doublequotes("")')
        else:
            r = evaluate(args[1],0)
            r = round(r,9)
            value=str(r)
    except Exception as e:
        # raise e # uncomment the line if need to debug the code
        value = str(e)
    return (value)

if __name__=='__main__':
    value=scalc()
    print(value)

    