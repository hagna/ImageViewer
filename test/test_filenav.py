from twisted.trial.unittest import TestCase
from filenav import FileNav
from twisted.python.filepath import FilePath
import time
# just a reminder oh yeah http://wacha.ch/wiki/sdlconsole/

class TestFileNav(TestCase):

    def setUp(self):
        self.fp = FilePath(self.mktemp())
        self.fp.makedirs()
        self.f = FileNav(self.fp)


    def test_init(self):
        """
        FileNav takes a fp as initializer
        """
        fp = FilePath(self.mktemp())
        f = FileNav(fp)
        self.assertEquals(f._current, fp)


    def test_setCurrentError(self):
        """
        If current is set to something other than a FilePath it throws
        an exception.
        """
        f = self.f
        self.assertRaises(RuntimeError, f.setCurrent, 1)


    def test_GetterSetterCurrent(self):
        """
        Getter and setter for current work
        """
        f = self.f
        z = FilePath(self.mktemp())
        f.setCurrent(z)
        self.assertEquals(f.getCurrent(), z)


    def test_property(self):
        """
        """
        f = self.f
        f._current = 1
        self.assertEquals(f.current, 1)
        f.current = FilePath(self.mktemp())
        self.assertNotEquals(f.current, 1)


    def _make_abc(self):
        a = self.fp.child('a')
        b = self.fp.child('b')
        c = self.fp.child('c')
        time.sleep(0.1)
        a.setContent('a')
        time.sleep(0.1)
        b.setContent('b')
        time.sleep(0.1)
        c.setContent('c')
        return a,b,c


    def test_prevFile_wrap(self):
        """
        FileNav.previous returns the previous file by access time and wraps.
        """
        f = self.f
        a,b,c = self._make_abc()
        f.current = c
        self.assertEquals(f.previous, a)
        self.assertEquals(f.current, a)

    def test_prevFile(self):
        """
        FileNav.previous returns the previous file by access time (newer that is).
        """
        f = self.f
        a,b,c = self._make_abc()
        f.current = b
        self.assertEquals(f.previous, c)
        self.assertEquals(f.current, c)
    

    def test_nextFile_wraps(self):
        """
        FilNav.next returns the next file in the series by access
        time.
        """
        f = self.f
        a,b,c = self._make_abc()
        f.current = a
        self.assertEquals(f.next, c)
        self.assertEquals(f.current, c)


    def test_nextFile(self):
        f = self.f
        a,b,c = self._make_abc()
        f.current = b
        self.assertEquals(f.next, a)
        self.assertEquals(f.current, a)
