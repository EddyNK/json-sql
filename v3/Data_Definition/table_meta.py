accepted_types = ["string", "int", "float", "date", "time"]

class TableMetaData:
    '''
    Describes the contents of a table,
        - Column type: "string", "int", "float", "date", "time",
        - Column name: "..."
    '''
    meta = {"table name": None, "primary key": -1,
              "column types": {}}
    
    def __init__(self, name=None):
        if name != None:
            self.meta["table name"] = name

    def load(self, meta):
        self.meta = meta
    
    def set_primary_key(self, column_name: str, type: str):
        self.add_column(column_name, type)
        self.meta["primary key"] = column_name
        
    def add_column(self, column_name: str, type: str):
        if type not in accepted_types:
            raise ValueError("results: status must be one of %r." % accepted_types)
        self.meta["column types"][column_name] = type

    def get_column_type(self, column_name: str):
        return self.meta["column types"][column_name]
    
    def get_primary_key_column_name(self):
        return self.meta["primary key"]
    
    def get_table_name(self):
        return self.meta["table name"]