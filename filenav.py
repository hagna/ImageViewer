from twisted.python.filepath import FilePath

def similarChild(c, newdir):
    s = sorted(newdir.children(), reverse=True, key=lambda a: a.getModificationTime())
    return FileNav(s[0])


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

    def __init__(self, fp, sortbyname=False):
        self._current = fp
        self.sortbyname = sortbyname

    def setCurrent(self, current):
        if not isinstance(current, FilePath):
            raise RuntimeError("%r is not a FilePath object" % current)
        self._current = current

    def getCurrent(self):
        return self._current

    current = property(getCurrent, setCurrent)

    def _sortall(self):
        if self.sortbyname:
            res = sorted(self.current.parent().children(), key=lambda a: (a, a.getModificationTime()))
        else:
            res = sorted(self.current.parent().children(), key=lambda a: a.getModificationTime())
        return res

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





