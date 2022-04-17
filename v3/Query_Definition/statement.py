from operator import *
from typing import Dict

'''
    compares value and target based off of an operation and
    returns true or false
'''
def compare_numbers_strings(operation,val,target):
    match operation:
        case '==':
            return eq(val, target)
        case '>':
            return gt(val,target)
        case '<':
            return lt(val,target)
        case '<=':
            return le(val,target)
        case '>=':
            return ge(val,target)
        case '!=':
            return ne(val,target)

def compare_dates(operation,val,target):
        pass

class Statement:
    '''
    Defines a query statement
        - col: "Name of column subject to operation"
        - operation: How the column will be assesed, 
                - options['==','>','<','!=','>=','<=']
        - target: value used in comlumn assemsment

    '''
    def __init__(self, statement: Dict):
        if statement:
            self.load(statement["column"],statement["operation"],statement["target"])
        else:
            self.load(None,None,None)

    def load(self,col,operation,target):
        self.column = col
        self.operation = operation
        self.target = target
        return self
        
    def export(self):
        statement = {
            "column": self.column,
            "operation": self.operation,
            "target": self.target
        }
        return statement
    
    def exec(self, data_type, values_list):
        '''
            list of values are filtered based off of the operation and 
            target values within statement object, returns
            a list of indexes of the values that pass each statemtent contraints.
        '''
        if data_type == "date":
            qualified_indexes = [i for i in range(len(values_list)) 
                             if compare_dates(self.operation,values_list[i], self.target)]
        else:
            qualified_indexes = [i for i in range(len(values_list)) 
                             if compare_numbers_strings(self.operation,values_list[i], self.target)]
        return qualified_indexes
    