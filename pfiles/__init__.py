from datetime import datetime
from os import makedirs
from os.path import join, abspath, curdir, dirname


class Pfile(object):
    def __init__(self, path, mode):
        self.f = open(path, mode)
        self.opened = datetime.utcnow()
        self.updated = None
        self.flushed = None
        self.closed = None

    def write(self, line):
        self.f.write(line)
        self.updated = datetime.utcnow()

    def flush(self):
        self.f.flush()
        self.flushed = datetime.utcnow()

    def close(self):
        self.f.close()
        self.closed = datetime.utcnow()


class File(object):
    def __init__(self, root=None, max_open_files=1000):
        """
        'root' should be an absolute path
        'max_open_files' is the max number of open files at a given time;
        we close the least used files when opening new files and we're
        at the max number of files.
        """
        if not root:
            self.root = abspath(curdir)
        else:
            self.root = root

        # A map of paths to an open file.
        self.files = {}
        self.maxf = max_open_files

    def _mkdir_if_missing(self, path):
        try:
            makedirs(path)
        except:
            pass

    def num_open(self):
        return len(self.files)

    def close_oldest(self):
        """
        Closes the oldest Pfile instances, by the Pfile.updated attribute.

        Removes the key from self.files

        """
        oldest = (None, None)

        for k, v in self.files.iteritems():
            if oldest == (None, None):
                oldest = (k, v.updated)
                continue
            if v.updated < oldest[1]:
                oldest = (k, v.updated)
        old = oldest[0]
        if old is None:
            return
        f = self.files.pop(old)
        f.close()

    def add_or_open_file(self, path, mode):
        """
        Return the already opened file or open it and add
        to the collection of open files.

        """
        fp = join(self.root, path)

        if fp in self.files:
            return self.files[fp]

        # Make the directory if we're writing.
        if 'a' in mode or 'w' in mode:

            base = dirname(fp)
            self._mkdir_if_missing(base)

        num_open = len(self.files)
        while num_open >= self.maxf:
            self.close_oldest()
            num_open -= 1

        f = Pfile(fp, mode)
        self.files[fp] = f

        return self.files[fp]

    def closeall(self):
        """
        Close all opened files.

        """
        for fp in self.files.itervalues():
            fp.flush()
            fp.close()

        self.files = {}
