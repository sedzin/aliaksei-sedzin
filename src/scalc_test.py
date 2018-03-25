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
     
     [(
       'log (2)\n'+
       '   ^\n'+
       'Error: Expecting opening bracket of log function at positoin 4'
      ),
       'log (2)'],
            
     [(
       'Simple Scientific Calculator\n'+
       'USAGE:    scalc [math expression]\n'+
       'Example:  scalc (2+3)*6' 
      )],
       
          
       
     ['10.0'        ,'   10'          ], 
     ['5.0'         ,'  2+3  '        ], 
     ['-5.0'        ,'    -2+-3  '    ], 
     ['10.0'        ,' 2+2* 2 *2  '   ], 
     ['6.0'         ,'-  2+2*2* 2  '  ],
     ['14.666666667','2( 22  )/3  '   ], 
     ['2.302585093' ,'log(10)'        ],
     
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


    if expectedResult==result:
        testSucceeded=True
    
    if testSucceeded:
        msg='OK' 
    else:
        msg='ERROR!!!'
        winsound.Beep(600, 250)

    print('\nArguments    \n'+str(arguments))
    print('\nResult       \n'+result+'.')
    print('\nExpected     \n'+expectedResult+'.')
    print('\n'+msg+'\n\n\n')
    
