import unittest

from Query_Functions.classifier import classify


class TestClassify(unittest.TestCase):
    '''
    '''
    
    def test_classify_valid_input(self):
        '''
        '''
        test_arg = [[0,1],[0,1],[0,2]]
        columns_to_classify_by = [0]
        res = classify(columns_to_classify_by,test_arg)
        assert(res == {(0,): [[0, 1], [0, 1], [0, 2]]})
    
    def test_classify_bad_index(self):
        '''
        '''
        test_arg = [[0,1],[0,1],[0,2]]
        columns_to_classify_by = [5] #<- bad col index
        res = classify(columns_to_classify_by,test_arg)
        assert(res == None)
    
    def test_classify_empty_entries(self):
        '''
        '''
        test_arg = [] #<- empty
        columns_to_classify_by = [0]
        res = classify(columns_to_classify_by,test_arg)
        assert(res == {})
        
    def test_classify_by_multiple_indexes_1(self):
        '''
        '''
        test_arg = [[0,1,2],[0,1,4],[0,0,1]]
        columns_to_classify_by = [0,1]
        res = classify(columns_to_classify_by,test_arg)
        assert(res == {(0,1): [[0,1,2], [0,1,4]], (0,0): [[0,0,1]]})
        
    def test_classify_by_multiple_indexes_2(self):
        '''
        '''
        test_arg = [[0,1,2],[0,1,4],[0,0,1]]
        columns_to_classify_by = [0,1,2]
        res = classify(columns_to_classify_by,test_arg)
        assert(res == {(0,1,2): [[0,1,2]], (0,1,4): [[0,1,4]], (0,0,1): [[0,0,1]]})
        
    def test_classify_mixed_types(self):
        '''
            Although I recommend purely numerical comparisons
            this is to demonstrate that its possible to group by a host of
            types such as strings, float and integers.
        '''
        test_arg = [["hello",1.1,2],["hello",1.1,4],["hello",0,1]]
        columns_to_classify_by = [0,1]
        res = classify(columns_to_classify_by,test_arg)
        assert(res == {("hello",1.1): [["hello",1.1,2], ["hello",1.1,4]], ("hello",0): [["hello",0,1]]})

if __name__ == '__main__':
    unittest.main()