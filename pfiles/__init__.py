from os import makedirs
from os.path import join, abspath, curdir, dirname


class File(object):
    def __init__(self, root=None):
        """
        'root' should be an absolute path

        """
        if not root:
            self.root = abspath(curdir)
        else:
            self.root = root

        # A map of paths to an open file.
        self.files = {}

    def _mkdir_if_missing(self, path):
        try:
            makedirs(path)
        except:
            pass

    def add_or_open_file(self, path, mode):
        """
        Return the already opened file or open it and add
        to the collection of open files.

        """
        fp = join(self.root, path)

        # Make the directory if we're writing.
        if 'a' in mode or 'w' in mode:

            base = dirname(fp)
            self._mkdir_if_missing(base)

        if fp in self.files:
            return self.files[fp]

        f = open(fp, mode)
        self.files[fp] = f

        return self.files[fp]

    def closeall(self):
        """
        Close all opened files.

        """
        for fp in self.files.itervalues():
            fp.close()
