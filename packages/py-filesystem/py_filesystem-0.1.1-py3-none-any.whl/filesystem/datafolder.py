import errno
import logging
import os
import shutil
import tempfile

from .databasic import Base
from .dataerror import DirMoveError, DirMoveInsideItselfError
from .datafile import File


class Folder(Base):
    """Class representing a folder.

    Args
        path (str): pathname of folder.
    """
    def __new__(cls, path, *args, **kwargs):
        if not os.path.isdir(path):
            logging.error(f"{os.strerror(errno.ENOENT)}: {path}")
            raise NotADirectoryError(
                errno.ENOTDIR, os.strerror(errno.ENOTDIR), path)
        # Removed last "/" in path name
        sep = os.path.sep + (os.path.altsep or '')
        path = path.rstrip(sep)
        instance = object.__new__(cls)
        return instance

    def __init__(self, path):
        super().__init__(path)

    def __repr__(self):
        return f"Folder('{self._path}')"

    # #################################################################
    # Method
    # #################################################################
    @property
    def size(self):
        """Get size of folder.

        Returns
            int
        """
        getsize = os.path.getsize
        join = os.sep.join
        size = 0
        for root, dirs, files in self.walk():
            size += sum(getsize(join([root, name])) for name in files)
        return size

    def size_humanized(self):
        """Returns the size of the folder in a human-readable format.

        Returns
            str

        """
        return super()._humanize_size(self.size)

    @property
    def is_empty(self):
        return len(self.listdir) == 0

    @property
    def listdir(self):
        """Returns a list of the contents of the folder.

        Returns
            list

        """
        list_dir = os.listdir(self._path)
        list_dir.sort()
        return list_dir

    @property
    def listdir_abspath(self):
        """Returns a list of the contents of the folder.
        The elements are represented with their absolute path

        Returns
            list
        """
        content = [os.path.join(self._path, name) for name in self.listdir]
        return content

    def move(
        self, new_dirname, overwrite=False, o_time=False,
        rename=False, symlinks=False
    ):
        """Moves the folder to the destination folder.

        If folders and files with the same names exist
        in the destination folder, it is possible to overwrite them
        under certain conditions.
        Symbolic links can also be recreated in the
        new folder.

        Ars
            new_dirname (str): path of the folder to move to.
            overwrite (bool): overwrites a file if it already exists in the
                            destination folder.
                            (default: false)
            o_time (bool): replace a file if it already exists in the
                           destination folder only if the
                           destination file is older.
                           (default: False)
            rename (bool): renames the file if a file has the
                           same name in the destination folder.
                           A "_<int>" suffix is ​​added at the end
                           of the file name.
                           (Default: False)
            symlinks (bool): indicates whether symbolic links should
                             be recreated.
                             (default: False)

        Returns
            str: the new folder path.

        """
        new_dirname = os.path.abspath(new_dirname)
        if os.name == "nt" and not new_dirname.startswith("\\\\?\\"):
            new_dirname = f"\\\\?\\{os.path.abspath(new_dirname)}"

        if os.path.exists(new_dirname) and not os.path.isdir(new_dirname):
            logging.error(f"Isn't a directory: '{new_dirname}'")
            raise NotADirectoryError(f"Isn't a directory: '{new_dirname}'")

        new_path = os.path.join(new_dirname, self.basename)

        self._path = self.__move_contents_dir(
            self._path, new_path, overwrite, o_time, rename, symlinks
        )

        logging.debug(f"Dir moved: '{self._path}'")
        return self._path

    def rename(
        self, new_basename, overwrite=False, o_time=False, rename=False,
        symlinks=False
    ):
        """Rename the dir.

        Ars
            new_basename (str): new folder name.
            overwrite (bool): overwrites a file if it already exists in the
                            destination folder.
                            (default: false)
            o_time (bool): replace a file if it already exists in the
                           destination folder only if the
                           destination file is older.
                           (default: False)
            rename (bool): renames the file if a file has the
                           same name in the destination folder.
                           A "_<int>" suffix is ​​added at the end
                           of the file name.
                           (Default: False)
            symlinks (bool): indicates whether symbolic links should
                             be recreated.
                             (default: False)

        Returns
            str: the new folder path.

        """
        if not isinstance(new_basename, str) or new_basename == '':
            logging.error(f"Basename can't be '{new_basename}'")
            raise ValueError(f"Basename can't be '{new_basename}'")

        if "/" in new_basename or "\\" in new_basename:
            logging.error(f"'\\' and '/' not authorized: '{new_basename}'")
            raise ValueError(f"'\\' and '/' not authorized: '{new_basename}'")

        new_path = os.path.join(self.dirname, new_basename)
        self._path = self.__move_contents_dir(
            self._path, new_path, overwrite, o_time, rename, symlinks
        )
        logging.debug(f"Dir renamed: '{self._path}'")
        return self._path

    def remove(self, ignore_errors=False, onerror=None):
        """Deletes an entire directory tree.
        If ignore_errors is true, errors resulting from failed
        deletion will be ignored; if they are false or omitted,
        these errors are handled by calling a specified handler
        by onerror or, if omitted, they trigger a
        exception.

        For more details see how the function works
        shutil.rmtree.

        Ars
            ignore_errors (bool): indicates whether to ignore
                Errors. (default: False)
            onerror (str): (default: None)
        """
        shutil.rmtree(
            self._path, ignore_errors=ignore_errors, onerror=onerror
        )
        logging.info(f"Dir deleted: '{self._path}'")
        del self._path

    def walk(self, topdown=True, onerror=None, followlinks=False):
        """refer to os.walk"""
        yield from os.walk(self._path, topdown, onerror, followlinks)

    # #################################################################
    # private method
    # #################################################################
    def __move_contents_dir(
        self, src, dst, overwrite=False, o_time=False, rename=False,
        symlinks=False
    ):
        """Moves a folder and its contents to another folder.

        Ars
            src (str): path of the folder to be moved.
            dst (str): path of the folder where to make the move.
            overwrite (bool): overwrites a file if it already exists in the
                            destination folder.
                            (default: false)
            o_time (bool): replace a file if it already exists in the
                           destination folder only if the
                           destination file is older.
                           (default: False)
            rename (bool): renames the file if a file has the
                           same name in the destination folder.
                           A "_<int>" suffix is ​​added at the end
                           of the file name.
                           (Default: False)
            symlinks (bool): indicates whether symbolic links should
                             be recreated.
                             (default: False)

        """
        if shutil._samefile(src, dst):
            # Cas d'un système insensible à la casse
            os.rename(src, dst)
            return dst

        if self._dstinsrc(dst, src):
            logging.error(f"Can't move dir inside itself: '{src}'")
            raise DirMoveInsideItselfError(
                f"Can't move dir inside itself: '{src}'"
            )

        if not os.path.exists(dst):
            os.renames(src, dst)
            logging.debug(f"path changed: '{dst}'")
            return dst

        errors = []
        if not os.path.isdir(dst):
            logging.debug(f"A file already exists: '{dst}'")
            raise FileExistError(f"A file already exists: '{dst}'")
        else:
            names = os.listdir(src)
            names.sort()
            for name in names:
                srcname = os.path.join(src, name)
                dstname = os.path.join(dst, name)
                try:
                    if symlinks and os.path.islink(srcname):
                        linkto = os.readlink(srcname)
                        os.symlink(linkto, dstname)
                        logging.debug(f"Symlink created: '{dstname}'")
                    elif os.path.isdir(dstname):
                        self.__move_contents_dir(
                            srcname, dst, overwrite, o_time, rename, symlinks
                        )
                        logging.debug(f"Dir new path: '{dstname}'")
                    elif os.path.isfile(srcname):
                        f = File(srcname)
                        f.move(dst, overwrite, o_time, rename)
                        logging.debug(f"File new path: '{dstname}'")
                except OSError as why:
                    logging.error(
                        f"Can't change path: {str(why)}"
                    )
                    errors.append((src, dst, str(why)))
                except Error as err:
                    errors.extend(err.args[0])
        if errors:
            raise DirMoveError(errors)
        else:
            return dst

    @staticmethod
    def _dstinsrc(dst, src):
        """Checks that the destination folder is not contained in
        the source folder.

        Ars
            dst (str): destination folder path.
            src (str): source folder path.
        """
        if os.name == 'nt':
            src = src.lower()
            dst = src.lower()
        src = os.path.abspath(src)
        dst = os.path.abspath(dst)
        return dst.startswith(src)
