'''
Manages Query execution by composing Table class methods
To change or modify query order of operations or high level operation
you are in the correct file.
'''
from v3.Data_Definition.table import Table
from v3.Query_Functions.classifier import classify
from v3.Query_Functions.aggregator import aggregate
from v3.Query_Functions.operations import row_arithmatic
from v3.Query_Functions.classifier import classify

def query(table :Table, Query):
        '''
        Takes a query object and executes the proper funtion 
        in the proper order to acheive it
        '''
        # [FILTER]
        filtered_row_keys = table.filter(Query)
        resulting_map = []
        for row in filtered_row_keys:
            resulting_map.append(table.table_map.get_key_mapping(row))

        # [GROUP BY]
        grouping_res = []
        group_by_columns = Query["classify"]
        groups = classify(group_by_columns, resulting_map)
        
        ''' 
            This is an extra step needed for the original implementation
            of TABLE class. This step converts each rows mapping [0,1,...]
            into the true values ["string","float",...]
        '''
        for group in groups:
            resolved_group = [table.resolve_mapping(value) for value in groups[group]]
            grouping_res.append(resolved_group) 
        
        ' Arithmatic operations intended to be applied nested arrays (groups) '
        
        # Group by: Arithmatic operation
        operation = Query["mutate"]["arithmatic1"]
        if len(operation) > 0:
            for group in grouping_res:
                for index,row_val in enumerate(group):
                    # Process arithmatic on each value
                    group[index] = row_arithmatic(row_val, operation)

        # Group by: Aggregate functions
        operation = Query["mutate"]["aggregate1"]
        if len(operation) > 0:
            for index, group in enumerate(grouping_res):
                grouping_res[index] = aggregate(group, operation)
        
        ' Round 2 of arithmatic operations on the table as a whole '
        
        # Merge groups into 1 [[unified group]]
        # after group by arithmatic and aggregate operations have been completed
        unioned_table = [row for groups in grouping_res for row in groups]
        
        # Arithmatic operation
        operation = Query["mutate"]["arithmatic2"]
        if len(operation) > 0:
            for index, row_val in enumerate(unioned_table):
                unioned_table[index] = row_arithmatic(row_val, operation)
        
        # Aggregate functions
        operation = Query["mutate"]["aggregate2"]
        if len(operation) > 0:
            unioned_table = aggregate(unioned_table, operation)
        
        
        # [SORT]
        sort_column = Query["sort"]["column"]
        sort_direction = Query["sort"]["direction"]
        if sort_direction == -1:
            unioned_table = sorted(unioned_table, key=lambda row: row[sort_column], reverse=True)
        else:
            unioned_table = sorted(unioned_table, key=lambda row: row[sort_column])
        
        
        batch_size = Query["select"]
        return [resulting_row for index,resulting_row in enumerate(unioned_table) if index < batch_size]
