from pytiers.core import PitchTier, Point

def read_PitchTier(file):
    
    def findby_initial_str(strs, initial_str):
        for this_str in strs:
            if this_str.startswith(initial_str):
                return this_str
        raise Exception(f'No matching string found.')
    
    def str_to_float(_str):
        new_str = ''
        for this_str in _str:
            if this_str=='.':
                new_str = new_str + '.'
            else:
                try:
                    int(this_str)
                    new_str = new_str + this_str
                
                except ValueError:
                    pass
        return float(new_str)
    
    with open(file, 'r') as f:
        strs = f.readlines()

    pt = PitchTier(str_to_float(findby_initial_str(strs, 'xmin')),
                   str_to_float(findby_initial_str(strs, 'xmax')))
    
    point_num = str_to_float(findby_initial_str(strs, 'points:'))
    
    for idx, line in enumerate(strs):
        if 'points [' in line:
            point_index = int(str_to_float(strs[idx]))
            time = str_to_float(strs[idx+1])
            value = str_to_float(strs[idx+2])
            
            this_point = Point(time, value, point_index)
            
            pt._add_point_from_file(this_point)
       
    return pt