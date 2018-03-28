# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:00:23 2018

@author: Alex
"""


import unittest
import sys
from scalc import scalc     


class TestScalc(unittest.TestCase):
    
    def test_number(self):
        
        sys.argv=['scalc','10']
        self.assertEqual(scalc(),'10')
  
        sys.argv=['scalc','11.3']
        self.assertEqual(scalc(),'11.3')
        
        sys.argv=['scalc','-2.3']
        self.assertEqual(scalc(),'-2.3')
        
        sys.argv=['scalc','-.3']
        self.assertEqual(scalc(),'-0.3')
  
        sys.argv=['scalc','-2..3']
        self.assertEqual(scalc(),'-2..3\n   ^\nError: Unexpected decimal point at position 4')
        
        sys.argv=['scalc','1&00']
        self.assertEqual(scalc(),'1&00\n ^\nError: Unrecognised character "&" at position 2')
        
        sys.argv=['scalc','.']
        self.assertEqual(scalc(),'.\n ^\nError: Expecting a number at position 2')
        
    def test_variable(self):
        
        sys.argv=['scalc','x']
        self.assertEqual(scalc(),'x')
  
        sys.argv=['scalc','y']
        self.assertEqual(scalc(),'y')
  
        sys.argv=['scalc','z']
        self.assertEqual(scalc(),'z\n^\nError: Unrecognised character "z" at position 1')
        
        sys.argv=['scalc','l']
        self.assertEqual(scalc(),'l\n^\nError: Expecting a number or a decimal point at position 1')
        
    def test_addition(self):
        sys.argv=['scalc','1+1']
        self.assertEqual(scalc(),'2')
  
        sys.argv=['scalc','x+x']
        self.assertEqual(scalc(),'2x')
        
        sys.argv=['scalc','x+x+1.1+3']
        self.assertEqual(scalc(),'2x+4.1')
        
        sys.argv=['scalc','x++x']
        self.assertEqual(scalc(),'x++x\n  ^\nError: Expression expected at position 3')
        
        
    
    def test_subtraction(self):
        
        sys.argv=['scalc','10-.1']
        self.assertEqual(scalc(),'9.9')
  
        sys.argv=['scalc','x-x-x']
        self.assertEqual(scalc(),'-x')
        
        sys.argv=['scalc','3-x-8']
        self.assertEqual(scalc(),'-x-5')
        
        sys.argv=['scalc','x--x']
        self.assertEqual(scalc(),'x--x\n  ^\nError: Expression expected at position 3')
        
        
    
    def test_multiplication(self):
        
        sys.argv=['scalc','2*3.1']
        self.assertEqual(scalc(),'6.2')
  
        sys.argv=['scalc','3*x*x']
        self.assertEqual(scalc(),'3x^2')
        
        sys.argv=['scalc','3(3)x']
        self.assertEqual(scalc(),'9x')
    
        
        sys.argv=['scalc','2**3']
        self.assertEqual(scalc(),'2**3\n  ^\nError: Expression expected at position 3')
        
  
    def test_division(self):
        
        sys.argv=['scalc','1/3']
        self.assertEqual(scalc(),'0.333333333')
  
        sys.argv=['scalc','x/3']
        self.assertEqual(scalc(),'0.333333333x')
        
        sys.argv=['scalc','x/x']
        self.assertEqual(scalc(),'1')
        
        sys.argv=['scalc','100/0']
        self.assertEqual(scalc(),'100/0\n   ^\nError: Division by 0 at position 4')
  
        sys.argv=['scalc','100/x']
        self.assertEqual(scalc(),'100/x\n   ^\nError: Non-zero reminder while dividing polynomials at position 4')
  
    
    def test_log(self):
        
        sys.argv=['scalc','log(10)']
        self.assertEqual(scalc(),'2.302585093')
  
        sys.argv=['scalc','log(-2)']
        self.assertEqual(scalc(),'log(-2)\n    ^\nError: Log from a non-positive argument at position 5')
  
        sys.argv=['scalc','log7']
        self.assertEqual(scalc(),'log7\n   ^\nError: Expecting opening bracket of log function at position 4')
  
        sys.argv=['scalc','log(y)']
        self.assertEqual(scalc(),'log(y)\n    ^\nError: Can not take log from a polynomial at position 5')
  
    def test_umin(self):
        
        sys.argv=['scalc','-20']
        self.assertEqual(scalc(),'-20')
  
        sys.argv=['scalc','-x']
        self.assertEqual(scalc(),'-x')
  
        sys.argv=['scalc','--x']
        self.assertEqual(scalc(),'--x\n ^\nError: Expression expected at position 2')
  
    def test_uplus(self):
        
        sys.argv=['scalc','+20']
        self.assertEqual(scalc(),'20')
  
        sys.argv=['scalc','+x']
        self.assertEqual(scalc(),'x')
  
        sys.argv=['scalc','++x']
        self.assertEqual(scalc(),'++x\n ^\nError: Expression expected at position 2')
        
        sys.argv=['scalc','+-x']
        self.assertEqual(scalc(),'+-x\n ^\nError: Expression expected at position 2')
    
    
    def test_brackets(self):
        
        sys.argv=['scalc','(20)']
        self.assertEqual(scalc(),'20')
  
        sys.argv=['scalc','((x))']
        self.assertEqual(scalc(),'x')
  
        sys.argv=['scalc','((x']
        self.assertEqual(scalc(),'((x\n   ^\nError: Expecting closing bracket at position 4')
        
        sys.argv=['scalc',')10(']
        self.assertEqual(scalc(),')10(\n^\nError: Unexpected closing bracket at position 1')
        
        sys.argv=['scalc','12)']
        self.assertEqual(scalc(),'12)\n  ^\nError: Unexpected closing bracket at position 3')
    
    
    def test_expressions(self):
        
        sys.argv=['scalc','20+2*4']
        self.assertEqual(scalc(),'28')
  
        sys.argv=['scalc','((x/x)x)']
        self.assertEqual(scalc(),'x')
  
        sys.argv=['scalc','-2(x+1)(x+1)']
        self.assertEqual(scalc(),'-2x^2-4x-2')
        
        sys.argv=['scalc','(y+9)(y+10)(y+10)']
        self.assertEqual(scalc(),'y^3+29y^2+280y+900')
    
        sys.argv=['scalc','(y+9)(y+10)(y+10)/(y+10)']
        self.assertEqual(scalc(),'y^2+19y+90')
    
    
  
    def test_equations(self):
        
        sys.argv=['scalc','x=10']
        self.assertEqual(scalc(),'x=10')
  
        sys.argv=['scalc','x(x+1)=x']
        self.assertEqual(scalc(),'x=0')
  
        sys.argv=['scalc','(y-1)(y+1)=y*y-1']
        self.assertEqual(scalc(),'y=Any (any value is a valid solution)')
        
        sys.argv=['scalc','2=3']
        self.assertEqual(scalc(),'False')
  
        sys.argv=['scalc','2*2=4']
        self.assertEqual(scalc(),'True')
        
        sys.argv=['scalc','2*2==4']
        self.assertEqual(scalc(),'2*2==4\n    ^\nError: An extra "=" character found at position 5')
        
        sys.argv=['scalc','(x=4)']
        self.assertEqual(scalc(),'(x=4)\n  ^\nError: Expecting closing bracket at position 3')
        
        sys.argv=['scalc','78+x=']
        self.assertEqual(scalc(),'78+x=\n     ^\nError: Expression expected at position 6')
       
        sys.argv=['scalc','=78+x']
        self.assertEqual(scalc(),'=78+x\n^\nError: Expression expected at position 1')
       
        sys.argv=['scalc','x=y']
        self.assertEqual(scalc(),'x=y\n  ^\nError: Seen "x" already, but an extra variable "y" found at position 3')
       
        
        
    def test_errors(self):
        
        sys.argv=['scalc','////']
        self.assertEqual(scalc(),'////\n^\nError: Expression expected at position 1')
  
        sys.argv=['scalc','x()*x/(6)']
        self.assertEqual(scalc(),'x()*x/(6)\n  ^\nError: Expression expected at position 3')
  
        sys.argv=['scalc','yyy']
        self.assertEqual(scalc(),'yyy\n ^\nError: Unexpected character after a variable "y" at position 2')
        
        sys.argv=['scalc','x','2']
        self.assertEqual(scalc(),'Error: Too many command line arguments. Remove spaces or use doublequotes (e.g. scalc "1  +  2")')
        
        
    def test_help(self):
        
        sys.argv=['scalc']
        expectedText= (
      'Simple Scientific Calculator\n'+
      'USAGE:    scalc [math expression]\n'+
      'Supported functions: +,-,*,/,log\n'+
      'Supported variables: single x or y\n' +
      'Supported equations type: linear\n' +
      'Examples:  scalc (2+3)*6, scalc x+10=12-x, scalc "y(y+y)y*log(10)"\n'
      )
        self.assertEqual(scalc(),expectedText)
  
        
if __name__ == '__main__':
    unittest.main()

