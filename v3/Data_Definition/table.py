import json
import csv
from math import *
from typing import OrderedDict

from Query_Definition.statement import Statement
from .table_meta import TableMetaData
from ..Helpers.converters import convert_string

class TableValues:
    '''
    table name: name of associated csv file
    columns: 
        - type: data type of the column 
        - value: all possible values found within the column and to be mapped based off of index
    key:
        - type: data type of the key column
        - name: column name
    '''

    def __init__(self, name=None):
        self.relation = OrderedDict()
        self.relation["table name"] = None
        self.relation["key"] = {"name": "index", "type": "int"}
        self.relation["columns"] = {}
        if name != None:
            self.relation["table name"] = name

    def load(self, relation: dict):
        self.relation = OrderedDict(relation)

    def load(self, file_path: str):
        data = json.load(open('location'), object_pairs_hook=OrderedDict)
        self.relation = OrderedDict(data)

    def __add_column_header(self, column_name: str, type: str):
        self.relation["columns"][column_name] = {}
        self.relation["columns"][column_name]["type"] = type
        self.relation["columns"][column_name]["values"] = []

    def get_column_names(self):
        return list(self.relation["columns"].keys())

    def get_column_values(self, name: str):
        return self.relation["columns"][name]["values"]

    def get_column_type(self, name: str):
        return self.relation["columns"][name]["type"]

    def get_column_index(self, name: str):
        return list(self.relation["columns"].keys()).index(name)

    def __add_column_value(self, column_name: str, value):
        self.relation["columns"][column_name]["values"].append(value)

    def __add_key_header(self, name, type):
        self.relation["key"]["name"] = name
        self.relation["key"]["type"] = type

    def __remove_duplicates(self):
        for name in self.get_column_names():
            # Only store unique values in each column
            unique_list = list(dict.fromkeys(
                self.relation["columns"][name]["values"]))
            self.relation["columns"][name]["values"] = unique_list

    def __sort_column_values(self):
        for name in self.get_column_names():
            # Sort each column
            self.relation["columns"][name]["values"].sort()

    def __optimize(self):
        self.__remove_duplicates()
        self.__sort_column_values()

    def export_as_json(self):
        # Saving the file to be loaded in later🤷🏾
        name = self.relation["table name"]
        with open(name + '_values' + '.json', 'w+') as fp:
            json.dump(self.relation, fp)

    def toString(self):
        return json.dumps(self.relation, sort_keys=False, indent=4)

    def load_from_csv(self, csvfile: str, TableDescription: TableMetaData):
        ''''
            Important design detail
                header with a key index of (-1), no column
                was given as an as a primary key. Instead 
                Each rows unique identifier will be its row index.
        '''
        # Set up dictionary data TableDescription information
        with open(csvfile, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            column_names = []
            pk = TableDescription.get_primary_key_column_name()
            for row in csv_reader:
                # Process csv file row by row
                if line_count == 0:
                    # current row = column header
                    column_names = row
                    ''' 
                    Set each value entries meta information
                    as provided from the TableDescription Object
                    Adds: Column name and type 
                    '''
                    for column in row:
                        if column == pk:
                            # One of the columns is pk
                            key_column_type = TableDescription.get_column_type(
                                pk)
                            self.__add_key_header(pk, key_column_type)
                        else:
                            # Place non key columns in apporpriate section
                            column_type = TableDescription.get_column_type(
                                column)
                            self.__add_column_header(column, column_type)
                else:
                    '''
                    Collect all values within a column
                    '''
                    for index, value in enumerate(row):
                        if len(value) == 0:
                            continue
                        column = column_names[index]
                        col_type = TableDescription.get_column_type(column)
                        value = convert_string(value, col_type)
                        if column == pk:
                            # map.__add_key(value) //Do this in the other module
                            continue
                        else:
                            self.__add_column_value(column, value)
                # TODO: Do this in the mapper funtion
                # No column selected as key use row based index instead
                # if pk == -1 and line_count != 0:
                #     map.__add_key(line_count)
                line_count += 1
            # Necessary Optimizations
            self.__optimize()


class TableMapping:
    '''
    Map between a CSV row values as an index into another file (relation)
    This holds no true value just an pointer to a value

    table name: name of associated csv file
    columns: 
        - type: data type of the column 
        - value: all possible values found within the column and to be mapped based off of index
    values:{ index: value }
        - index: unique row identifier
        - value: list of mapped values that correspond 
            (list index <-> column index) and (value <-> value at the indexed columns index)  
                ie. [0] -> col 0 value index 0
    '''

    def __init__(self, name=None):
        self.value_map = OrderedDict()
        self.value_map["table name"] = None
        self.value_map["map"] = {}
        if name != None:
            self.value_map["table name"] = name

    def load(self, map: dict):
        self.value_map = map

    def __add_key(self, key):
        self.value_map["map"][key] = []

    def __add_key_mapping(self, key, value):
        self.value_map["map"][key] = value

    def get_key_list(self):
        return list(self.value_map["map"].keys())

    def get_key_mapping(self, key: int):
        return self.value_map["map"][key]

    def export_as_json(self):
        # Saving the file 🤷🏾
        name = self.value_map["table name"]
        with open(name + '_map' + '.json', 'w+') as fp:
            json.dump(self.value_map, fp)

    def toString(self):
        return json.dumps(self.value_map, sort_keys=False, indent=4)

    def load_from_csv(self, csvfile: str, TableDescription: TableMetaData, relation_values: TableValues):
        '''
        For each colum index store the index of the column value 
        '''
        with open(csvfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            column_names = []
            pk = TableDescription.get_primary_key_column_name()
            for row in csv_reader:
                if line_count == 0:
                    column_names = row
                else:
                    map_values = []  # [ each index of the value in the tables given column ]
                    key = line_count  # default key value to index
                    for index, value in enumerate(row):
                        column = column_names[index]
                        col_type = TableDescription.get_column_type(column)
                        if column == pk:
                            key = convert_string(value, col_type)
                        else:
                            ''' 
                            '''
                            if not value:
                                # Blank value
                                value_index = - 1
                            else:
                                value = convert_string(value, col_type)
                                value_index = relation_values.get_column_values(
                                    column).index(value)
                            map_values.append(value_index)
                    self.__add_key_mapping(key, map_values)
                line_count += 1

class Table:
    '''
    Table
    Manages interactions with a table
    '''
    def __init__(self) -> None:
        pass

    def load_from_csv(self, csv_path: str, table_meta: dict):
        '''
        Load table column information and values as table_values
        and map the relationship between value, column and index 
        as table_map.
        '''
        self.table_meta = TableMetaData()
        self.table_meta.load(table_meta) 
        name = self.table_meta.get_table_name()
        self.table_values = TableValues(name)
        self.table_map = TableMapping(name)
        # Load csv file
        self.table_values.load_from_csv(csv_path, self.table_meta)
        self.table_map.load_from_csv(
            csv_path, self.table_meta, self.table_values)

    def __filter_rows_by_statements(self, filter_set: Statement):
        '''
        Filter each table by statement 
        results in array of passing row indexes
        '''
        passed_keys = []
        # Filter each column based off of statement object specification
        for index, statement in enumerate(filter_set["statements"]):
            # Operates on table column values 
            statement = Statement(statement)
            column_value_list = self.table_values.get_column_values(
                statement.column)
            target_column_index = self.table_values.get_column_index(
                statement.column)
            approved_column_value_indexes = set(
                statement.exec("int", column_value_list))
            keys_with_columns_that_passed = []
            # Ensure that a given key map has values that pass the filtration statement
            for index, key in enumerate(self.table_map.get_key_list()):
                key_value_map = self.table_map.get_key_mapping(key)
                if key_value_map[target_column_index] in approved_column_value_indexes:
                    keys_with_columns_that_passed.append(key)
            passed_keys.append(keys_with_columns_that_passed)
        return passed_keys

    @staticmethod
    def __filter_rows_by_conjunctives(conjunctive_list, list_to_proces):
        ''' 
        ---- Process Conjunctives ----
        Given a list containing groups of numbers this function
        will create a new lists based off of specified "and", "or"
        conjuction operations.
        # Precendence:
        # 1. 'OR' = (arr1 + arr2)
        # 2. 'AND' = (arr1 - arr2 )
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
        '''
        1.Filter map indexes based off of specified statemtents within
        each_filter set creating an allow list of map indexes.
        2.Process each resulting map index based off of conjunctives 
        '''
        # --- Process each statement in the filter set ---
        passed_keys = self.__filter_rows_by_statements(filter_set)
        self.__filter_rows_by_conjunctives(
            filter_set["conjunctives"], passed_keys)
        return passed_keys[0]
    

    def filter(self, query):
        '''
        Performs filter and conjunctive operation on each row and returns the indexes of
        rows that pass these statements
        '''
        filter_set_results = []
        for filter_set in query["filter"]["conditionals"]:
            filter_set_results.extend([self.__process_filter_set(filter_set)])

        self.__filter_rows_by_conjunctives(
            query["filter"]["conjunctives"], filter_set_results)
        return filter_set_results[0]

    def resolve_mapping(self, map: list):
        '''
        Converts a list representing map values and resolves it to the 
        Appropriate value
        '''
        converted_map = []
        for column_index, value_index in enumerate(map):
            column = self.table_values.get_column_names()[column_index]
            value = self.table_values.get_column_values(column)[value_index]
            converted_map.append(value)
        return converted_map
        
        
        
        