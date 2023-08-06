class PitchTier(object):
    """A PitchTier."""
    
    __slots__ = ['__objects', '__start_time', '__end_time', '__objects_to_sort', '_indexed']

    
    def __init__(self, start_time, end_time):
        self.__objects = []
        self.__start_time = start_time
        self.__end_time = end_time
        self._indexed = True

    def add_point(self, point):
        """Adds point to the PitchTier."""
        point = Point(point.time, point.value, superior_PitchTier=self)
        
        if point.time < self.start_time or point.time > self.end_time:
            raise Exception('Trying to set a point outside of time linits.')
        
        time = point.time
        
        for this_point in self.__objects:
            if this_point.time==time:
                raise Exception(f'Point object with time {time} already exists.')
        
        self.__objects.append(point)
        
        self.__objects_to_sort = [(point.time, point) for point in self.__objects]
        self.__objects = [i[1] for i in sorted(self.__objects_to_sort, key=lambda x: x[0])]
        
        self._indexed = False
        self._reindex()
        self._indexed = True
    
    def to_plot(self, start_time=None, end_time=None, size=None):
        """Plots the points of the PitchTier from between two time points. If the time points are not specified, start time and end time are used."""
        import seaborn as sns
        from matplotlib import pyplot as plt

        if size!=None:
            plt.figure(figsize=size)
        
        if start_time==None:
            start_time = self.start_time
        if end_time==None:
            end_time = self.end_time
        
        df = self.to_dataframe()
        
        this_df = df[df.time>=start_time][df.time<=end_time]
        
        plot = sns.scatterplot(x='time', y='value', data=this_df)
        
        return plot
    
    def get_point(self, by_target, by, ignore_missing_point=False):
        """Get Point of the PitchTier with chosen method."""
        
        try:
            by.by_method
        except AttributeError:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        if by.by_method=='by_time':
            for point in self.__objects:
                if point.time==by_target:
                    return point

        elif by.by_method=='by_index':
            point = self.__objects[by_target-1]
            
            return point

        elif by.by_method=='by_point':
            for point in self.__objects:
                if point==by_target:
                    return point
        
        if not ignore_missing_point:
            raise Exception('Point not found.')
        
    def remove_point(self, by_target, by, ignore_missing_point=False):
        """Remove Point of the PitchTier with chosen method."""
        
        try:
            by.by_method
        except AttributeError:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        point = self.get_point(by_target, by, ignore_missing_point=ignore_missing_point)
        
        if point==None:
            pass
        else:
            self.__objects.remove(point)
        
        self._indexed = False
        self._reindex()
        self._indexed = True
    
    def shift_point_to_time(self, target_time, by_target, by, ignore_missing_point=False):
        """Remove Point of the PitchTier to chosen time with chosen method."""

        try:
            by.by_method
        except AttributeError:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        point = self.get_point(by_target, by, ignore_missing_point=ignore_missing_point)
        
        if point==None:
            pass
        else:
            self.remove_point(point, pytg.by.point)
            
            self._indexed = False
            point.time = target_time
            self._indexed = True
            
            self.add_point(point)
    
    def batch_raise_value(self, by_target, by, value, ignore_missing_point=False):
        """Batch raise or lower value of points of the PitchTier."""
        points = []
        
        try:
            by.by_method
        except AttributeError:
            raise Exception(f'Invalid by_method. Use help() to see valid methods.')
        
        if by.by_method=='by_point':
            for point in by_target:
                if point in self.__objects:
                    points.append(point)
                elif ignore_missing_point:
                    pass
                else:
                    raise Exception('Point not found.')

        elif by.by_method=='by_index':
            for index in range(by_target[0], by_target[1]):
                points.append(self.get_point(index, pytg.by.index))
                
        elif by.by_method=='by_time':
            for point in self.__objects:
                if by_target[0] <= point.time <= by_target[1]:
                    points.append(point)
        
        for point in points:
            point.value+=value
    
    def to_dataframe(self):
        """Convert the PitchTier to dataframe."""
        import pandas as pd
        
        df = pd.DataFrame()
        for point in self.__objects:
            point_index, time, value = point.point_index, point.time, point.value
            
            df = df.append(
                {
                    'index':point_index,
                    'time':time,
                    'value':value
                }, ignore_index=True
            )
        return df
    
    def write_to_file(self, file):
        """Write the PitchTier to file."""
        
        with open(file, 'w') as f:
            f.writelines(
                [
                    'File type = "ooTextFile"\n',
                    'Object class = "PitchTier"\n',
                    '\n',
                    f'xmin = {self.start_time} \n',
                    f'xmax = {self.end_time} \n',
                    f'points: size = {len(self.__objects)} \n'
                ]
            )
            
            for point in self.__objects:
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
        new_objects = []
        old_objects = self.objects.copy()
        appended = False
        
        for this_point in self.__objects:
            if this_point.time==time:
                raise Exception(f'Point object with time {time} already exists.')
        
        self.__objects.append(point)
    
    def _reindex(self):
        for idx, point in enumerate(self.__objects):
            point.point_index = idx+1

    @property
    def objects(self):
        """Points of this PitchTier."""
        
        return self.__objects
        
    @property
    def start_time(self):
        """Start time of this PitchTier."""

        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        if start_time < 0:
            raise Exception('Invalid start_time.')
        self.__start_time = start_time

    @property
    def end_time(self):
        """End time of this PitchTier."""

        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        if end_time < 0:
            raise Exception('Invalid end_time.')
        self.__end_time = end_time
    
    @property
    def indexed(self):
        return self._indexed
        
    def __getitem__(self, item):
        return self.objects[item]

    def __repr__(self):
        return f'{self.__class__.__name__}(start_time={self.start_time}, end_time={self.end_time}, duration={self.end_time-self.start_time}, points={self.objects})'
    
class Point(object):
    
    __slots__ = ['__time', '__value', '__point_index', '__superior_PitchTier']
    
    def __init__(self, time, value, point_index=None, superior_PitchTier=None):

        if value < 0:
            raise Exception('Invalid pitch value.')
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