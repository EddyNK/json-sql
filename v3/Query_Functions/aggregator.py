import statistics

'''
    Method for aggregating a specific index value amongs 
    multiple arrays within a 2d array.
'''
def aggregate(nested_array:list, operations:dict):
    # If operations are not set return list as is
    if len(operations) < 1:
        return nested_array
    
    res = nested_array[0]
    for target_index in operations:
        '''Create a list of all values at the index of operation'''
        to_aggregate = []
        for row in nested_array:
            to_aggregate.append(row[target_index])
        ''' Resolve the operation '''
        res[target_index] = operate(to_aggregate,operations[target_index])
    return [res]
        

# NOTE: distinc?
def operate(list:list, operation:str):
    match operation:
        case 'sum':
            return sum(list)
        case 'avg': # mean
            return statistics.mean(list)
        case 'median':
            return statistics.median(list)
        case 'mode':
            return statistics.mode(list)
        case 'count':
            return len(list)
        case 'min':
            return min(list)
        case 'max':
            return max(list)
        case 'stdev':
            if len(list) < 2:
                return 0
            return statistics.stdev(list)
        case 'variance':
            if len(list) < 2:
                return 0
            return statistics.variance(list)