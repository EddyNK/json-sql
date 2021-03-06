import profile

from Query_Functions.query import query
from v3.Data_Definition.table import Table

"""
Assumption 1: File meta data will accompany the csv
"""
# This is the header information for Caffeine.csv and test.csv
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
    "operation": "!=",
    "target": "Coffee"
}

statement2 = {
    "column": "Calories",
    "operation": "==",
    "target": 0
}

set1 = {
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

set2 = {
    "conjunctives": ["or"],
    "statements": [statement3, statement4],
}

test_query = {
    "filter": {
        "conjunctives": [],
        "conditionals": [set1]
    },
    "classify": [4],  # column index to group by
    "mutate": {
        "arithmatic1": {
            2: "val + 10",
            # 3: "log(val)"
        },
        "aggregate1": {
            # 2: "mode",
            # 3: "stdev"
        },
        # --- At this point groups are now resolved ---
        "arithmatic2": {
            1: "val + 1"
        },
        "aggregate2": {
            # 2: "sum", 
            # 3: "stdev"
        }
    },
    "sort": {
        "column": 0,
        "direction": -1
    },
    "select": 100
}

def main(csv_path: str, csv_meta: dict):
    # Create new table
    
    table = Table()
    table.load_from_csv(csv_path, csv_meta)
    print(query(table, test_query))
    # Load csv file
    return table

main("./Data/caffeine.csv", caffeine_meta)
# main("./Data/test.csv", "")


if __name__ == '__main__':
    import cProfile
    import re
    cProfile.run('main("./Data/caffeine.csv", caffeine_meta)')