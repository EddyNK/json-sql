'''
    Helper object used during the query operation in query.py module
    - In charge of the where clause
    - 
'''
from v3.Data_Definition.table import Table
from v3.Query_Definition.statement import Statement


class Filter:
    '''
    '''
    def __init__(self, table: Table):
        self.table_column_data = table.table_values
        self.table_values_map = table.table_map

    def __filter_rows_by_statements(self, filter_set: Statement):
        '''
        Filter each row by the current value based off of Statement
        object.
        '''
        passed_keys = []
        # Filter each column based off of statement object specification
        for index, statement in enumerate(filter_set["statements"]):
            # Find ....
            statement = Statement(statement)
            column_value_list = self.table_column_data.get_column_values(
                statement.column)
            target_column_index = self.table_column_data.get_column_index(
                statement.column)
            approved_column_value_indexes = set(
                statement.exec("int", column_value_list))

            keys_with_columns_that_passed = []
            # Ensure that a given key map has values that pass the filtration statement
            for index, key in enumerate(self.table_values_map.get_key_list()):
                key_value_map = self.table_values_map.get_key_mapping(key)

                if key_value_map[target_column_index] in approved_column_value_indexes:
                    keys_with_columns_that_passed.append(index)
            passed_keys.append(keys_with_columns_that_passed)

        return passed_keys

    def __filter_rows_by_conjunctives(self, conjunctive_list, list_to_proces):
        ''' 
        ---- Process Conjunctives ----
        Takes each matching row index and creates new lists based off of 
        conjuctive operation.
        # Precendence:
        # 1. 'OR' = (arr1 + arr2)
        # 2. 'AND' = (arr1 - arr2 ) remove unique values 
        # TODO: IDK if we should do NOT
        # 3. Process 'NOT'
        '''
        conjunctive_list_copy = conjunctive_list.copy()
        while len(conjunctive_list_copy) > 0:
            try:
                # Process all 'or' conjunctives on resulting lists
                index = conjunctive_list_copy.index("or")
                # 'or' is like combining all possible results
                list_to_proces[index] = list_to_proces[index] + \
                    list_to_proces[index + 1]
                # Remove second array since its been joined with the first
                del list_to_proces[index + 1]
                # Remove duplicates
                list_to_proces[index] = list(set(list_to_proces[index]))
                # Remove 'or' from conjuction list since it has been processed
                del conjunctive_list_copy[index]
            except:
                # all 'or' conjunctives have been processed now begin processing 'and'conjunctives
                try:
                    # Process all 'and' conjunctives on resulting lists
                    index = conjunctive_list_copy.index("and")
                    # 'and' is similar to finding duplicates in 2 lists
                    list_to_proces[index] = list_to_proces[index] + \
                        list_to_proces[index + 1]
                    del list_to_proces[index + 1]
                    # Find duplicates
                    seen = set()
                    dupes = [x for x in list_to_proces[index]
                             if x in seen or seen.add(x)]
                    # Save results
                    list_to_proces[index] = dupes
                    # Remove 'and' from conjuction list since it has been processed
                    del conjunctive_list_copy[index]
                except:
                    # all 'and' and 'or' statements have been processed
                    pass

    def __process_filter_set(self, filter_set):
        # --- Process each statement in the filter set ---
        passed_keys = self.__filter_rows_by_statements(filter_set)
        self.__filter_rows_by_conjunctives(
            filter_set["conjunctives"], passed_keys)
        return passed_keys[0]

    def filter(self, query):
        "Process a queries filter statement"
        filter_set_results = []
        for filter_set in query["filter"]["filter_sets"]:
            filter_set_results.extend([self.__process_filter_set(filter_set)])

        self.__filter_rows_by_conjunctives(
            query["filter"]["conjunctives"], filter_set_results)
        return filter_set_results[0]
