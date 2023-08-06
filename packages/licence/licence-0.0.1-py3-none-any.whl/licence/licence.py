#!/usr/bin/env python3
"""License texts and header strings.

Important
---------

Watch the British spelling of "licence" with regard to computer code
throughout! This avoids a name conflict with the built-in statement `license`.


How to use?
-----------

Import the module:
    >>> from licence import Licence

Load the license:
    >>> lic = Licence('GPL-3.0')

Render the license with default values:
    >>> t = lic.licence()
    >>> # `t` now contains a string with the license text, which can be written
    >>> # to a file, such as:
    >>> with open('LICENSE', 'w') as f:
    ...     f.write(t)

Render the header string to be included into each file:
    >>> t = lic.header()
If the license does not support rendering a `header`, an `AttributeError` will
be thrown!

If you want the header to be enclosed in triple quotations marks:
    >>> t = lic.header(prolog="'''", epilog="'''")

or if you want to have it as a comment:
    >>> t = lic.header(comment="# ")


How to find a license?
----------------------

Import the module:
    >>> from licence import Licence

Find the license:
    >>> lice = Licence.find(id='MIT')
    >>> # `lice` now contains a list with licenses, whose ids are 'MIT' - since
    >>> # ids are unique, there should be only one license
    >>> lice
    [<Licence('MIT')]

Find all GNU licenses:
    >>> lice = Licence.find(pypi='License :: OSI Approved :: GNU')
    >>> lice
    [<Licence('GPL-2.0+')>, <Licence('GPL-2.0')>, <Licence('AGPL-3.0')>, ...]

Get all available licenses:
    >>> lice = Licence.find()

Note, that after a license has been found, the license texts have to be loaded,
otherwise an `AttributeError` will be thrown!
    >>> lice = Licence.find(id='MIT')
    >>> lice
    [<Licence('MIT')]
    >>> lic = lice[0]
    >>> t = lic.licence()
    AttributeError: 'The MIT license' does not use 'licence'
    >>> lic.load()
    >>> t = lic.licence()

The `Licence.find()` class method takes keyword arguments and will filter the
available licenses based on these keywords, e.g. "id='MIT'" looks for all
licenses whose id is exactly 'MIT'. Other keywords are:
    - "id": Exact match
      (see https://spdx.org/licenses/)
    - "name": Exact match
      (see https://spdx.org/licenses/)
    - "pypi": Matches the start of the meta data value
      (see https://pypi.org/classifiers/)
    - "rpm": Exact match
      (see https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses)
    - "url": Exact match
Multiple keywords are supported and they are `AND`ed together.


How to add a new license?
-------------------------

All that is required is to add a license file to the `Licence.path`!

Start with a text file containing the license text. Then add the meta data at
the beginning of the file:
    # name: <full name of the license>
    # rpm: <identifier used by rpm>
    # pypi: <identifier used by PyPi>
    # url: <link to the license>

- The <full name of the license> can be looked up at https://spdx.org/licenses/
- The <identifier used by rpm> can be looked up at
  https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses
- The <identifier used by PyPi> can be looked up at
  https://pypi.org/classifiers/

If the license asks for a header to be included into each source file, add a
header section:
    # header:
    #    Copyright (C) yyyy  author name
    # header: end

If the license asks to display some information for interactive programs, add
a interactive section:
    # interactive:
    #     program  Copyright (C) yyyy  author name
    # interactive: end

Now replace the variable parts of the license with tokens starting with `$`.
These are replaced, when the text is rendered. Standard tokens are:
    - `$year`: The year (or current year, if not given)
    - `$login`: The author's login name (if not given, the login name of the
      current user as provided by the operating system will be used).
    - `$author`: The author's full name (if not given, the full name of the
      current user as provided by the operating system will be used).
    - `$email`: The author's email address (if not given, the email address of
      the current user as provided by the operating system will be used - note,
      that this is not available most of the time).
    - `$name_email`: The string "name <email>" (if not given, it will be
      calculated from `$author` and `$email`).
Any other tokens can be used as well, but they do not have a default value.

Now look back to https://spdx.org/licenses/ and make a note of the identifier.
This will be the file name and the internal 'id' of the license. So save the
file under the identifier with a suffix of '.txt' in any location mentioned in
the `Licence.path` (see next section).

Please also consider to make it available at https://codeberg.org/sph/licence


How to have your own repository of license files?
-------------------------------------------------

The license files are saved in any location mentioned in the `Licence.path`.
There is a standard path implemented in the module, but this can be modified:
    >>> # Add a new path
    >>> Licence.add_path('~/licenses')
    >>> # Remove a path
    >>> Licence.del_path('~/licenses')
    >>> # Show all paths
    >>> Licence.paths
    >>> # Clear the path - it will be empty afterwards
    >>> Licence.clear_path()

Note, that it is possible to modify `Licence.paths` directly (but you have to
use `pathlib.Path` objects!), but the above mentioned methods take care of
that and also make some sanity checks, so they are preferred.


Created on Mon Aug 29 16:09:12 2022

Copyright (C) 2022  Stephan Helma

This file is part of 'licence'.

'license' is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

'licence' is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with 'licence'. If not, see <https://www.gnu.org/licenses/>.

"""

from collections.abc import Mapping
from datetime import date
from pathlib import Path
from string import Template
import platform
if platform.system() == 'Windows':
    import ctypes
else:
    import getpass
    import pwd


# Also update the version in `pyproject.toml`!
__version__ = '0.0.1'


# __pyversion__
# https://docs.python.org/3/whatsnew/index.html
# >=3.7:
#   f-strings!
#   ordered dicts
# >=3.8:
#   f-strings with `f'{expr=}'`
#   `:=` operator
#   Positional-only parameters: `def f(a, b, /, c, d, *, e, f)`
# >=3.9:
#   Dictionary merge and update operators |, |=
#   str.removeprefix(prefix), str.removesuffix(suffix)
# >=3.10
#   Parenthesized context managers
#   Structural Pattern Matching: `match expr: case 1: ... case _: ...`
# >=3.11
#   TOML parser `import tomllib`
#   ...
__pyversion__ = '>=3.7'


class classproperty:
    """Make a class property attribute.

    The @classproperty decorator turns the decorated method into a “getter”
    for a read-only class attribute with the same name, such that the property
    can be accessed without initiating the class.

    Copyright (C) 2012  Denis Ryzhkov
    https://stackoverflow.com/questions/128573/using-property-on-classmethods#answer-13624858

    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def __set__(self, instance):
        return AttributeError("can't set attribute")


def get_year():
    """Get the current year.

    Returns
    -------
    year : int
        The current year.

    """
    return date.today().year


def get_login():
    """Get the login name for the current user.

    Returns
    -------
    login : str
        The login name of the current user.

    """
    if platform.system() == 'Windows':
        login = getpass.getuser()
    else:
        # This can handle `su` and headless logins
        login = pwd.getpwnam(getpass.getuser()).pw_name

    return login


def get_fullname():
    """Get the full user name from the information provided by the OS.

    Returns
    -------
    full_name : str
        The full name of the current user as provided by the operating system.

    """
    if platform.system() == 'Windows':
        # https://stackoverflow.com/questions/21766954/how-to-get-windows-users-full-name-in-python#answer-21766991
        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        NameDisplay = 3

        size = ctypes.pointer(ctypes.c_ulong(0))
        GetUserNameEx(NameDisplay, None, size)

        name_buffer = ctypes.create_unicode_buffer(size.contents.value)
        GetUserNameEx(NameDisplay, name_buffer, size)
        name = name_buffer.value
    else:
        # Unix systems are easier...
        gecos = pwd.getpwnam(getpass.getuser()).pw_gecos.split(',')
        name = gecos[0].strip()

    return name.strip()


def get_email():
    """Get the email address from the information provided by the OS.

    Returns
    -------
    email : str|None
        If an email address can be found, the email address; otherwise `None`.

    """
    if platform.system() == 'Windows':
        email = None
    else:
        gecos = pwd.getpwnam(getpass.getuser()).pw_gecos.split(',')
        email = gecos[-1].strip()
        if '@' not in email:
            email = None

    return email


class Licence(Mapping):

    # A list with the `pathlib.Path`'s to the directories containing the
    # license files
    _licences_paths = [Path(__file__).parent / 'licenses']

    @classproperty
    def paths(cls):
        """The list of paths, where license files can be found."""
        return cls._licences_paths

    #
    # Class
    #

    def __init__(self, id, meta_only=False):
        """Initializes the `Licence` class.

        Parameters
        ----------
        id : str
            The SPDX identifier (https://spdx.org/licenses/) of the license
            (this is the name of the license file).
        meta_only : bool, optional
            If `True`, return only the meta data, but no template or multi-line
            meta data (multi-line data is replaced with their boolean value).
            The default is `False`.

        Raises
        ------
        ValueError
            The license file '<id>.txt' does not exist in any of the
            directories specified in `Licence.paths`.
        KeyError
            A metadata key is given twice in the license file (or is a
            reserved key (currently 'file' and 'id').

        """
        self._meta = {}
        # Find license file
        for path in self.paths:
            # Cannot use `.with_suffix()`, because many file names have a
            # period in their 'id' (and hence in the file name)
            file = path / f'{id}.txt'
            if file.is_file():
                self._meta['file'] = file
                self._meta['id'] = id
                break
        else:
            raise ValueError(
                f"The license file '{file}' for license '{id}' does not exist")

        self.load(meta_only=meta_only)

    def __str__(self):
        return self._meta['name']

    def __repr__(self):
        return f'''<{self.__class__.__name__}('{self["id"]}')>'''

    #
    # Mapping
    #

    def __getitem__(self, key):
        return self._meta[key]

    def __len__(self):
        return len(self._meta)

    def __iter__(self):
        return iter(self._meta)

    #
    # All methods not defined in class are used for text rendering
    #

    def __getattr__(self, name):
        try:
            template = self._meta[name]
        except KeyError:
            if name == 'license':
                raise AttributeError(
                    "You used 'license' and probably meant 'licence' "
                    "(watch the British spelling with an 'c')")
            else:
                raise AttributeError(
                    f"'{self}' does not use '{name}'. ")
        if not isinstance(template, list):
            # All templates are lists!
            raise AttributeError(
                f"'{self}' object has no attribute '{name}'")
        return lambda **kwargs: self.text(template, **kwargs)

    #
    # Instance methods
    #

    def load(self, meta_only=False):
        """(Re)load the data from the file.

        Parameters
        ----------
        meta_only : TYPE, optional
            If `True`, return only the meta data, but no template or multi-line
            meta data (multi-line data is replaced with their boolean value).
            The default is `False`.

        Raises
        ------
        KeyError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Clear the meta data, but the 'file' and 'id' keys
        file = self._meta['file']
        id_ = self._meta['id']
        self._meta.clear()
        self._meta['file'] = file
        self._meta['id'] = id_

        # Read the license file
        with open(self._meta['file']) as f:
            licence = f.read().splitlines()

        # Get the metadata from the file
        gathering = False
        for i, line in enumerate(licence):
            if line.startswith('#'):
                # Line with metadata
                if not gathering:
                    # Not in gathering mode - we expect 'key: value'
                    key, value = line.lstrip('#').split(':', maxsplit=1)
                    key = key.strip()
                    value = value.strip()
                    if value:
                        # We got 'key: value'
                        if key in self._meta:
                            raise KeyError(
                                f"Metadata key '{key}' "
                                f"either reserved or already given. "
                                f"License file: {self._meta['file']}, "
                                f"Line: {i}")
                        self._meta[key] = value.strip()
                    else:
                        # We got 'key:' - switch to gathering mode
                        gathering = True
                        self._meta[key] = []
                else:
                    # In gathering mode - we expect line or end token
                    value = line.strip('# ')
                    if value == f'{key}: end':
                        # We got end token - switch back from gathering mode
                        gathering = False
                    else:
                        # We got line - add it to the metadata
                        self._meta[key].append(value)
            elif line.strip():
                # First non-empty line without metadata
                break

        # 'name' key is required!
        if 'name' not in self._meta:
            raise KeyError(
                f"The license file does not contain the 'name' key, "
                f"which is compulsory. "
                f"License file: {self._meta['file']}")

        if meta_only:
            # Replace multiline meta data with boolean values
            for key, value in self._meta.items():
                if isinstance(value, list):
                    self._meta[key] = bool(self._meta.get(key, False))
        else:
            # Add remainder as license template
            self._meta['licence'] = licence[i:]

    #
    # Static methods
    #

    @staticmethod
    def text(template, prolog=None, comment=None, epilog=None, **kwargs):
        """Generate the any license string

        The `string.Template` text can be ‘encapsulated’ with `prolog`,
        `comment` and `epilog` strings.

        This method can be used without loading the license file first
        (technically speaking it is a `staticmethod`).

        Parameters
        ----------
        template : list
            The list with the lines of the template text.
        prolog : str|None, optional
            A string to be put before the header, e.g. "/*" for C. If `None`,
            no prolog is added, if the empty string "", an empty line is added.
            The default is `None`.
        comment : str|None, optional
            A string to be put in front of each header line, e.g. " * " for C
            (or "# " for Python). If `None`, nothing is added before the line.
            The default is `None`.
        epilog : str|None, optional
            A string to be put after the header, e.g. " */" for C. If `None`,
            no epilog is added, if the empty string "", an empty line is added.
            The default is `None`.
        **kwargs :
            Keyword arguments with replacements for tokens in the license file.
            The most important keys are:
                `year` : optional
                    The year to be put into the copyright line.
                    The default is the current year.
                `login` : optional
                    The author's login name. The default is extracted from
                    information provided by the operating system.
                `author` : optional
                    The author's full name to be put into the copyright line.
                    The default is extracted from information provided by the
                    operating system.
                `email` : optional
                    The author's email address to be put into the copyright
                    line. Mainly used to calculate the `name_email` key: If
                    empty, no email address is inserted into the `name_email`
                    key.
                    The default is extracted from information provided by the
                    operating system (which most of the time is an empty
                    string!)
                `name_email` : optional
                    The author's full name and the email address to be put
                    into the copyright line.
                    The default is calculated from the `author` and `email`
                    keys: "author <email>" (if the `email` key is empty, no
                    email is added and `name_email` simply becomes "author").

        Returns
        -------
        str
            The rendered text.

        """
        #
        # Generate the `string.Template` using `prolog`, `comment` and `epilog`
        #

        # Add the `prolog`, `comment` and `epilog`
        t = []
        if prolog is not None:
            t.append(prolog)
        if comment is not None:
            t.extend([f'{comment}{line}' for line in template])
        else:
            t.extend(template)
        if epilog is not None:
            t.append(epilog)

        # Generate the `string.Template`
        t = Template('\n'.join(t))

        #
        # Render the template with the substitutions `kwargs` given
        #

        # Optional $year token
        if kwargs.get('year', None) is None:
            kwargs['year'] = get_year()
        # Optional $login token
        if not kwargs.get('login', None):
            kwargs['login'] = get_login()
        # Optional $author token
        # TODO: Suppport multiple authors?
        if not kwargs.get('author', None):
            kwargs['author'] = get_fullname()
        # Optional $email token
        if kwargs.get('email', None) is None:
            kwargs['email'] = get_email()
        # Optional $name_email token
        if kwargs.get('name_email', None) is None:
            if kwargs['email']:
                kwargs['name_email'] = f'{kwargs["name"]} <{kwargs["email"]}>'
            else:
                kwargs['name_email'] = kwargs['author']

        # Render and return the template
        return t.substitute(**kwargs)

    #
    # Class methods
    #

    @classmethod
    def find(cls, **kwargs):
        """Looks for licenses matching the given criteria.

        Note that a license found that way does not contain the license texts
        yet. These need to be loaded with `load()`!

        Parameters
        ----------
        **kwargs :
            The keyword arguments are the criteria used to filter the available
            licenses, e.g. `id='MIT'` looks for all licenses whose id is
            exactly 'MIT' (there should be only one license in the list,
            because the `id` should be unique).

            The main keywords are (but all keywords available in the meta data
            could be used):
            - `id` (exact match):
              See https://spdx.org/licenses/ for standard identifiers.
            - `name` (exact match):
              See https://spdx.org/licenses/ for standard names.
            - `pypi` (matches the start of the meta data value):
              See https://pypi.org/classifiers/ for valid identifiers.
            - `rpm` (exact match):
              See
              https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses
              for valid names.
            - `url` (exact match)
            - `header` (boolean)
              Filter if the license asks for a header to be included into each
              source file.
            - `interactive` (boolean)
              Filter if the license asks to display some information for
              interactive programs.

            Multiple keywords are supported and they are `AND`ed together.

        Returns
        -------
        lice : list of Licence
            A list of licenses matching the criteria.

        """
        lice = []
        # Load the metadata of all license files
        for path in cls.paths:
            for file in path.iterdir():
                if file.is_file():
                    lice.append(cls(str(file.stem), meta_only=True))
        # Filter them according to the `kwargs`
        for key, value in kwargs.items():
            if key == 'pypi':
                # The 'python' meta data looks keys starting with the given
                # string
                lice = [
                    louse
                    for louse in lice
                    if louse.get(key, '').startswith(value)]
            else:
                lice = [
                    louse
                    for louse in lice
                    if louse.get(key, None) == value]
        return lice

    @classmethod
    def clear_paths(cls):
        """Clear the list of paths to license files.

        This is a convenience function and equivalent to:
            >>> Licence.paths.clear()

        """
        cls._licences_paths.clear()

    @classmethod
    def add_path(cls, path):
        """Add a new `path` with license files (if it is not there already).

        This is a convenience function and roughly equivalent to:
            >>> Licence.paths.append(pathlib.Path(path).resolve())

        Parameters
        ----------
        path : str | pathlib.Path
            The path to add to the list of paths. A '~' will be expanded with
            the user's home directory.

        Raises
        ------
        FileNotFoundError
            The `path` is either not a directory or does not exist at all.

        """
        path = Path(path).expanduser().resolve()
        if path not in cls._licences_paths:
            if not path.is_dir():
                raise FileNotFoundError(
                    f"The directory '{path}' "
                    f"does not exist or is not a directory")
            cls._licences_paths.append(path)

    @classmethod
    def del_path(cls, path):
        """Removes a `path` from the list of paths.

        This is a convenience function and roughly equivalent to:
            >>> Licence.paths.remove(pathlib.Path(path).resolve())

        Parameters
        ----------
        path : str | pathlib.Path
            The path to be removed from the list of paths. A '~' will be
            expanded with the user's home directory.

        Raises
        ------
        AttributeError
           If the `path` is not in the list of paths.

        """
        path = Path(path).expanduser().resolve()
        # Check if `path` is in our list of paths
        cls._licences_paths.index(path)
        # Remove it
        cls._licences_paths.remove(path)


if __name__ == '__main__':
    import sys

    # Process the command line arguments
    try:
        id_ = sys.argv[1]
        licence = sys.argv[2]
        kwargs = {}
        for arg in sys.argv[3:]:
            key, value = arg.split('=', maxsplit=1)
            kwargs[key] = value
    except Exception:
        print(
            f"Usage: {sys.argv[0]} license_id licence|header|... **kwargs\n"
            f"\n"
            f"The keyword arguments are the same as for the 'text()' method.")
        sys.exit(1)

    # Get and render the `licence`
    lic = Licence(id_)
    print(getattr(lic, licence)(**kwargs))
