def convert_string(string,type):
    """
    Convert a string to a defined type
    """
    match type:
        case "int":
           return int(string)
        case "float":
            return float(string)
        case "string":
            return string
