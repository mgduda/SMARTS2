from multiprocessing.managers import BaseManager, NamespaceProxy

class ResultClass:
    result = None
    msg = None
    directory = None

class ResultProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'run')

    def run(self):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('run')

# Our custom Shared Object manager which we will use to share each
# test instance with the scheduler
class Result(BaseManager):
    pass

Result.register('result', ResultClass, ResultProxy)
