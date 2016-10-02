def concatenate( items ):
    result = ''
    first = True 
    for item in items:
        #Don't leave a delimiter dangling at the beginning or end
        if not first:
            result += ", " 
        else:
            first = False
        result += str(item)
        
    return result

print( concatenate(['one', 'two', 'three']) )
