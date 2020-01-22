from multiprocessing.managers import BaseManager, NamespaceProxy


""" The Result Class, Result Managers and Result Proxy

The ResultClass, Result Manager (Class Result) and the Result Proxy (ResultProxy)
all work in unison to communicate results between the TestManager and individual
tests.

Individual tests are spawned as child process, thus some kind of interprocess
communication needs to occur between the TestManager (Parent) and the test
(child) to communicate whether or not they pass or fail.

https://docs.python.org/3.8/library/multiprocessing.html#managers

Python's multiprocessing.Managers (see above) provide a method for syncing
different Python objects across multiple processes.

ResultClass is the base class in which each test will 'interact' with. The
Result class acts as the manager (or server) of the ResultClass, and finally,
the ResultProxy is the object that referes to a shared object, which is called
the referent. In SMARTS case, our proxy object(s) are used by individual tests,
while the referent of the test proxies live with the TestManager.

The ResultProxy class is needed to enable the passed ResultClass to behave like
an object (i.e. we can set and add new attributes).
"""

class ResultClass:
    """ """
    result = None
    msg = None
    directory = None

class Result(BaseManager):
    pass

class ResultProxy(NamespaceProxy):
    pass

Result.register('result', ResultClass, ResultProxy)



""" Reporter Specific Functions """

def initialize_reporter(reporterType):
    """ Return an initialized reporter - Currently not used """
    pass

class BaseReporter:
    def add_result(result):
        """ Add a result to a reporter instance - currently not used"""
        pass

    def genereate_report():
        """ Generate a specified report """
        pass
