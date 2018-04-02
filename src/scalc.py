# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 15:08:24 2018

@author: Alex
"""

import sys
from parselib import Parser
from error import Error

def helpText():
    value=(
           'Simple Scientific Calculator\n'+
           'USAGE:    scalc [math expression]\n'+
           'Supported functions: +,-,*,/,log\n'+
           'Supported variables: single x or y\n' +
           'Supported equations type: linear\n' +
           'Examples: scalc (2+3)*6, scalc "x = log(12)-x"\n'
           )
    return value

def scalc():

    args = sys.argv
    narg=len(args)
    
    if narg==1:
        return helpText()
    
    if narg>2:
        return 'Error: Too many command line arguments. Remove spaces or use doublequotes (e.g. scalc "1  +  2")'
    
    string=args[1]
    try:
        p=Parser(string)
        return p.evaluate()
              
    except Error as e:
        space=' '*e.position
        output= (string+'\n'+space+'^\n'+'Error: '+str(e.message)+' at position '+str(e.position+1) )
        return output


if __name__=='__main__':
    output=scalc()
    print(output)  
