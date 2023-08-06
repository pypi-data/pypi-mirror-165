"""Methods for referenceing Point objects: by.time, by.index, by.point"""

class Time(object):
    """When passed to \'by\', functions to state the Point object should be referenced by time. Essentially returns a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_time'
    
    @property
    def by_method(self):
        return self.__by_method

class Index(object):
    """When passed to \'by\', functions to state the Point object should be referenced by point index. Essentially returns a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_index'
    
    @property
    def by_method(self):
        return self.__by_method

class Point(object):
    """When passed to \'by\', functions to state the Point object should be referenced by the Point per se. Essentially returns a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_point'
    
    @property
    def by_method(self):
        return self.__by_method

by_methods = [Time().by_method,
              Index().by_method,
              Point().by_method]