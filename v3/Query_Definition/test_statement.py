import unittest
from statement import Statement

class TestStatement(unittest.TestCase):
    '''
        Test a statements exec method
            comparison operatiors ['==','>','<','!=','>=','<=']
    '''
    
    def test_exec_date(self):
        pass
    
    def test_exec_string(self):
        test_data = ["a", "b", "ab", "z"]
        statement = Statement(None)
        # Equality
        res = statement.load("", "==", "a").exec("string", test_data)
        self.assertEqual([0], res) 
        # Break Equality
        res = statement.load("", "==", "no match").exec("string", test_data)
        self.assertEqual([], res)
        # Not Equal
        res = statement.load("", "!=", "z").exec("string", test_data)
        self.assertEqual([0, 1, 2], res)
        # Greater than
        res = statement.load("", ">", "b").exec("string", test_data)
        self.assertEqual([3], res)
        # less than
        res = statement.load("", "<", "b").exec("string", test_data)
        self.assertEqual([0, 2], res)
        # Equal or greater
        res = statement.load("", ">=", "b").exec("string", test_data)
        self.assertEqual([1, 3], res)
        # Equal or lesser
        res = statement.load("", "<=", "b").exec("string", test_data)
        self.assertEqual([0, 1, 2], res)
        pass
    
    def test_exec_int(self):
        test_data = [1, 2, 3, 4]
        statement = Statement(None)
        # Equality
        res = statement.load("", "==", 1).exec("int", test_data)
        self.assertEqual([0], res) 
        # Break Equality
        res = statement.load("", "==", 100).exec("int", test_data)
        self.assertEqual([], res)
        # Not Equal
        res = statement.load("", "!=", 4).exec("int", test_data)
        self.assertEqual([0, 1, 2], res)
        # Greater than
        res = statement.load("", ">", 2).exec("int", test_data)
        self.assertEqual([2, 3], res)
        # less than
        res = statement.load("", "<", 2).exec("int", test_data)
        self.assertEqual([0], res)
        # Equal or greater
        res = statement.load("", ">=", 2).exec("int", test_data)
        self.assertEqual([1, 2, 3], res)
        # Equal or lesser
        res = statement.load("", "<=", 2).exec("int", test_data)
        self.assertEqual([0, 1], res)
        pass
    
    def test_exec_float(self):
        test_data = [1.0, 1.00, 1.1, 1.11, 1.5]
        statement = Statement(None)
        # Equality
        res = statement.load("", "==", 1).exec("int", test_data)
        self.assertEqual([0,1], res) 
        # Break Equality
        res = statement.load("", "==", 1.9).exec("int", test_data)
        self.assertEqual([], res)
        # Not Equal
        res = statement.load("", "!=", 1.0).exec("int", test_data)
        self.assertEqual([2, 3, 4], res)
        # Greater than
        res = statement.load("", ">", 1.1).exec("int", test_data)
        self.assertEqual([3, 4], res)
        # less than
        res = statement.load("", "<", 1.1).exec("int", test_data)
        self.assertEqual([0,1], res)
        # Equal or greater
        res = statement.load("", ">=", 1.1).exec("int", test_data)
        self.assertEqual([2, 3, 4], res)
        # Equal or lesser
        res = statement.load("", "<=", 1.1).exec("int", test_data)
        self.assertEqual([0, 1, 2], res)
        pass
    
    def test_exec_empty(self):
        pass
    
    def test_exec_null(self):
        pass
    
if __name__ == '__main__':
    unittest.main()