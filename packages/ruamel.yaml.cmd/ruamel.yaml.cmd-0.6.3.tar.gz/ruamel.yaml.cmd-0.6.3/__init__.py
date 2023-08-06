# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.yaml.cmd',
    version_info=(0, 6, 3),
    __version__='0.6.3',
    version_timestamp='2022-09-01 06:58:05',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='commandline utility to manipulate YAML files',
    entry_points='yaml',
    license='MIT',
    since=2015,
    nested=True,
    install_requires=[
            # 'ruamel.std.argparse>=0.8',
            'configobj',
            'ruamel.yaml.convert>=0.3',
            'ruamel.yaml>=0.17.17',
            'ruamel.yaml.base',
            'lz4',
    ],
    extras_require={'configobj': ['configobj']},
    tox=dict(
        env='3',
    ),
    python_requires='>=3',
    print_allowed=True,
)

version_info = _package_data['version_info']
__version__ = _package_data['__version__']

_cligen_data = """\
# all tags start with an uppercase char and can often be shortened to three and/or one
# characters. If a tag has multiple uppercase letter, only using the uppercase letters is a
# valid shortening
# Tags used:
# !Commandlineinterface, !Cli,
# !Option, !Opt, !O
# !PreSubparserOption, !PSO
# !Help, !H
# !Argument, !Arg
# !Module   # make subparser function calls imported from module
# !Instance # module.Class: assume subparser method calls on instance of Class imported from module
# !Action # either one of the actions in subdir _action (by stem of the file) or e.g. "store_action"
# !Config YAML/INI/PON  read defaults from config file
# !AddDefaults
# !Epilog epilog text (for multiline use | )
# !NQS used on arguments, makes sure the scalar is non-quoted e.g for instance/method/function
#      call arguments, when cligen knows about what argument a keyword takes, this is not needed
!Cli 0:
- !Opt [verbose, v, !Help increase verbosity level, !Action count, const: 1, nargs: 0, default: 0]
- !Opt [indent, metavar: IND, !Help 'set indent level (default: auto)']
- !Opt [bsi, dest: block_seq_indent, metavar: BLOCK_SEQ_IND, type: int, !Help 'set block sequence indent level (default: auto)']
# - !Opt [map_indent, metavar: M, type: int, !Help 'set indent level for mappings (default: auto)']
# - !Opt [seq_indent, metavar: M, type: int, !Help 'set indent level for sequences (default: auto)']
# - !Opt [offset, dest: seq_indicator_offset, metavar: OFFSET, type: int, !Help 'set block sequence indicator offset (default: auto), make sure there is enough space in the sequence indent']
# options for YAML output 
- !Opt [flow, !Action store_true, !Help use flow-style YAML instead of block style]
- !Opt [semi, !Action store_true, !Help write block style YAML except for "leaf" mapping/dict]
- !Opt [literal, !Action store_true, !Help convert scalars with newlines to literal block style]
- !Opt [write, w, !Action store_true, !Help 'write individual .yaml files (reusing basename), instead of stdout']
- !Opt [output, o, metavar: OUT, !H 'write to file %(metavar)s instead of stdout']
- !Opt [smart-string, !Action store_true, !Help set literal block style on strings with \n otherwise plain if possible]
- !Instance ruamel.yaml.cmd.yaml_cmd.YAMLCommand
- rt:
  - !Alias round-trip
  - !Prolog round trip on YAML document, test if first or second round stabilizes document
  - !Opt [save, !Action store_true, !Help "save the rewritten data back\n    to the input file (if it doesn't exist a '.orig' backup will be made)\n    "]
  - !Opt [width, metavar: W, default: 80, type: int, !Help 'set width of output (default: %(default)s']
  - !Arg [file, nargs: +]
  - !Help test round trip on YAML document
- me:
  - !Alias merge-expand
  - !Prolog expand merges in input file to output file
  - !Opt [allow-anchors, !Action store_true, !Help allow "normal" anchors/aliases in output]
  - !Arg [file, nargs: 2]
  - !Help expand merges in input file to output file
- json:
  - !Alias from-json 
  - !Prolog convert JSON to block-style YAML
  # - !Opt [flow, !Action store_true, !Help use flow-style instead of block style]
  # - !Opt [semi, !Action store_true, !Help write block style except for "leaf" mapping/dict]
  # - !Opt [literal, !Action store_true, !Help convert scalars with newlines to literal block style]
  - !Opt [mozlz4, !Action store_true, !Help decode mozilla lz4]
  # - !Opt [write, w, !Action store_true, !Help 'write a  .yaml file, instead of stdout']
  - !Arg [file, nargs: +]
  - !Help convert JSON to block-style YAML
- ini:
  - !Alias from-ini
  - !Prolog convert .ini/config file to block YAML
  - !Opt [basename, b, !Action store_true, !Help 're-use basename of .ini file for .yaml file, instead of writing to stdout']
  - !Opt [test, !Action store_true]
  - !Arg [file]
  - !Help convert .ini/config to block YAML
- pon:
  - !Alias from-pon
  - !Prolog convert .pon config file to block YAML
  - !Arg [file, nargs: +]
  - !Help convert .pon config file to block YAML
- htmltable:
  - !Prolog |
      convert YAML to html tables. If hierarchy is two levels deep (
      sequence/mapping over sequence/mapping) this is mapped to one table
      If the hierarchy is three deep, a list of 2 deep tables is assumed, but
      any non-list/mapp second level items are considered text.
      Row level keys are inserted in first column (unless --no-row-key),
      item level keys are used as classes for the TD. 
  - !Opt [level, !Action store_true, !Help 'print # levels and exit']
  - !Opt [check]
  - !Arg [file]
  - !Help convert YAML to HTML tables
- from-html:
  - !Prolog |
      convert HTML to YAML. Tags become keys with as
      value a list. The first item in the list is a key value pair with
      key ".attribute" if attributes are available followed by tag and string
      segment items. Lists with one item are by default flattened.
  - !Opt [no-body, !Action store_true, !H drop top level html and body from HTML code segments]
  - !Opt [strip, !Action store_true, !H strip whitespace surrounding strings]
  - !Arg [file]
  - !Help convert HTML to YAML
- from-csv:
  - !Alias csv
  - !Prolog |
      convert CSV to YAML.
      By default generates a sequence of rows, with the items in a 2nd level
      sequence.
  - !Opt [mapping, m, !Action store_true, !H 'generate sequence of mappings with first line as keys']
  - !Opt [delimeter, metavar: DELIM, default: ',', !H 'field delimiter (default %(default)s)']
  - !Opt [strip, !Action store_true, !H 'strip leading & trailing spaces from strings']
  - !Opt [no-process, dest: process, !Action store_false,
          !H 'do not try to convert elements into int/float/bool/datetime']
  - !Arg [file]
  - !Help convert CSV to YAML
- from-dirs:
  - !Alias fromdirs
  - !Prolog |
      Combine multiple YAML files into one.
      Path chunks (directories) are converted to mapping entries, the YAML contents
      the value of the (last) key. If there are multiple files in one directory, the
      filenames are used as well (or specify --use-file-name).
  # - !Opt [output, o, !H 'write to file OUTPUT instead of stdout']
  - !Opt [use-file-names, !Action store_true]
  - !Opt [sequence, !Action store_true, !H 'no paths, each YAML content is made an element of a root level sequence']
  - !Arg [file, nargs: +, !H 'full path names (a/b/data.yaml)']
  - !Help combine multiple YAML files into one
- pickle:
  - !Alias [from-pickle, frompickle]
  - !Prolog |
      Load Python pickle file(s) and dump as YAML
  - !Opt [create-to-yaml, !Action store_true, !Help create a tagged to_yaml method even if available]
  - !Arg [file, nargs: '*']
  - !Help convert Python pickle file(s) to YAML
- mapping:
  - !Alias map
  # - !Opt [output, o, !Help write to file OUTPUT instead of stdout]
  - !Arg [key, !Help key of the new root-level mapping]
  - !Arg [file, !Help file with YAML content that will be value for key]
  - !Help create new YAML file with at root a mapping with key and file content
- add:
  - !Option ['parents', !Action store_true, !H create parents if necessary]
  - !Option ['item', !Action store_true, !H 'create item']
  - !Option ['key', !Action store_true, !H 'create key, even if not found in siblings of item']
  - !Option ['str', !Action store_true, !H store value as string]
  - !Option ['file', !H use FILE instead of first argument as YAML file]
  - !Option ['value', !H use FILE instead of first argument as YAML file]
  - !Option ['sep', !H set separator for splitting single element path]
  - !Arg [args, nargs: '*', !H '[file] path in yaml/path.in.yaml [value]']
  - !Help add a value to a path in the data structure loaded from YAML
  - !Prolog >
     Add a value to a path in the data structure loaded from YAML.
     Use value are resolved like in YAML, use --str if necessary
     The value is the last args token.
     The "path" in the data structure is taken from all other args,
     interpreting numerical values as indices in list/seq.

     E.g.:
         yaml add --parents --value Windows test.yaml computers os type
         yaml add --file test.yaml computers os secure false
         yaml add --str test.yaml computers.os.year 2019
- sort:
  - !Option ['file', !H use FILE instead of first argument as YAML file]
  - !Arg [args, nargs: '*', !H '[file] [path in yaml/path.in.yaml]']
  - !Prolog |
    Load the file, check if path leads to a mapping, sort by key
    and write back. No path -> work on root of data structure.
    File is not written if mapping is already in sorted order.
  - !Help sort the keys of a mapping in a YAML file
- edit:
  - !Arg [file, !H 'file to edit using $EDITOR']
  - !Help Edit a YAML document, save over orginal only when loadable 
  - !Prolog >
    Edits a copy of the file argument and only updates the file when the copy
    is loadable YAML. The copy is not removed after exiting editor if not
    parseable and used (if not older than the original file) to continue.

    Copy is named .ye.<filename>

"""  # NOQA
