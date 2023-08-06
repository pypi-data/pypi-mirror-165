from pytiers.core import PitchTier, DurationTier, Point
import os

def read_tier(file):
    """Read Praat\'s PitchTier and DurationTier."""
    
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
    
    tier_type = strs[1].split(' ')[-1].replace('"', '').replace('\n', '')
    original_dir = os.path.dirname(file)
    file_name = os.path.basename(file).split('.')[0]

    if tier_type=='PitchTier':
        tier = PitchTier(str_to_float(findby_initial_str(strs, 'xmin')),
                         str_to_float(findby_initial_str(strs, 'xmax')),
                         name=file_name,
                         original_dir=original_dir)
    elif tier_type=='DurationTier':
        tier = DurationTier(str_to_float(findby_initial_str(strs, 'xmin')),
                            str_to_float(findby_initial_str(strs, 'xmax')),
                            name=file_name,
                            original_dir=original_dir)
    else:
        raise Exception(f'{tier_type} is not supported.')
    
    point_num = str_to_float(findby_initial_str(strs, 'points:'))
    
    for idx, line in enumerate(strs):
        if 'points [' in line:
            point_index = int(str_to_float(strs[idx]))
            time = str_to_float(strs[idx+1])
            value = str_to_float(strs[idx+2])
            
            this_point = Point(time, value, point_index)
            
            tier._add_point_from_file(this_point)
       
    return tier