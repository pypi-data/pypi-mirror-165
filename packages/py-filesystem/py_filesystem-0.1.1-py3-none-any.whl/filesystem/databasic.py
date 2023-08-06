import datetime
import errno
import os


class Base:
    """A class representing data: folder, file or link.
    This data must exist.
    """

    def __new__(cls, path, *args, **kwargs):
        if not os.path.exists(path):
            log.error(f"{os.strerror(errno.ENOENT)}: '{path}'")
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path)
        instance = object.__new__(cls)
        return instance

    def __init__(self, path):
        path = os.path.abspath(path)
        if os.name == "nt" and not path.startswith("\\\\?\\"):
            path = f"\\\\?\\{os.path.abspath(path)}"
        self._path = path
        if os.path.isdir(self._path):
            self._data_type = "folder"
        elif os.path.isfile(self._path):
            self._data_type = "file"
        elif os.path.islink(self._path):
            self._data_type = "link"
        elif os.path.ismount(self._path):
            self._data_type = 'mount'
        else:
            self._data_type = 'unknown'

    def __repr__(self):
        """
        """
        return f"cbkMgt.data.Data('{self._path}')"

    def __str__(self):
        """
        """
        return self._path

    @property
    def data_type(self):
        """return a string that represent the type of data"""
        return self._data_type

    @property
    def path(self):
        """return a string that is the full path of data"""
        return self._path

    @property
    def basename(self):
        """return a string that is the basename of the data"""
        return os.path.basename(self._path)

    @property
    def dirname(self):
        """return the dirname where the data is located"""
        return os.path.dirname(self._path)

    def is_readable(self):
        """Check if data is readable for the user"""
        return os.access(self._path, os.R_OK)

    def is_writable(self):
        """Check if data is writable for the user"""
        return os.access(self._path, os.W_OK)

    def is_executable(self):
        """Check if data is executable for the user"""
        return os.access(self._path, os.X_OK)

    @property
    def atime(self):
        """return the time at which the data was accessed"""
        return os.path.getatime(self._path)

    def atime_humanized(self, date_format='%d %b %Y %H:%M:%S'):
        """return the time at which the data was accessed

        Attr
            date_format (str):
        """
        time = self.atime
        return self._strftime(time, date_format)

    @property
    def ctime(self):
        """return the time at which the data was changed"""
        return os.path.getctime(self._path)

    def ctime_humanized(self, date_format='%d %b %Y %H:%M:%S'):
        """return the time at which the data was changed

        Attr
            date_format (str):
        """
        time = self.ctime
        return self._strftime(time, date_format)

    @property
    def mtime(self):
        """return the time at which the content of the data was changed"""
        return os.path.getmtime(self._path)

    def mtime_humanized(self, date_format='%d %b %Y %H:%M:%S'):
        """return the time at which the content of the data was changed

        Attr
            date_format (str):
        """
        time = self.mtime
        return self._strftime(time, date_format)

    @property
    def size(self):
        """return a interger that is the size of the data"""
        return os.path.getsize(self._path)

    def size_humanized(self):
        """return a interger that is the size of the data"""
        size = self.size
        return self._humanize_size(size)

    @property
    def what(self):
        return self._data_type

    # =================================================================
    # Static methods
    # =================================================================
    @staticmethod
    def _humanize_size(long_number):
        """Convert a long number in a format readable for human

        Att
            long_number (long): Number in bits to convert in Bytes
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(long_number) < 1024.0:
                return f"{long_number:3.1f}{unit}B"
            long_number /= 1024.0
        return f"{long_number:.1f}YiB"

    @staticmethod
    def _strftime(time, date_format):
        """Convert time.time in string format

        Attr
            time (float):
            date_format (str):

        """
        time = datetime.datetime.fromtimestamp(time)
        time = datetime.datetime.strftime(time, date_format)
        return time
