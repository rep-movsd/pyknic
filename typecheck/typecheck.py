#!/bin/python2
'''
A type checker for python2
==========================

FAQ


What is it?
-----------
Essentially a decorator that you apply to functions, which throws an exception 
if the wrong type of arguments are passed to the function. 


Why do we need it?
------------------
The bane of dynamic languages are type errors, which happen only on runtime.
It would be cool if we could catch type errors at the call site rather than 
deep inside a function or chaining down several functions.
Since even python3 has only type annotations, why not roll our own system?
It may lack elegance, but it does something useful


How does the decorator know the expected argument types?
--------------------------------------------------------
We tell it, using a kind of Hungarian notation - each function argument has a
type prefix that maps to a python type. The type prefix is all lowercase and 
extends upto the first non [a-z] character


Why this ugly camelCase? Hungarian notation is bad! etc. etc.
---------------------------------------------------------------
As for camelCase, feel free to change the regex if you need a different style
As for Hungarian notation, I use it all the time myself and my code is the 
better for it in all languages I use. I'd rather have some ugliness than type
errors. 
Also type prefixes work brilliantly with IDE autocomplete. It helps filter out 
the possible completions when you key in the type prefix.


Why not pass the argument types to the decorator?
-------------------------------------------------
If you did that, it woul be harder to read what param has what type and would 
look messy. Also, if you did that, you wouldn't catch errors if the arguments 
are reordered and the call sites not updated.
Here, it's just about renaming args and adding a parameter-less decorator, and
it will catch type errors caused by argument reordering


Does it work for keyword args?
------------------------------
Yes!


Does it work for default args?
------------------------------
Yes!


Can we add more types?
---------------------
Sure you can, the prefix to type mapping is in a dictionary, add entries to it 
dynamically with TypeChecker.registerType() or hardcode it into the dict


What if we need to ignore typechecks for some parameters?
--------------------------------------------------------
Use the prefix 'a' - like 'aParam' for parameters that you don't want the 
decorator to check. But think about whether you really want to do such a 
horrible thing.


What about nested types? Can we check for [int] or [(int,int)...] and so on?
----------------------------------------------------------------------------
One problem is how you can encode the type in the name consistently
The second problem is that python doesn't expose the complete type of a value
just by using type()
Instead of comparing types as strings, you can have a function that can "walk"
down a nested type and compare it against another. Maybe I'll implement it


How to use it?
--------------
Just import this file and apply the decorator @typecheck before each function.
Name your function arguments with their types prefixed
Turn this off in production code.


Why is the code so terse?
-------------------------
I hate loops, I like comprehensions


Can we do this for local variables somehow?
-------------------------------------------
Perhaps, I have an idea, lets see if it works.


This is a bad example of python
-------------------------------
I'm a C++ programmer, so be gentle!


This sucks! Dynamic languages need to be flexible! 
--------------------------------------------------
So do you, go do some Yoga

'''

import sys
import inspect, itertools 
from collections import OrderedDict
import re

class TypeCheckerDummyClass:
    pass

class TypeChecker(object):
    dctTypes = \
    {
        'a': None,
        'i': int,
        's': str,
        'b': bool,
        'f': float,
        'arr': list,
        'dct': dict,
        'set': set,
        'obj': object,
        'fn': type(lambda x: x),
        'cls': type(TypeCheckerDummyClass)
    }
    
    def __init__(self, function):
        self.function = function


    @classmethod
    def registerType(_, sPrefix, tType):
        TypeChecker.dctTypes[sPrefix] = tType


    def getArgsInfo(self, arrArgNames, arrArgValues):
        arrArgTypes = [TypeChecker.dctTypes.get(re.split('[^a-z]', x)[0], '') for x in arrArgNames]
        arrValTypes = [type(x) for x in arrArgValues]
        return [x for x in itertools.izip(range(0, len(arrArgNames)), arrArgNames, arrArgTypes, arrValTypes, arrArgValues)]
        

    def call(self, *args, **kwargs):
        argSpec = inspect.getargspec(self.function)
        arrNames = argSpec[0]
        arrDefaults = list(argSpec[3] or ())
        arrTypes = self.getArgsInfo(arrNames + kwargs.keys(), list(args) + arrDefaults + kwargs.values()) 
        sTypeCheckerMismatch = '\n'.join(['Arg(%d) %s: Expected %s, got %s with value "%s"' % t for t in arrTypes if t[2] and t[2] != t[3]])
        if len(sTypeCheckerMismatch):
            raise Exception('Type check errors in function ' + self.function.__name__ + '\n' + sTypeCheckerMismatch) 
        self.function.__call__(*args, **kwargs)

def typecheck(function):
    return TypeChecker(function).call

if __name__ == '__main__':

    @typecheck
    def fn(fCount, sName, dctTest, iThing, untyped, fApple, **kwargs):
        print 'OK!'

    print '''fn(fCount, sName, dctTest, iThing, untyped, fApple, **kwargs)\n'''

    try:
        print '''Testing:  fn(1.0, 'banana', {'hell' : 'world'}, "s", 'whatevs', fApple=1.2)'''
        fn(1.0, 'banana', {'hell' : 'world'}, "s", 'whatevs', fApple=1.2)
    except Exception as e:
        print e;
    
    try:
        print '''\nTesting: fn(1.0, 'banana', {'hell' : 'world'}, 1, 1, fApple=1.2)'''
        fn(1.0, 'banana', {'hell' : 'world'}, 1, 1, fApple=1.2)
    except Exception as e:
        print e;
    
    
    
    #fn(1.0, 'apple', {'hell' : 'world'}, "Ha", fApple=1)
