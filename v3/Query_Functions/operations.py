from math import *

'''
Applies arithmatic functions on a specified rows
Can also apply multiple operations on multiple rows
'''
def row_arithmatic(row:list, operations: dict):
    for index in operations:
        val = row[index]
        row[index] = eval(operations[index]) #NOTE: Security Risk
    return row