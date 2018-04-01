# scalc

A simple command line scientific calculator 
The calculator supports: +, -, *, /, log, unary - and + on floating point numbers
The calculator supports solving linear equations with a single variable (x or y).
The calculator supports parentheses in both modes


## Assignment

A simple scientific calculator with the following features had to be created:

The calculator supports addition, subtraction, multiplication, division, log on floating point numbers.
The calculator can solve simple linear equations with a single variable (namely, x or y), for simplicity, only addition, subtraction and multiplication operations are allowed.
The calculator supports parentheses in both modes.
The calculator should have a language parser.
Do not use any library that can accomplish any of the listed requirements.
The calculator should handle all error cases properly (by carefully indicating the errors to the user).
Write tests.

Examples:

input: (3+(4-1))*5
output: 30

input: 2 * x + 0.5 = 1
output: x = 0.25

input: 2x + 1 = 2(1-x)
output: x = 0.25

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

A Python 3.6 development environment is required. 
For example the following distribution can be used:
* [Anaconda](https://www.anaconda.com/what-is-anaconda/)


### Installing

Please refer to the installation instructions of the development environment itself.
Copy the source files in a working directory.
The calculator can be run from the development environment terminal by using the following command
``` run scalc ```
For example
```
run scalc 2+2
```
should produce the following output
```
4
```

And running 
```
run scalc "(x+1)(x+1)=x"
```
should produce
```
x = 0.5
```

## Running the tests

Run test_scalc.py and the tests should run automatically.

## Built With

* [Anaconda](https://www.anaconda.com/what-is-anaconda/) - Python distribution
* [Spyder](https://pythonhosted.org/spyder/) - Development environment (included in Anaconda)
* [Git](https://git-scm.com/) - Version control

## Authors

* **Alex Sedzin**