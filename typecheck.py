#!/bin/python2
import sys
import inspect, itertools 
from collections import OrderedDict
import re

class TypeCheckerDummyClass:
    pass

class TypeChecker(object):
    '''
    A decorator that attempts to provide rudimentary type checking for function 
    calls
    Types are encoded via a sort of naieve Hungarian notation
    If the types of the values of the decorated functions arguments do not 
    match the type of the functions values, an exception is thrown.
    '''
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

    def getArgsInfo(self, arrArgNames, arrArgValues, index = 0):
        arrArgTypes = [TypeChecker.dctTypes.get(re.split('[^a-z]', x)[0], '') for x in arrArgNames]
        arrValTypes = [type(x) for x in arrArgValues]
        return [x for x in itertools.izip(range(index, len(arrArgNames) + index), arrArgNames, arrArgTypes, arrValTypes)]
        

    def call(self, *args, **kwargs):
        arrTypes = self.getArgsInfo(inspect.getargspec(self.function)[0] + kwargs.keys(), list(args) + kwargs.values()) 
        arrTypesKW = self.getArgsInfo(kwargs.keys(), kwargs.values(), len(arrTypes) + 1)
        sMismatch = '\n'.join(['Arg(%d) %s: Expected %s, got %s' % t for t in (arrTypes + arrTypesKW) if t[2] and t[2] != t[3]])
       
        if len(sMismatch):
            raise Exception(sMismatch) 

        self.function.__call__(*args, **kwargs)


                         
def typecheck(function):
    return TypeChecker(function).call

@typecheck
def fn(fCount, sName, dctTest, aThing=1, **kwargs):
    print locals()

fn(1.0, 'apple', {'hell' : 'world'}, fApple=1.2)

fn(1.0, 'apple', {'hell' : 'world'}, fApple=1)
