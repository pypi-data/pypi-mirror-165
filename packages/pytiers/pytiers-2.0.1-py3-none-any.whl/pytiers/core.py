from . import by as _by
from parameters import parameters
import os

class Tier(object):
    """An abstract Tier."""
    
    __slots__ = ['__points', '__start_time', '__end_time', '__points_to_sort', '_indexed', '__original_dir']

    
    def __init__(self, start_time, end_time, name='', points=None, original_dir=''):
        self.__points = [points, []][points==None]
        self.__start_time = start_time
        self.__end_time = end_time
        self.__original_dir = original_dir
        self._indexed = True
        self.name = name
        self.tier_type = None

    def add_point(self, point):
        """Adds point to the Tier."""
        point = Point(point.time, point.value, superior_PitchTier=self)
        
        if point.time < self.start_time or point.time > self.end_time:
            raise Exception('Trying to set a point outside of time linits.')
        
        time = point.time
        
        for this_point in self.__points:
            if this_point.time==time:
                raise Exception(f'Point object with time {time} already exists.')
        
        self.__points.append(point)
        
        self.__points_to_sort = [(point.time, point) for point in self.__points]
        self.__points = [i[1] for i in sorted(self.__points_to_sort, key=lambda x: x[0])]
        
        self._indexed = False
        self._reindex()
        self._indexed = True

    def add_points(self, points):
        """Adds points to the Tier."""
        
        for point in points:
            point = Point(point.time, point.value, superior_PitchTier=self)
            
            if point.time < self.start_time or point.time > self.end_time:
                raise Exception('Trying to set a point outside of time linits.')
            
            time = point.time
            
            for this_point in self.__points:
                if this_point.time==time:
                    raise Exception(f'Point object with time {time} already exists.')
            
            self.__points.append(point)
        
        self.__points_to_sort = [(point.time, point) for point in self.__points]
        self.__points = [i[1] for i in sorted(self.__points_to_sort, key=lambda x: x[0])]
        
        self._indexed = False
        self._reindex()
        self._indexed = True
    
    def to_plot(self, start_time=None, end_time=None):
        """Plots the points of the Tier from between two time points. If the time points are not specified, start time and end time are used. To change related parameters, use parameters."""
        import seaborn as sns
        from matplotlib import pyplot as plt

        plt.figure(figsize=parameters['to_plot']['size'])
        
        if start_time==None:
            start_time = self.start_time
        if end_time==None:
            end_time = self.end_time
        
        df = self.to_dataframe()
        
        this_df = df[df.time>=start_time][df.time<=end_time]
        
        plot = sns.scatterplot(x='time', y='value', data=this_df)
        
        return plot
    
    def get_point(self, by_target, by):
        """Get Point of the Tier with chosen method. To change related parameters, use parameters."""
        
        if by.by_method not in _by.by_methods:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        if by.by_method=='by_time':
            for point in self.__points:
                if point.time==by_target:
                    return point

        elif by.by_method=='by_index':
            try:
                point = self.__points[by_target-1]
                
                return point
            except IndexError:
                pass

        elif by.by_method=='by_point':
            for point in self.__points:
                if point==by_target:
                    return point
        
        if not parameters['points']['ignore_missing_point']:
            raise Exception('Point not found.')
    
    def get_points(self, by_target, by):

        points = []
        
        if by.by_method not in _by.by_methods:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        if by.by_method=='by_point':
            for point in by_target:
                if point in self.__points:
                    points.append(point)
                elif parameters['points']['ignore_missing_point']:
                    pass
                else:
                    raise Exception('Point not found.')

        elif by.by_method=='by_index':
            for index in range(by_target[0], by_target[1]+1):
                points.append(self.get_point(index, _by.Index()))
                
        elif by.by_method=='by_time':
            for point in self.__points:
                if by_target[0] <= point.time <= by_target[1]:
                    points.append(point)
        
        return points
        
    def remove_point(self, by_target, by):
        """Remove Point of the Tier with chosen method. To change related parameters, use parameters."""
        
        if by.by_method not in _by.by_methods:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        point = self.get_point(by_target, by)
        
        if point==None:
            pass
        else:
            self.__points.remove(point)
        
        self._indexed = False
        self._reindex()
        self._indexed = True

    def remove_points(self, by_target, by):
        """Remove Point of the Tier with chosen method. To change related parameters, use parameters."""
        
        if by.by_method not in _by.by_methods:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        points = self.get_points(by_target, by)
        
        for point in points:
            if point==None:
                pass
            else:
                self.__points.remove(point)
        
        self._indexed = False
        self._reindex()
        self._indexed = True

    def shift_point_to_time(self, target_time, by_target, by):
        """Shift Point of the Tier to chosen time with chosen method. To change related parameters, use parameters."""

        if by.by_method not in _by.by_methods:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        point = self.get_point(by_target, by)
        
        if point==None:
            pass
        else:
            self.remove_point(point, _by.Point())
            
            self._indexed = False
            point.time = target_time
            self._indexed = True
            
            self.add_point(point)
    
    def batch_raise_value(self, by_target, by, value):
        """Batch raise or lower value of points of the Tier. To change related parameters, use parameters."""

        points = self.get_points(by_target, by)
        
        for point in points:
            point.value+=value
    
    def to_dataframe(self):
        """Convert the Tier to dataframe."""
        import pandas as pd
        
        df = pd.DataFrame()
        for point in self.__points:
            point_index, time, value = point.point_index, point.time, point.value
            
            df = df.append(
                {
                    'index':point_index,
                    'time':time,
                    'value':value
                }, ignore_index=True
            )
        return df
    
    def write_to_file(self, file=''):
        """Write the Tier to file. By default saves to the original directory, if any. To change related parameters, use parameters."""
        
        if file=='':
            file = f'{self.original_dir}/{self.name}.{self.tier_type}'
        
        if os.path.isfile(file):
            if not parameters['write_to_file']['replace']:
                if parameters['write_to_file']['duplicate']:
                    original_dir = os.path.dirname(file)
                    file_name = f"{os.path.basename(file).split('.')[0]} {parameters['write_to_file']['duplicated name extension']}"
                    file_extension = os.path.basename(file).split('.')[1]
                    
                    file = f'{original_dir}/{file_name}.{file_extension}'
                else:
                    raise Exception(f'{file} already exists. If you wish to replace it, set \'replace\' to True. If you wish to duplicate it, set \'duplicate\' to True.')

        with open(file, 'w') as f:
            f.writelines(
                [
                    'File type = "ooTextFile"\n',
                    f'Object class = "{self.tier_type}"\n',
                    '\n',
                    f'xmin = {self.start_time} \n',
                    f'xmax = {self.end_time} \n',
                    f'points: size = {len(self.__points)} \n'
                ]
            )
            
            for point in self.__points:
                f.writelines(
                    [
                        f'points [{point.point_index}]:\n'
                        f'\tnumber = {point.time} \n'
                        f'\tvalue = {point.value} \n' 
                    ]
                )
        
    def _add_point_from_file(self, point):
        
        point = Point(point.time, point.value, point.point_index, superior_PitchTier=self)
        
        if point.time < self.start_time or point.time > self.end_time:
            raise Exception('Trying to set a point outside of time linits.')
        
        time = point.time
        
        for this_point in self.__points:
            if this_point.time==time:
                raise Exception(f'Point object with time {time} already exists.')
        
        self.__points.append(point)
    
    def _reindex(self):
        for idx, point in enumerate(self.__points):
            point.point_index = idx+1

    @property
    def points(self):
        """Points of this Tier."""
        
        return self.__points
        
    @property
    def start_time(self):
        """Start time of this Tier."""

        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        if start_time < 0:
            raise Exception('Invalid start_time.')
        self.__start_time = start_time

    @property
    def end_time(self):
        """End time of this Tier."""

        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        if end_time < 0:
            raise Exception('Invalid end_time.')
        self.__end_time = end_time
    
    @property
    def indexed(self):
        
        return self._indexed
    
    @property
    def original_dir(self):
        
        return self.__original_dir
        
    def __getitem__(self, item):
        return self.points[item]

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name}, start_time={self.start_time}, end_time={self.end_time}, duration={self.end_time-self.start_time}, points={self.points})'

class PitchTier(Tier):
    """A PitchTier."""
    
    def __init__(self, start_time=0, end_time=0, name='', points=None, original_dir=''):
        super(PitchTier, self).__init__(start_time, end_time, name, points, original_dir)
        
        self.tier_type = 'PitchTier'

class DurationTier(Tier):
    """A DurationTier."""
    
    def __init__(self, start_time=0, end_time=0, name='', points=None, original_dir=''):
        super(DurationTier, self).__init__(start_time, end_time, name, points, original_dir)
        
        self.tier_type = 'DurationTier'

class Point(object):
    
    __slots__ = ['__time', '__value', '__point_index', '__superior_PitchTier']
    
    def __init__(self, time, value, point_index=None, superior_PitchTier=None):

        if value < 0:
            raise Exception('Invalid value.')
        if time < 0:
            raise Exception('Invalid time.')
        if point_index!=None:
            if point_index < 1:
                raise Exception('Invalid point index.')
        
        self.__time = time
        self.__value = value
        self.__point_index = point_index
        self.__superior_PitchTier = superior_PitchTier
        
    @property
    def time(self):
        """Time of this Point object."""
        
        return self.__time
    
    @time.setter
    def time(self, time):
        
        if time < 0:
            raise Exception('Invalid time.')
        self.__time = time
        
        if self.superior_PitchTier!=None:
            self.superior_PitchTier._reindex()

    @property
    def value(self):
        """Value of this Point object."""
        
        return self.__value
    
    @value.setter
    def value(self, value):
        
        if value < 0:
            raise Exception('Invalid pitch value.')
        self.__value = value
        
    @property
    def point_index(self):
        """Index of this Point object."""
        
        return self.__point_index

    @point_index.setter
    def point_index(self, point_index):
        
        if self.superior_PitchTier==None:
            if point_index < 1:
                raise Exception('Invalid point_index.')
            self.__point_index = point_index
        
        elif not self.superior_PitchTier.indexed:
            self.__point_index = point_index
        
        else:
            raise AttributeError('can\'t set attribute')
    
    @property
    def superior_PitchTier(self):
        """The PitchTier this Point object belongs to."""
        
        return self.__superior_PitchTier
                
    def __repr__(self):
        return f'{self.__class__.__name__}[{self.point_index}](time={self.time}, value={self.value})'