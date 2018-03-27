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
 
# one empty input argument  
    [(
       '\n'+
       '^\n'+
       'Error: Expression expected at position 1'
      ),
       ''],
 
# no bracket after log 
    [(
        'log (2)\n'+
        '   ^\n'+
        'Error: Expecting opening bracket of log function at position 4'
         ),
        'log (2)'], 
       
# unexpected character
     [(
       '4*[9]\n'+
       '  ^\n'+
       'Error: Unrecognised character "[" at position 3'
      ),
       '4*[9]'], 


     [(
       '450/(4*3-12)=x\n'+
       '   ^\n'+
       'Error: Division by 0 at position 4'
      ),
       '450/(4*3-12)=x'], 

      
# no input arguments
     [(
      'Simple Scientific Calculator\n'+
      'USAGE:    scalc [math expression]\n'+
      'Supported functions: +,-,*,/,log\n'+
      'Supported variables: x,y\n' +
      'Supported equations type: linear\n' +
      'Examples:  scalc (2+3)*6, scalc x+10=12-x, scalc "y(y+y)y*log(10)"\n'
      )],

# valid expressions and equations         
     ['10'                       ,'   10'          ], 
     ['5'                        ,'  2+3  '        ], 
     ['-5'                       ,'    -2+-3  '    ], 
     ['10'                       ,' 2+2* 2 *2  '   ], 
     ['6'                        ,'-  2+2*2* 2  '  ],
     ['14.666666667'             ,'2( 22  )/3  '   ], 
     ['2.302585093'              ,'log(10)'        ],
     ['x^2+4x+4'                 ,'(2+x)(2+x)'     ],
     ['x=5'                      ,'x=5'            ],
     ['x=0'                      ,'2x=10x'         ],
     ['y=5.5'                    ,'2y-1=10'                  ],
     ['y=1'                      ,'(y+9)(y+10)/(y+10)=10'    ],
     ['y^3+29y^2+280y+900'       ,' (y+9)(y+10)(y+10)'       ],
     
    
    ]# end of testVectors

allTestsOK=True

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
        msg='Test detectd an ERROR!!!'
        allTestsOK=False
        winsound.Beep(600, 250)

        print('\nArguments    \n'+str(arguments))
        print('\nResult       \n'+result+'.')
        print('\nExpected     \n'+expectedResult+'.')
        print('\n'+msg+'\n\n\n')
if allTestsOK:
    print('All tests are OK')
