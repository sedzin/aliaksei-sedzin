# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:14:38 2018

@author: Alex
"""

import unittest
from polynomial import polynomial


class TestPolynomial(unittest.TestCase):
    
    def test_eq(self):
        p1=polynomial([10,10,10])
        p2=polynomial([10,10,10])
        p3=polynomial([1])
        self.assertTrue(p1==p2)
        self.assertFalse(p1==p3)
        self.assertFalse(p1!=p2)
        self.assertTrue(p1!=p3)
        

    
    def test_string(self):
        P1=polynomial([10])
        s=str(P1)
        self.assertEqual(s,'10')
        P1=polynomial([-10,0,10,-14.2])
        s=str(P1)
        self.assertEqual(s,'-14.2x^3+10x^2-10')

    def test_add(self):
        self.assertEqual(polynomial([1,1]).add(polynomial([1,1])),polynomial([2,2]))

    def test_sub(self):
        self.assertEqual(polynomial([1,1]).sub(polynomial([1,1])),polynomial([0]))
        self.assertEqual(polynomial([1,1]).sub(polynomial([1,1,0,2.3])),polynomial([0,0,0,-2.3]))

    def test_mul(self):
        self.assertEqual(polynomial([1,1]).mul(polynomial([1,1])),polynomial([1,2,1]))
        self.assertEqual(polynomial([10.1,-10]).mul(polynomial([2,3])),polynomial([20.2,10.3,-30]))
        
    def test_div(self):
        self.assertEqual(polynomial([1,2,1]).div(polynomial([1,1])),polynomial([1,1]))    
        
        with self.assertRaises(Exception) as context:
            polynomial([1,2,1]).div(polynomial([0,1]))
        self.assertEqual('Non-zero reminder while dividing polynomials',str(context.exception))
        
        with self.assertRaises(Exception) as context:
            polynomial([1,1,1]).div(polynomial([0]))
        self.assertEqual('Division by 0',str(context.exception))
    
    def test_log(self):
        self.assertEqual(polynomial([10]).log(),polynomial([2.302585092994046]))    
        
        with self.assertRaises(Exception) as context:
            polynomial([1,1,1]).log()
        self.assertEqual('Can not take log from a polynomial',str(context.exception))
        
        with self.assertRaises(Exception) as context:
            polynomial([-10]).log()
        self.assertEqual('Log from a non-positive argument',str(context.exception))
    
    def test_umin(self):
        self.assertEqual(polynomial([1,1]).umin(),polynomial([-1,-1]))


if __name__ == '__main__':
    unittest.main()