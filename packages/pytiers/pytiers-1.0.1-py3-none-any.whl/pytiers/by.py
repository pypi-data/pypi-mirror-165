"""Methods for referenceing Point objects: by.time, by.index, by.point"""

class time(object):
    """When passed to \'by\', functions to state the Point object should be referenced by time. Essentially returns a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_time'
    
    @property
    def by_method(self):
        return self.__by_method

class index(object):
    """When passed to \'by\', functions to state the Point object should be referenced by point index. Essentially returns a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_index'
    
    @property
    def by_method(self):
        return self.__by_method

class point(object):
    """When passed to \'by\', functions to state the Point object should be referenced by the Point per se. Essentially returns a string."""
    __slots__ = ['__by_method']
    def __init__(self):
        self.__by_method = 'by_point'
    
    @property
    def by_method(self):
        return self.__by_method

time = time()
index = index()
point = point()

by_methods = [time.by_method,
              index.by_method,
              point.by_method]

bys = [time.__class__.__name__,
       index.__class__.__name__,
       point.__class__.__name__]