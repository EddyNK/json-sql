'''
Method used during group by operation
'''
def classify(columns_to_group_by: list, matrix : list):
    '''
    classifies list by common values at specified indexes
    '''
    
    '''
    1. Find unique group values in each list and use them as the keys to a dictionary
        that will manage these groups
    '''
    groups = {}
    for row in matrix:
        val_at_index = []
        for col in columns_to_group_by:
            try:
                val_at_index.append(row[col])
            except IndexError:
                return None
        groups[tuple(val_at_index)] = []
    
    '''
    2. Loop through the list and group all memebers that match these values
    '''
    for group in groups.keys():
        for row in matrix:
            is_group_memeber = True
            i = 0
            for target_col in columns_to_group_by:
                if row[target_col] != group[i]:
                    is_group_memeber = False
                i += 1
            if is_group_memeber:
                groups[group].append(row)
    return groups
      
# classify([0,1],[[0,1],[0,2],[1,3]])