from twisted.python.filepath import FilePath

class FileNav(object):
    """
    Provides a next, previous, current file interface.  Just
    initialize it with a starting file and then you can do stuff like
    this:

    >>> a = FileNav(FilePath('a'))
    >>> a.next()
    >>> a.previous()
    >>> a.current()
    """

    def __init__(self, fp):
        self._current = fp

    def setCurrent(self, current):
        if not isinstance(current, FilePath):
            raise RuntimeError("%r is not a FilePath object" % current)
        self._current = current

    def getCurrent(self):
        return self._current

    current = property(getCurrent, setCurrent)

    def _sortall(self):
        return sorted(self.current.parent().children(), key=lambda a: a.getAccessTime())

    def getPrevious(self):
        all = self._sortall()
        z = all.index(self.current)
        self._current = all[z-1]
        return all[z-1]

    previous = property(getPrevious)

    def getNext(self):
        all = self._sortall()
        z = all.index(self.current)
        z = (z+1) % len(all)
        self._current = all[z]
        return all[z]

    next = property(getNext)





