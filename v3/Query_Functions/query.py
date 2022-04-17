'''
Manages the processing of an sql like "where" statement
'''
from Query_Functions.classifier import classify
from Main import main
from v3.Data_Definition.table import Table
from Query_Functions.filter import Filter

caffeine_meta = {
    "table name": "Caffeine.csv", 
    "primary key": -1,
    "column types": {
        "drink": "string",
        "Volume (ml)": "float",
        "Calories": "int",
        "Caffeine (mg)": "int",
        "type": "string"
    }
}

# (s1 and s2) and (s3 and s4)

statement1 = {
        "column": "type",
        "operation": "==",
        "target": "Coffee"
    }

statement2 = {
        "column": "Calories",
        "operation": "==",
        "target": 0
    }

filter_set1 = {
    "conjunctives": [],
    "statements": [statement1],  
}

statement3 = {
        "column": "drink",
        "operation": "==",
        "target": "Costa Coffee"
    }

statement4 = {
        "column": "drink",
        "operation": "==",
        "target": "Hell Energy Coffee"
    }

filter_set2 = {
    "conjunctives": ["or"],
    "statements": [statement3, statement4],  
}

test_query = { 
    "filter":{
        "conjunctives": [],
        "filter_sets": [filter_set1]
    },
    "group by":[3]
}

def query(table: Table, Query):
    '''
    Takes a query object and executes order of operation to acheive it
    '''
    # [FILTER]
    table = main("./Data/caffeine.csv", caffeine_meta)
    filterObject = Filter(table)
    resulting_row_id = filterObject.filter(Query)
    resulting_map = []
    for row in resulting_row_id:
        if(row == 0):
            continue
        resulting_map.append(table.table_map.get_key_mapping(row))
    # print(resulting_map)
    # [GROUP BY]
    group_by_columns = test_query["group by"]
    groups = classify(group_by_columns, resulting_map)
    # print(groups)
    for group in groups:
        print("----------")
        print(group)
        for value in groups[group]:
            print(table.convert_map_to_value(value))
            
query(None, test_query)
