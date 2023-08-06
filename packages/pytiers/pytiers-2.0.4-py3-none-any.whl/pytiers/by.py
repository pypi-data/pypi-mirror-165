"""Methods for referenceing Point objects: by.time, by.index, by.point\nUsage example:\n pytiers.get_point(1, by.Index())\n returns the point in the Tier object with the #1 index."""

class Time(object):
    """When passed to \'by\', function to state the Point object should be referenced by time. Essentially return a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_time'
    
    @property
    def by_method(self):
        return self.__by_method

class Index(object):
    """When passed to \'by\', function to state the Point object should be referenced by point index. Essentially return a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_index'
    
    @property
    def by_method(self):
        return self.__by_method

class Point(object):
    """When passed to \'by\', function to state the Point object should be referenced by the Point per se. Essentially return a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_point'
    
    @property
    def by_method(self):
        return self.__by_method

by_methods = [Time().by_method,
              Index().by_method,
              Point().by_method]