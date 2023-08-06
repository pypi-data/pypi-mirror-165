"""Temporary filesystem management implementation."""
import os
from pathlib import Path
import shutil
import sys
from typing import List, Union


class TmpFs:
    """Creates a temporary file system manager for testing.

    This plugin is a fake filesystem management implementation that relies on
    the pytest's tmp_path fixture to enable safe testing of projects that
    require disk operations and are difficult to mock.

    Alternatives:
        pyfakefs: mocks python io functions
        tempfile: creates temporary files and folders

    Attributes:
        tmp_path (Path): Path to the temporary file system.
        original_cwd (str): Original current working directory.
    """

    tree_space = '    '
    tree_branch = '│   '
    tree_tee = '├── '
    tree_last = '└── '

    def __init__(self, tmp_path: Path):
        """Initialize the temporary file system.

        Args:
            tmp_path (Path): Path to the temporary file system.
        """
        self.tmp_path: Path = tmp_path
        self.original_cwd = os.getcwd()

        sys.path.append(self._strpath(tmp_path))

    def _path(self, relative: str) -> Path:
        # returns the pathlib Path object for a relative path
        return self.tmp_path / relative

    def _strpath(self, path: Path) -> str:
        # standardize path separators to '/'
        return path.as_posix()

    def _print(self, string: str):
        # encapsulates printing to stdout
        print(string)

    def path(self, path: str) -> str:
        """Returns the absolute path to a file in the temporary file system.

        Args:
            path (str): Path to the file.

        Returns:
            str: Absolute path to the file.

        Example:
            >>> fs.path('a/b/c.txt')  # doctest: +ELLIPSIS
            '.../a/b/c.txt'
        """
        return self._strpath(self._path(path))

    def write(self, path: str, *lines: str) -> str:
        """Creates a file in the temporary file system and adds text to it.

        Args:
            path (str): Relative path to the file.
            *lines (str): Contents of the file.

        Returns:
            str: Absolute path to the file.

        Example:
            >>> _ = fs.write('b/c/d.txt', 'Hello, world!')
            >>> fs.read('b/c/d.txt')
            'Hello, world!'
        """
        p = self._path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('\n'.join(lines))
        return self._strpath(p)

    def touch(self, path: str) -> str:
        """Creates a file in the temporary file system.

        Args:
            path (str): Relative path to the file.

        Returns:
            str: Absolute path to the file.

        Example:
            >>> _ = fs.touch('c/d/e.txt')  # doctest: +ELLIPSIS
            >>> fs.ls('c/d')
            ['e.txt']
        """
        return self.write(path, '')

    def mkdir(self, path: str) -> str:
        """Creates a folder in the temporary file system.

        Args:
            path (str): Relative path to the folder.

        Returns:
            str: Absolute path to the folder.

        Example:
            >>> _ = fs.mkdir('d/e/f')
            >>> fs.ls('d/e')
            ['f']
        """
        p = self._path(path)
        p.mkdir(parents=True, exist_ok=True)
        return self._strpath(p)

    def rm(self, path: str) -> bool:
        """Removes a file or folder from the temporary file system.

        Args:
            path (str): Relative path to the file or folder.

        Returns:
            bool: True if the file or folder was removed, False otherwise.

        Example:
            >>> _ = fs.touch('e/f/g.txt')
            >>> fs.rm('e/f/g.txt')
            True
            >>> fs.ls('e/f')
            []

            >>> fs.rm('1235')
            False
        """
        p = self._path(path)
        if p.is_file():
            p.unlink()
            return True
        elif p.is_dir():
            shutil.rmtree(self._strpath(p))
            return True
        return False

    def clean(self):
        """Removes the files and folders in the temporary file system.

        Example:
            >>> _ = fs.touch('f/g/h.txt')
            >>> fs.ls('.')  # doctest: +ELLIPSIS
            [...'f'...]
            >>> fs.clean()
            >>> fs.ls('.')
            []
        """
        for node in self.ls('.'):
            self.rm(node)
        self.mkdir('.')

    def mv(self, source: str, destination: str) -> str:
        """Moves a file or a folder from one location to another in the tmpfs.

        Args:
            source (str): Relative path to the file or folder to move.
            destination (str): Relative path to the location to move the file
                or folder to.

        Returns:
            str: Absolute path to the moved file or folder.

        Example:
            >>> _ = fs.write('i/j/k.txt', 'abc')
            >>> _ = fs.mkdir('l/m')
            >>> _ = fs.mv('i/j/k.txt', 'l/m/n.txt')
            >>> fs.read('l/m/n.txt')
            'abc'
        """
        source = self.path(source)
        destination = self.path(destination)
        shutil.move(source, destination)
        return destination

    def ls(self, path: str) -> List[str]:
        """Returns a list of files and folders in the temporary file system.

        Args:
            path (str): Relative path to the folder.

        Returns:
            List[str]: Sorted list of files and folders in the specified path.

        Example:
            >>> _ = fs.touch('o/p/q.txt')
            >>> _ = fs.mkdir('o/p/s')
            >>> fs.ls('o/p')
            ['q.txt', 's']
        """
        p = self._strpath(self._path(path))
        return sorted(os.listdir(p))

    @classmethod
    def _tree(cls, dir_path: Path, prefix: str = ''):
        """Recursive tree representation generator.

        A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters

        Thanks to https://stackoverflow.com/a/59109706/13303314
        """
        contents = sorted(list(dir_path.iterdir()))
        # contents each get pointers that are ├── with a final └── :
        pointers = [cls.tree_tee] * (len(contents) - 1) + [cls.tree_last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir():  # extend the prefix and recurse:
                extension = (cls.tree_branch if pointer == cls.tree_tee
                             else cls.tree_space)
                # i.e. space because last, └── , above so no more |
                yield from cls._tree(path, prefix=(prefix + extension))

    def tree_format(self, path: str) -> str:
        r"""Returns a visual tree structure of a folder in the temporary fs.

        Args:
            path (str): Relative path to the folder.

        Returns:
            str: Visual tree structure of the specified folder.

        Example:
            >>> _ = fs.touch('r/s/t.txt')
            >>> _ = fs.mkdir('r/s/u')
            >>> fs.tree_format('r/s')
            '├── t.txt\n└── u'
        """
        p = self._path(path)
        return '\n'.join(self._tree(p))

    def tree(self, path: str):
        r"""Prints a visual tree structure of a folder in the temporary fs.

        Args:
            path (str): Relative path to the folder.

        Example:
            >>> _ = fs.touch('s/t/u.txt')
            >>> _ = fs.mkdir('s/t/v')
            >>> _ = fs.touch('s/w/x.txt')
            >>> fs.tree('s')
            ├── t
            │   ├── u.txt
            │   └── v
            └── w
                └── x.txt
        """
        self._print(self.tree_format(path))

    def read(self, path: str) -> str:
        """Returns the contents of a file in the temporary file system.

        Args:
            path (str): Relative path to the file.

        Returns:
            str: Contents of the file.

        Example:
            >>> _ = fs.write('y/z/a.txt', 'abc')
            >>> fs.read('y/z/a.txt')
            'abc'
        """
        return self._path(path).read_text()

    def cat(self, path: str) -> str:
        r"""Returns the contents of a file in the temporary file system.

        Args:
            path (str): Relative path to the file.

        Returns:
            str: Contents of the file.

        Example:
            >>> _ = fs.write('b/c/d.txt', 'abc\ndef')
            >>> fs.cat('b/c/d.txt')
            abc
            def
        """
        return self._print(self.read(path))

    def tmp_cwd(self) -> str:
        """Moves to the current working directory in the temporary file system.

        Returns:
            str: Current working directory in the temporary file system.

        Example:
            >>> import os
            >>> cwd = os.path.dirname(os.path.abspath(__file__))
            >>> os.chdir(cwd)
            >>> _ = fs.tmp_cwd()
            >>> os.getcwd() == cwd
            False
            >>> _ = fs.cwd()
            >>> os.getcwd() == cwd
            True

            Can be used with a with statement:

            >>> with fs as fs:
            ...     print(os.getcwd() == cwd)
            False
            >>> os.getcwd() == cwd
            True
        """
        self.original_cwd = os.getcwd()
        new_cwd = self.path('.')
        os.chdir(new_cwd)
        return new_cwd

    def cwd(self) -> Union[str, None]:
        """Moves to the old current working directory.

        Returns:
            str: Old current working directory.

        Example:
            >>> import os
            >>> cwd = os.path.dirname(os.path.abspath(__file__))
            >>> os.chdir(cwd)
            >>> _ = fs.tmp_cwd()
            >>> os.getcwd() == cwd
            False
            >>> _ = fs.cwd()
            >>> os.getcwd() == cwd
            True
        """
        os.chdir(self.original_cwd)
        original_cwd = self.original_cwd
        return original_cwd

    def __enter__(self):
        """Changes the current working directory to the temporary file system.

        Returns:
            TmpFs
        """
        self.tmp_cwd()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Changes the current working directory to the original one."""
        self.cwd()
