# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 15:20:59 2018

@author: Alex
"""

class Error(Exception):
    def __init__(self,message,position):
        self.message = message
        self.position = position