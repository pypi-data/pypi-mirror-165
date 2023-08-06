# licence

If you ever wanted to add a license file automatically or wanted to add a
license header to an automatically generated file, look no further, because
that is exactly what this module does. It allows you to select from the
preconfigured licenses and you can also add your own licenses.

It does not need any external modules at all!

Another advantage is, that it is easy to add new licenses: Just prepare the
license file and save it either in the default directory (see `License.paths`)
or a directory of your own and tell `Licence` to use it. No fiddling with
Python code!


## Homepage

- https://codeberg.org/sph/licence/
- https://pypi.org/project/licence/


## A word of warning

Watch the British spelling of "licen**c**e" with regard to computer code
throughout! This avoids a name conflict with the built-in statement `license`.


## How to install?

```shell
pip3 install licence
```

or to upgrade an existing installation

```shell
pip3 install --upgrade licence
```


## How to use?

Import the module:
```python3
>>> from licence import Licence
```

Load the license:
```python3
>>> lic = Licence('GPL-3.0')
```

Render the license with default values:
```python3
>>> t = lic.licence()
>>> # `t` now contains a string with the license text, which can be written
>>> # to a file, such as:
>>> with open('LICENSE', 'w') as f:
...     f.write(t)
```

Render the header string to be included into each file:
```python3
>>> t = lic.header()
```
If the license does not support rendering a `header`, an `AttributeError` will
be thrown!

If you want the header to be enclosed in triple quotations marks:
```python3
>>> t = lic.header(prolog='"""', epilog='"""')
```

or if you want to have it as a comment:
```python3
>>> t = lic.header(comment="# ")
```


## How to find a license?

Import the module:
```python3
>>> from licence import Licence
```

Find the license:
```python3
>>> lice = Licence.find(id='MIT')
>>> # `lice` now contains a list with licenses, whose ids are 'MIT' - since
>>> # ids is unique, there should be only one license
>>> lice
[<Licence('MIT')]
```

Find all GNU licenses:
```python3
>>> lice = Licence.find(pypi='License :: OSI Approved :: GNU')
>>> lice
[<Licence('GPL-2.0+')>, <Licence('GPL-2.0')>, <Licence('AGPL-3.0')>, ...]
```

Get all available licenses:
```python3
>>> lice = Licence.find()
```

Note, that after a license has been found, the license texts have to be loaded,
otherwise an `AttributeError` will be thrown!
```python3
>>> lice = Licence.find(id='MIT')
>>> lice
[<Licence('MIT')]
>>> lic = lice[0]
>>> t = lic.licence()
AttributeError: 'The MIT license' does not use 'licence'
>>> lic.load()
>>> t = lic.licence()
```

The `Licence.find()` class method takes keyword arguments and will filter the
available licenses based on these keywords, e.g. "id='MIT'" looks for all
licenses whose id is exactly 'MIT'. Other keywords are:
- `id`: Exact match
  (see https://spdx.org/licenses/)
- `name`: Exact match
  (see https://spdx.org/licenses/)
- `pypi`: Matches the start of the meta data value
  (see https://pypi.org/classifiers/)
- `rpm`: Exact match
  (see https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses)
- `url`: Exact match

Multiple keywords are supported and they are `AND`ed together.


## How to add a new license?

All that is required is to add a license file to a location from the list
`Licence.paths`!

Start with a text file containing the license text. Then add the meta data at
the beginning of the file:
```
# name: <full name of the license>
# rpm: <identifier used by rpm>
# pypi: <identifier used by PyPi>
# url: <link to the license>
```

- The `<full name of the license>` can be looked up at https://spdx.org/licenses/
- The `<identifier used by rpm>` can be looked up at
  https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses
- The `<identifier used by PyPi>` can be looked up at
  https://pypi.org/classifiers/

If the license asks for a header to be included into each source file, add a
header section:
```
# header:
#    Copyright (C) yyyy  author name
# header: end
```
If the license asks to display some information for interactive programs, add
a interactive section:
```
# interactive:
#     program  Copyright (C) yyyy  author name
# interactive: end
```

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
the `Licence.paths` (see next section).

Please also consider to make it available at https://codeberg.org/sph/licence,
either by making a [pull request](https://codeberg.org/sph/license/pulls/)
with the new license file or open a
[new issue](https://codeberg.org/sph/license/issues/) and attach the new
license file.


## How to have your own repository of license files?

The license files are stored in any location mentioned in the `Licence.paths`.
The standard paths, such as the user and site data directories as well as this
module's path, are implemented in the module, but the list can be modified, if
the nees should arise:

- Add a new path at the beginning of the list:
```python3
>>> Licence.add_path('~/licenses')
```
- Remove a path:
```python3
>>> Licence.del_path('~/licenses')
```
- Show all paths:
```python3
>>> Licence.paths
```
- Clear the list of paths - it will be empty afterwards:
```python3
>>> Licence.clear_paths()
```
- Reset the list of paths to its default values:
```python3
>>> Licence.reset_paths()
```

Note, that it is possible to modify `Licence.paths` directly (but you have to
use `pathlib.Path` objects!), but the above mentioned methods take care of
that and also make some sanity checks, so they are preferred.


## Alternatives

- [license](https://pypi.org/project/license/): The original license module,
  but the author lost interest and does not want to hand over the project. BTW
  that project names clashes with the Python built-in `license` statement.
- [licenraptor](https://pypi.org/project/licenraptor/): Based on the original
  [license](https://pypi.org/project/license/) with one (Chinese) license
  added.

Command line utilities:
- [choosealicense-cli](https://pypi.python.org/project/choosealicense-cli>)
- [licenser](https://pypi.python.org/project/licenser>)
- [licen](https://pypi.python.org/project/licen>)
- [lice](https://pypi.python.org/project/lice>)
- [garnish](https://pypi.python.org/project/garnish>)


## API

### Class `Licence(id, meta_only=False)`

This class reads the license file and renders the license texts. It also makes
the meta data accessible. In addition it provides some useful class methods,
which can be called without initiating a class object.

#### Initialization

##### Parameters

- `id` (`str`):
  The [SPDX](https://spdx.org/licenses/) identifier of the license (this is
  the name of the license file).
- `meta_only` (`bool`, optional):
  If `True`, return only the meta data, but no template or multi-line meta
  data (multi-line data is replaced with their boolean value).
  The default is `False`.

##### Exceptions

A `ValueError` is raised, if the license file `<id>.txt` does not exist in any
of the directories specified in `Licence.paths`.

A `KeyError` is raised, if the license file states a key twice (or uses any of
the reserved keys 'file' or 'id').

#### Meta data

The class behaves like a dictionary, albeit a read-only one, so that the meta
data can be accessed with their key, e.g.
```python3
>>> l = Licence('MIT')
>>> l['name']
```
returns the full name (the `name` meta data) of the MIT license.

Basically every key given in the license file is accessed in that manner; the
main keys are:
- `id`: The [SPDX](https://spdx.org/licenses/) identifier of the license (not
  read from the license file)
- `file`: The file path to the license file (not read from the license file)
- `name`: The full [SPDX](https://spdx.org/licenses/) name of the license
- `rpm`: The identifier used by
  [RPM](https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses)
- `pypi`: The identifier used by [PyPi](https://pypi.org/classifiers/)
- `url`: The link to the license

Some licenses specify a `header` and even an `interactive` text. These are used
to be included into the every file of the project or as message for interactive
programs, respectively. They are accessed with the `header` and `interactive`
keys (and return a list of strings, were each string is one line of the text).

The license text itself is accessible with the `licence` key (and again is a
list of strings, where each string is one line of the license text).

#### Method `load(meta_only=False)

Loads the contents of the file stored in the 'file' key. This can be used to
reload the contents of the file, e.g. to read in the contents of the templates,
if the class was initialized with `meta_only=True` (which is done when finding
licenses).

The `meta_only` keyword parameter, has the same meaning as during the
initialization of the class.

#### Static method `text(template, prolog=None, comment=None, epilog=None, **kwargs)`

Generate any license string, encapsulating it between `prolog` and `epilog` and
prepending `comment` in front of every line.

The `kwargs` are used to substitute the placeholders with the same name in the
template.

Since this is a static method, it can theoretically be used without loading the
license file first.

##### Parameters

- `template` (`list`):
   The list with the lines of the template text.
- `prolog` (`str`|`None, optional):
   A string to be put before the header, e.g. "/*" for C. If `None`, no prolog
   is added, if the empty string "", an empty line is added.
   The default is `None`.
- `comment` (`str`|`None`):
   A string to be put in front of each header line, e.g. " * " for C (or "# "
   for Python). If `None`, nothing is added before the line.
   The default is `None`.
- `epilog` (`str`|`None`):
   A string to be put after the header, e.g. " */" for C. If `None`, no epilog
   is added, if the empty string "", an empty line is added.
   The default is `None`.
- `**kwargs`:
    Keyword arguments with replacements for tokens in the license file.
    The most important keys are:
    - `year` (optional):
        The year to be put into the copyright line.
        The default is the current year.
    - `login` (optional):
        The author`s login name. The default is extracted from information
        provided by the operating system.
    - `author` (optional):
        The author`s full name to be put into the copyright line.
        The default is extracted from information provided by the
        operating system.
    - `email` (optional):
        The author's email address to be put into the copyright line. Mainly
        used to calculate the `name_email` key: If empty, no email address is
        inserted into the `name_email` key.
        The default is extracted from information provided by the operating
        system (which most of the time is an empty string!)
    - `name_email` (optional):
        The author's full name and the email address to be put into the
        copyright line.
        The default is calculated from the `author` and `email` keys:
        "author <email>" (if the `email` key is empty, no email is added and
        `name_email` simply becomes "author").

#### Class method `find(**kwargs)`

Looks for licenses using the given criteria. It uses the meta data and returns
a list with all licenses matching the criteria.

The keyword arguments are the criteria used to filter the available licenses,
e.g. `id='MIT'` looks for all licenses whose id is exactly 'MIT' (there should
be only one license in the list, because the `id` should be unique). The main
keywords are (see also the section about the meta data above):
- `id` (exact match):
  See https://spdx.org/licenses/ for standard identifiers.
- `name` (exact match):
  See https://spdx.org/licenses/ for standard names.
- `pypi` (matches the start of the meta data value):
  See https://pypi.org/classifiers/ for valid identifiers.
- `rpm` (exact match):
  See https://fedoraproject.org/wiki/Licensing:Main#SoftwareLicenses for valid
  names.
- `url` (exact match)
- `header` (boolean)
  Filter if the license asks for a header to be included into each source file.
- `interactive` (boolean)
  Filter if the license asks to display some information for interactive
  programs.

Multiple keywords are supported and they are `AND`ed together.

Note that a license found that way does not contain the license texts yet. These
need to be loaded with `load()`!

#### Class methods `licence()`, `header()`, `interactive()`, …

If some data should be rendered into a license text, call that meta data with
the same arguments as the `text()` method, but without the `template`
parameter, which will be gotten from the meta data, e.g. `licence()` will
render the meta data `licence`, `header(comment='# ')` will render the meta
data `header` and adds a '# ' in front of each line.

#### `paths` manipulation

##### Class attribute `paths`

The class attribute `Licence.paths` contains the list of `pathlib.Path`s for
each directory, where license files are stored. It already contains the path
to the licenses supplied with the module.

This class attribute can be accessed without initiating the `Licence` class!

The list of paths can be manipulated with the help of the `.…_path()` class
methods (see below). Any subsequent calls of `Licence()` will then use this
modified list of paths to look for a license file.

##### Class method `add_path(path)`

Add the new directory `path` the list of paths at its end. The `path` can
either be a string or a `pathlib.Path`. The special character `~` will be
expanded with the user's home directory. It checks, if the path is an
existing directory and if it is not already in the list.

Raises `FileNotFoundError`, if the `path` does not exists.

##### Class method `del_path(path)`

Deletes the directory `path` from the list of paths. The `path` can either be
a string or a `pathlib.Path`. The special character `~` will be expanded with
the user's home directory.

Raises `AttributeError`, if the `path` is not in the list of paths.

##### Class method `clear_path(path)`

Clears the list of paths and set it to the empty list.

### Helper functions

#### Function `get_year()`

Returns the current year.

#### Function `get_login()`

Returns the login name for the current user.

#### Function `get_fullname()`

Returns the full user name from the information provided by the operating
system.

#### Function `get_email()`

Returns the email address from the information provided by the operating
system.

#### Decorator `classproperty`

Makes a class property attribute and can be used very similar to the
`@property` decorator.


## CLI

The file can be called from the command line:
```shell
python3 id licence|header|... **kwargs
```

where `id` is the license identifier (as in the class initialization),
`licence|header|...` the part of the license to be rendered and the keyword
arguments `**kwargs` the same as for the `text()` method (without the
`template` parameter).
