# KiRename

Rename a KiCad project

## License

GPL v3. See LICENSE for details.

Copyright Bob Cousins 2017

Version 0.1 <br>
*** Beta test version: use with caution ***


## Usage

```
rename_project.py [-s <source>] [-d <dest>] [-n <name> | -t <tag> ]

-s               source directory (./)
-d               destination directory (./)
-n               new name
-t               tag to add
-x               dry run, do not change any files
-h | --help      show quick help | more help
```

Note: there must be only one project in source directory.


## Typical uses

1. Rename a project foo.pro to bar.pro

>  $ rename_project -n new_name

2. Rename a project foo.pro to foo_v1.pro

> $ rename_project -t _v1

3. Rename a project foo.pro to /temp/bar.pro

> $ rename_project -d /temp -n bar

4. Rename a project foo.pro to /temp/foo_v1.pro

> $ rename_project -d /temp -t _v1

5. Rename a project foo.pro to ./YYYY-MM-DD_HH-MM-SS/foo.pro

> $ rename_project

6. Rename a project foo.pro to ./save1/foo.pro

> $ rename_project -d save1
