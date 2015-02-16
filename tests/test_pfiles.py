from datetime import datetime, timedelta

from mock import Mock

from pfiles import File

from StringIO import StringIO


def mock_pfile():
    m = Mock()
    m.updated = datetime.utcnow()
    m.f = StringIO()
    return m


class TestCloseOldest(object):
    def test_close_oldest(self):
        f = File('.', max_open_files=5)

        # Fake files
        f.files = {str(_): mock_pfile() for _ in xrange(5)}

        # get a pointer to the oldest object
        old_pointer = f.files['0']

        # Check that the oldest key is here
        assert '0' in f.files

        f.close_oldest()

        # Confirm that the oldest key is missing
        assert '0' not in f.files

        assert old_pointer.close.called
