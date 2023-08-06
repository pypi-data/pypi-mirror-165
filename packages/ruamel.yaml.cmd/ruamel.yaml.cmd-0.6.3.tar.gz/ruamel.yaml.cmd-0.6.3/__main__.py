# coding: utf-8
# flake8: noqa
# cligen: 0.2.0, dd: 2022-09-01


import argparse
import importlib
import sys
import typing

from . import __version__


class HelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, *args: typing.Any, **kw: typing.Any):
        kw['max_help_position'] = 40
        super().__init__(*args, **kw)

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        import textwrap

        paragraphs = []
        for paragraph in text.splitlines():
            paragraphs.append(textwrap.fill(paragraph, width,
                             initial_indent=indent,
                             subsequent_indent=indent))
        return '\n'.join(paragraphs)


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: typing.Any, **kw: typing.Any):
        kw['formatter_class'] = HelpFormatter
        super().__init__(*args, **kw)


class DefaultVal(str):
    def __init__(self, val: typing.Any):
        self.val = val

    def __str__(self) -> str:
        return str(self.val)


class CountAction(argparse.Action):
    """argparse action for counting up and down

    standard argparse action='count', only increments with +1, this action uses
    the value of self.const if provided, and +1 if not provided

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=CountAction, const=1,
            nargs=0)
    parser.add_argument('--quiet', '-q', action=CountAction, dest='verbose',
            const=-1, nargs=0)
    """

    def __call__(
        self,
        parser: typing.Any,
        namespace: argparse.Namespace,
        values: typing.Union[str, typing.Sequence[str], None],
        option_string: typing.Optional[str] = None,
    ) -> None:
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


def main(cmdarg: typing.Optional[typing.List[str]]=None) -> int:
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    parsers.append(ArgumentParser())
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), dest='_gl_verbose', metavar='VERBOSE', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=None, dest='_gl_indent', metavar='IND', help='set indent level (default: auto)', action='store')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)', action='store')
    parsers[-1].add_argument('--flow', default=None, dest='_gl_flow', action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=None, dest='_gl_semi', action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=None, dest='_gl_literal', action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=None, dest='_gl_write', action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=None, dest='_gl_output', metavar='OUT', help='write to file %(metavar)s instead of stdout', action='store')
    parsers[-1].add_argument('--smart-string', default=None, dest='_gl_smart_string', action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('rt', aliases=['round-trip'], description='round trip on YAML document, test if first or second round stabilizes document', help='test round trip on YAML document')
    px.set_defaults(subparser_func='rt')
    parsers.append(px)
    parsers[-1].add_argument('--save', action='store_true', help="save the rewritten data back\n    to the input file (if it doesn't exist a '.orig' backup will be made)\n    ")
    parsers[-1].add_argument('--width', default=80, metavar='W', type=int, help='set width of output (default: %(default)s')
    parsers[-1].add_argument('file', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('me', aliases=['merge-expand'], description='expand merges in input file to output file', help='expand merges in input file to output file')
    px.set_defaults(subparser_func='me')
    parsers.append(px)
    parsers[-1].add_argument('--allow-anchors', action='store_true', help='allow "normal" anchors/aliases in output')
    parsers[-1].add_argument('file', nargs=2)
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('json', aliases=['from-json'], description='convert JSON to block-style YAML', help='convert JSON to block-style YAML')
    px.set_defaults(subparser_func='json')
    parsers.append(px)
    parsers[-1].add_argument('--mozlz4', action='store_true', help='decode mozilla lz4')
    parsers[-1].add_argument('file', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('ini', aliases=['from-ini'], description='convert .ini/config file to block YAML', help='convert .ini/config to block YAML')
    px.set_defaults(subparser_func='ini')
    parsers.append(px)
    parsers[-1].add_argument('--basename', '-b', action='store_true', help='re-use basename of .ini file for .yaml file, instead of writing to stdout')
    parsers[-1].add_argument('--test', action='store_true')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('pon', aliases=['from-pon'], description='convert .pon config file to block YAML', help='convert .pon config file to block YAML')
    px.set_defaults(subparser_func='pon')
    parsers.append(px)
    parsers[-1].add_argument('file', nargs='+')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('htmltable', description='convert YAML to html tables. If hierarchy is two levels deep (\nsequence/mapping over sequence/mapping) this is mapped to one table\nIf the hierarchy is three deep, a list of 2 deep tables is assumed, but\nany non-list/mapp second level items are considered text.\nRow level keys are inserted in first column (unless --no-row-key),\nitem level keys are used as classes for the TD. \n', help='convert YAML to HTML tables')
    px.set_defaults(subparser_func='htmltable')
    parsers.append(px)
    parsers[-1].add_argument('--level', action='store_true', help='print # levels and exit')
    parsers[-1].add_argument('--check')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('from-html', description='convert HTML to YAML. Tags become keys with as\nvalue a list. The first item in the list is a key value pair with\nkey ".attribute" if attributes are available followed by tag and string\nsegment items. Lists with one item are by default flattened.\n', help='convert HTML to YAML')
    px.set_defaults(subparser_func='from_html')
    parsers.append(px)
    parsers[-1].add_argument('--no-body', action='store_true', help='drop top level html and body from HTML code segments')
    parsers[-1].add_argument('--strip', action='store_true', help='strip whitespace surrounding strings')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('from-csv', aliases=['csv'], description='convert CSV to YAML.\nBy default generates a sequence of rows, with the items in a 2nd level\nsequence.\n', help='convert CSV to YAML')
    px.set_defaults(subparser_func='from_csv')
    parsers.append(px)
    parsers[-1].add_argument('--mapping', '-m', action='store_true', help='generate sequence of mappings with first line as keys')
    parsers[-1].add_argument('--delimeter', default=",", metavar='DELIM', help='field delimiter (default %(default)s)')
    parsers[-1].add_argument('--strip', action='store_true', help='strip leading & trailing spaces from strings')
    parsers[-1].add_argument('--no-process', dest='process', action='store_false', help='do not try to convert elements into int/float/bool/datetime')
    parsers[-1].add_argument('file')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('from-dirs', aliases=['fromdirs'], description='Combine multiple YAML files into one.\nPath chunks (directories) are converted to mapping entries, the YAML contents\nthe value of the (last) key. If there are multiple files in one directory, the\nfilenames are used as well (or specify --use-file-name).\n', help='combine multiple YAML files into one')
    px.set_defaults(subparser_func='from_dirs')
    parsers.append(px)
    parsers[-1].add_argument('--use-file-names', action='store_true')
    parsers[-1].add_argument('--sequence', action='store_true', help='no paths, each YAML content is made an element of a root level sequence')
    parsers[-1].add_argument('file', nargs='+', help='full path names (a/b/data.yaml)')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('pickle', aliases=['from-pickle', 'frompickle'], description='Load Python pickle file(s) and dump as YAML\n', help='convert Python pickle file(s) to YAML')
    px.set_defaults(subparser_func='pickle')
    parsers.append(px)
    parsers[-1].add_argument('--create-to-yaml', action='store_true', help='create a tagged to_yaml method even if available')
    parsers[-1].add_argument('file', nargs='*')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('mapping', aliases=['map'], help='create new YAML file with at root a mapping with key and file content')
    px.set_defaults(subparser_func='mapping')
    parsers.append(px)
    parsers[-1].add_argument('key', help='key of the new root-level mapping')
    parsers[-1].add_argument('file', help='file with YAML content that will be value for key')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('add', help='add a value to a path in the data structure loaded from YAML', description='Add a value to a path in the data structure loaded from YAML. Use value are resolved like in YAML, use --str if necessary The value is the last args token. The "path" in the data structure is taken from all other args, interpreting numerical values as indices in list/seq.\nE.g.:\n    yaml add --parents --value Windows test.yaml computers os type\n    yaml add --file test.yaml computers os secure false\n    yaml add --str test.yaml computers.os.year 2019\n')
    px.set_defaults(subparser_func='add')
    parsers.append(px)
    parsers[-1].add_argument('--parents', action='store_true', help='create parents if necessary')
    parsers[-1].add_argument('--item', action='store_true', help='create item')
    parsers[-1].add_argument('--key', action='store_true', help='create key, even if not found in siblings of item')
    parsers[-1].add_argument('--str', action='store_true', help='store value as string')
    parsers[-1].add_argument('--file', help='use FILE instead of first argument as YAML file')
    parsers[-1].add_argument('--value', help='use FILE instead of first argument as YAML file')
    parsers[-1].add_argument('--sep', help='set separator for splitting single element path')
    parsers[-1].add_argument('args', nargs='*', help='[file] path in yaml/path.in.yaml [value]')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('sort', description='Load the file, check if path leads to a mapping, sort by key\nand write back. No path -> work on root of data structure.\nFile is not written if mapping is already in sorted order.\n', help='sort the keys of a mapping in a YAML file')
    px.set_defaults(subparser_func='sort')
    parsers.append(px)
    parsers[-1].add_argument('--file', help='use FILE instead of first argument as YAML file')
    parsers[-1].add_argument('args', nargs='*', help='[file] [path in yaml/path.in.yaml]')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    px = subp.add_parser('edit', help='Edit a YAML document, save over orginal only when loadable', description='Edits a copy of the file argument and only updates the file when the copy is loadable YAML. The copy is not removed after exiting editor if not parseable and used (if not older than the original file) to continue.\nCopy is named .ye.<filename>\n')
    px.set_defaults(subparser_func='edit')
    parsers.append(px)
    parsers[-1].add_argument('file', help='file to edit using $EDITOR')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--indent', default=DefaultVal(None), metavar='IND', help='set indent level (default: auto)')
    parsers[-1].add_argument('--bsi', dest='block_seq_indent', metavar='BLOCK_SEQ_IND', type=int, help='set block sequence indent level (default: auto)')
    parsers[-1].add_argument('--flow', default=DefaultVal(False), action='store_true', help='use flow-style YAML instead of block style')
    parsers[-1].add_argument('--semi', default=DefaultVal(False), action='store_true', help='write block style YAML except for "leaf" mapping/dict')
    parsers[-1].add_argument('--literal', default=DefaultVal(False), action='store_true', help='convert scalars with newlines to literal block style')
    parsers[-1].add_argument('--write', '-w', default=DefaultVal(False), action='store_true', help='write individual .yaml files (reusing basename), instead of stdout')
    parsers[-1].add_argument('--output', '-o', default=DefaultVal(None), metavar='OUT', help='write to file %(metavar)s instead of stdout')
    parsers[-1].add_argument('--smart-string', default=DefaultVal(False), action='store_true', help='set literal block style on strings with \\n otherwise plain if possible')
    parsers.pop()
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='ruamel.yaml.cmd', version=None, pkgs=['configobj', 'ruamel.yaml.convert', 'ruamel.yaml', 'ruamel.yaml.base', 'lz4'])
        print(__version__)
        return 0
    if '--help-all' in cmdarg[1:]:
        try:
            parsers[0].parse_args(['--help'])
        except SystemExit:
            pass
        for sc in parsers[1:]:
            print('-' * 72)
            try:
                parsers[0].parse_args([sc.prog.split()[1], '--help'])
            except SystemExit:
                pass
        sys.exit(0)
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['verbose', 'indent', 'flow', 'semi', 'literal', 'write', 'output', 'smart_string']:
        glv = getattr(args, '_gl_' + gl, None)
        if isinstance(getattr(args, gl, None), (DefaultVal, type(None))) and glv is not None:
            setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
        if isinstance(getattr(args, gl, None), DefaultVal):
            setattr(args, gl, getattr(args, gl).val)
    cls = getattr(importlib.import_module('ruamel.yaml.cmd.yaml_cmd'), 'YAMLCommand')
    obj = cls(args)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        parsers[0].parse_args('--help')
    fun = getattr(obj, funcname + '_subcommand', None)
    if fun is None:
        fun = getattr(obj, funcname)
    ret_val = fun()
    if ret_val is None:
        return 0
    if isinstance(ret_val, int):
        return ret_val
    return -1

def list_versions(pkg_name: str, version: typing.Union[str, None], pkgs: typing.Sequence[str]) -> int:
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append(
                (pkg,  getattr(importlib.import_module(pkg), '__version__', '--'))
            )
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))
    return 0


if __name__ == '__main__':
    sys.exit(main())
