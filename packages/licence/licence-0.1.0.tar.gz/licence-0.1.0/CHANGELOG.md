# Dev-branch

## Release highlights
## Added
## Changed
## Deprecated
## Removed
## Fixed
## Security
## Known bugs
## How to update


# v0.1.0 (2022-09-01)

## Release highlights

- Adds user and site data directories to the list of paths.
- The list of paths can be reset to its default values.
- `add_path(path)` will add the path to the beginning of the list of paths, so
  that the new path will take precedence over all others.

## Added

- API:
    - Adds user data dir and site data dirs to the list of paths. (Stephan
      Helma)
    - Adds class method `reset_paths()` to reset the list of paths to its
      default values. (Stephan Helma)

## Changed

- API:
    - Changes `add_path(path)` to insert the `path` at the start of the list.
      (Stephan Helma)

## Fixed

- Documentation:
    - Corrects the documentation `Licence.path` → `Licence.paths`. (Stephan
      Helma)
    - Corrects the documentation `Licence.clear_path()` →
      `Licence.clear_paths()`. (Stephan Helma)
    - Clarifies documentation about `Licence.paths` manipulation. (Stephan
      Helma)


# v0.0.2 (2022-08-31)

## Release highlights

- Licenses:
    - A 'NoLicense' has been added. It can be accessed either the traditional
      way with the license name `Licence('NoLicense')` or with `None`:
      `Licence(None)`.
    - The European Union Public License 1.2' (EUPL-1.2) has been added.

## Added

- Licenses:
    - Adds a 'NoLicense', which can also be accessed with `Licence(None)`.
      (Stephan Helma)
    - Adds the EUPL-1.2 license. (Stephan Helma)


# v0.0.1 (2022-08-31)

## Release highlights

- Initial commit. (Stephan Helma)
