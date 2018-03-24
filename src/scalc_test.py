# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 16:00:23 2018

@author: Alex
"""

import sys
import scalc
import winsound      


# define test vectors as follows
# [expected result, arg1(optional), arg2(optional)]
testVectors=[
     ['10.0'        ,'10'          ], 
     ['Simple Scientific'          ], 
     ['5.0'         ,'2+3'         ], 
     ['-5.0'        ,' -2+-3  '    ], 
     ['10.0'        ,' 2+2*2*2  '  ], 
     ['6.0'         ,'-  2+2*2*2  '],
     ['14.666666667','2(22)/3  '   ], 
     ['2.302585093' ,'log(10)'     ],
     [' '           ,'((('     ],
     ['Too many'    ,  '**', '2+3' ] 
     
    ]


for testVector in testVectors:
    testSucceeded=False
    narg=len(testVector)
    expectedResult=testVector[0]
    arguments=testVector[1:]
    
    
    # set up system arguments
    argv=['scalc.py']
    if narg>1:
        argv=argv+arguments
    sys.argv=argv
    
    result=scalc.scalc()

    if narg==2: #test if result exactly matches the expectation
        if expectedResult==result:
            testSucceeded=True
    else: # test if result contains the necessary substring
        if expectedResult in result:
            testSucceeded=True
            expectedResult=expectedResult+'..' 
    
    if testSucceeded:
        msg='OK' 
    else:
        msg='ERROR!!!'
        winsound.Beep(600, 250)

    print('\nArguments    '+str(arguments))
    print('Result       '+result+'.')
    print('Expected     '+expectedResult+'.')
    print(msg)
    
