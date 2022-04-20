import unittest

from Query_Functions.filter import Filter


class TestFilter(unittest.TestCase):
    '''
    '''
    
    def test_or(self):
        '''
        NOTE: Ensure duplicates are removed
        '''
        reducer = Filter(None,None)
        conjunctive = ["or"]
        statement_results = [[1, 2, 3], [3, 4, 5]]
        reducer.filter_conjunctives(conjunctive,statement_results)
        assert(statement_results == [[1, 2, 3, 4, 5]])

    def test_and(self):
        reducer = Filter(None,None)
        conjunctive = ["and"]
        statement_results = [[1, 2, 3], [3, 4, 5]]
        reducer.filter_conjunctives(conjunctive,statement_results)
        assert(statement_results == [[3]])
        
    def test_and_or_mix(self):
        '''
        NOTE: the OR statment must comes first in operation precedence
        as we want to delay the removal of possible results till the end.
        '''
        reducer = Filter(None,None)
        conjunctive = ["and", "or"]
        statement_results = [[1, 2] ,[2 ,3], [4, 5, 6]]
        reducer.filter_conjunctives(conjunctive,statement_results)
        assert(statement_results == [[2]])
        
    def test_or_or_pass(self):
        reducer = Filter(None,None)
        conjunctive = ["or", "or"]
        statement_results = [[1, 2], [3, 4], [5, 6]]
        reducer.filter_conjunctives(conjunctive,statement_results)
        assert(statement_results == [[1, 2, 3, 4, 5, 6]])

    def test_and_and_fail(self):
        reducer = Filter(None,None)
        conjunctive = ["and", "and"]
        statement_results = [[1, 2], [3, 4], [5, 6]]
        reducer.filter_conjunctives(conjunctive,statement_results)
        assert(statement_results == [[]])
        

    def test_and_and_pass(self):
        reducer = Filter(None,None)
        conjunctive = ["and", "and"]
        statement_results = [[1, 2], [1, 3], [1, 4]]
        reducer.filter_conjunctives(conjunctive,statement_results)
        assert(statement_results == [[1]])
    



if __name__ == '__main__':
    unittest.main()