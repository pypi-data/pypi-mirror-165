import errno
import hashlib
import logging
import magic
import os
import re
import shutil

from .databasic import Base
from .dataerror import FileMoveError, NotAFileError


class File(Base):
    """A class inheriting class Base representing a file.
    This file must exists.
    """
    def __new__(cls, path, *args, **kwargs):
        if not os.path.isfile(path):
            logging.error(f"{os.strerror(errno.ENOENT)}: '{path}'")
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path)
        instance = object.__new__(cls)
        return instance

    def __init__(self, path):
        super().__init__(path)

    def __repr__(self):
        """Display the class object."""
        return f"File('{self._path}')"

    @property
    def name(self):
        """Returns the file name without the extension"""
        return os.path.splitext(self.basename)[0]

    @property
    def extension(self):
        """returns the file extension"""
        return os.path.splitext(self.basename)[1]

    @property
    def mime(self):
        """Returns the mimetype of file"""
        return magic.from_file(self._path, mime=True)

    @property
    def md5(self):
        """Returns the value md5 of the file"""
        return self._sum_md5(self._path)

    def move(self, dst, makedirs=False, overwrite=False, o_time=False,
             suffix=False):
        """Move the file

        Attr
            dst (str): folder path where the file should be moved
            makedirs (bool): If destination path don't exists,
                it will be created. (default: False)
            overwrite (bool): Overwrites a file if already exists in
                destination folder. (default: False)
            o_time (bool): Overwrites a file if already exists in
                destination folder only if the destination file
                is older. (default: False)
            suffix (bool): Renames the file if a file has the same name
                in destination folder.
                A suffix "_<int>" is added at the end of file name.
                (default: False)

        Return
            path (str)
        """
        dst = os.path.abspath(dst)
        if os.name == "nt" and not dst.startswith("\\\\?\\"):
            dst = f"\\\\?\\{dst}"

        if os.path.exists(dst):
            if not os.path.isdir(dst):
                logging.error(f"{os.strerror(errno.ENOTDIR)}: '{dst}'")
                raise NotADirectoryError(
                    errno.ENOTDIR, os.strerror(errno.ENOTDIR), dst)
        else:
            if not makedirs:
                logging.error(f"{os.strerror(errno.ENOENT)}: '{dst}'")
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), dst)
            os.makedirs(dst)

        src = self._path
        dst = os.path.join(dst, self.basename)
        self._path = self._move(src, dst, overwrite, o_time, suffix)

        return self._path

    def rename(
        self, new_name, overwrite=False, o_time=False, suffix=False
    ):
        """Change the file basename (name + extension).

        Attr
            dst (str): folder path where the file should be moved
            makedirs (bool): If destination path don't exists,
                it will be created. (default: False)
            overwrite (bool): Overwrites a file if already exists in
                destination folder. (default: False)
            o_time (bool): Overwrites a file if already exists in
                destination folder only if the destination file
                is older. (default: False)
            suffix (bool): Renames the file if a file has the same name
                in destination folder.
                A suffix "_<int>" is added at the end of file name.
                (default: False)

        Return
            path (str)
        """
        if "/" in new_name or "\\" in new_name:
            logging.error(f"Unauthorized characters '\\', '\': '{new_name}'")
            raise ValueError(
                f"Unauthorized characters '\\', '\': '{new_name}'")

        src = self._path
        dst = os.path.join(os.path.dirname(src), new_name)
        self._path = self._move(src, dst, overwrite, o_time, suffix)

        return self._path

    def remove(self):
        """Delete the file"""
        os.remove(self._path)
        logging.info(f"{self._path} removed")
        self._path = None

    # =================================================================
    # Static methods
    # =================================================================
    @staticmethod
    def _sum_md5(target, blocksize=65536):
        """Returns the value md5 of the file.

        Attr
            target (str): full path of file
            blocksize (int): size of the segments of the file.
                Allows a faster calculation and gain of ram.
                (default: 65536)
        """
        hasher = hashlib.md5()
        with open(target, 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
        return(hasher.hexdigest())

    @staticmethod
    def _move(src, dst, overwrite=False, o_time=False, suffix=False):
        """move file source in file destination.

        Attr
            dst (str): folder path where the file should be moved
            makedirs (bool): If destination path don't exists,
                it will be created. (default: False)
            overwrite (bool): Overwrites a file if already exists in
                destination folder. (default: False)
            o_time (bool): Overwrites a file if already exists in
                destination folder only if the destination file
                is older. (default: False)
            suffix (bool): Renames the file if a file has the same name
                in destination folder.
                A suffix "_<int>" is added at the end of file name.
                (default: False)

        Return
            path (str)
        """
        if shutil._samefile(src, dst):
            return src

        if not os.path.exists(dst):
            shutil.move(src, dst)
            return dst

        if not os.path.isfile(dst):
            logging.warning(f"Not a file: '{dst}'")
            raise NotAFileError(f"Not a file: '{dst}'")

        if not overwrite and not suffix:
            logging.warning(f"Overwrite and suffix not available: '{src}'")
            raise FileMoveError(f"Overwrite and suffix not available: '{src}'")
        elif overwrite:
            if o_time:
                if os.path.getmtime(src) < os.path.getmtime(dst):
                    logging.warning(f"Older file: '{src}'")
                    raise FileMoveError(f"Older file: '{src}'")
            os.rename(src, dst)
            return dst
        elif suffix:
            #
            new_dirname, new_basename = os.path.split(dst)
            new_name, new_extension = os.path.splitext(new_basename)
            re_suffix = re.compile('^(.*_)(\\d+)$')
            re_search = re.search(re_suffix, new_name)

            if not re_search:
                index = 0
                prefix = f'{new_name}_'
            else:
                prefix, suffix = re_search.groups()
                index = int(suffix)

            while os.path.exists(dst):
                new_name = f'{prefix}{index}'
                new_basename = f'{new_name}{new_extension}'
                dst = os.path.join(new_dirname, new_basename)
                index += 1
            shutil.move(src, dst)
            return dst

