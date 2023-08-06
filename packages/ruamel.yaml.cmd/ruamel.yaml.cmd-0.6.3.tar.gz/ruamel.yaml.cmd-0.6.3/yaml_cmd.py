# coding: utf-8

"""
this is the source for the yaml utility
"""

import sys
import _ast
import ast
import os
import datetime
import contextlib
import subprocess
import io
import lz4.block
import textwrap
from pathlib import Path
import typing

import ruamel.yaml
import ruamel.yaml.base
from ruamel.yaml import YAML
from ruamel.yaml.compat import ordereddict, DBG_EVENT, DBG_NODE  # DBG_TOKEN
from ruamel.yaml.scalarstring import walk_tree

from ruamel.yaml.util import configobj_walker

from .simpleresolver import SimpleResolver


def yaml_to_html2(code):
    buf = io.StringIO()
    buf.write('<HTML>\n')
    buf.write('<HEAD>\n')
    buf.write('</HEAD>\n')
    buf.write('<BODY>\n')
    buf.write('<TABLE>\n')
    if isinstance(code, dict):
        for k in code:
            buf.write('  <TR>\n')
            for x in [k] + code[k]:
                buf.write('    <TD>{0}</TD>\n'.format(x))
            buf.write('  </TR>\n')
            # yaml = YAML()
            # data
    elif isinstance(code, list):
        # assume list of (k, v) pairs
        order = []
        for item in code:
            if not order:
                buf.write('  <TR>\n')
                for k in item:
                    order.append(k)
                    buf.write('    <TD>{0}</TD>\n'.format(k))
                buf.write('  </TR>\n')
            buf.write('  <TR>\n')
            for k in order:
                buf.write('    <TD>{0}</TD>\n'.format(item.get(k)))
            buf.write('  </TR>\n')

    buf.write('<TABLE>\n')
    buf.write('</BODY>\n')
    buf.write('</HTML>\n')
    return buf.getvalue()


def yaml_to_html(code, level):
    if level == 2:
        return yaml_to_html2(code)
    # elif level == 3:
    #     return yaml_to_html3(code)
    raise NotImplementedError


def commentify(data, sort_dict=True):
    """convert any normal dict and list in data to CommentedMap resp CommentedSeq
    and handle **their** values recursively
    """
    from ruamel.yaml.comments import CommentedMap, CommentedSeq

    def conv(d):
        if isinstance(d, (CommentedMap, CommentedSeq)):
            return d
        if isinstance(d, dict):
            ret_val = CommentedMap()
            if sort_dict and not isinstance(d, ordereddict):
                for key in sorted(d):
                    ret_val[key] = conv(d[key])
            else:
                for key in d:
                    ret_val[key] = conv(d[key])
            return ret_val
        if isinstance(d, list):
            ret_val = CommentedSeq()
            for k in d:
                ret_val.append(conv(k))
            return ret_val
        return d

    return conv(data)


def load_yaml_guess_and_set_indent(stream_or_path, yaml):
    """guess the block mapping and sequence indent, as well as offset of YAML stream/string

    returns loaded data and sets .indent() on yaml
    - offset is the number of spaces before a dash relative to previous indent
    - if there are no block sequences, indent is same as for mappings (with offset 0) and vv.
    """
    # load a YAML document, guess the indentation, if you use TABs you are on your own
    def leading_spaces(line):
        idx = 0
        while idx < len(line) and line[idx] == ' ':
            idx += 1
        return idx

    assert isinstance(yaml, YAML)
    if isinstance(stream_or_path, str):
        yaml_str = stream_or_path
    elif isinstance(stream_or_path, bytes):
        # most likely, but the Reader checks BOM for this
        yaml_str = stream_or_path.decode('utf-8')
    elif hasattr(stream_or_path, 'open'):
        yaml_str = stream_or_path.read_text()
    else:
        yaml_str = stream_or_path.read()
    map_indent = None
    seq_indent = None
    # indent = None  # default if not found for some reason
    offset = None
    prev_line_key_only = None
    key_indent = 0
    for line in yaml_str.splitlines():
        rline = line.rstrip()
        lline = rline.lstrip()
        if seq_indent is None and lline.startswith('- '):
            l_s = leading_spaces(line)
            offset = l_s - key_indent
            idx = l_s + 1
            while line[idx] == ' ':  # this will end as we rstripped
                idx += 1
            if line[idx] == '#':  # comment after -
                continue
            seq_indent = idx - key_indent
            break
        if map_indent is None and prev_line_key_only is not None and rline:
            idx = 0
            while line[idx] in ' -':
                idx += 1
            if idx > prev_line_key_only:
                map_indent = idx - prev_line_key_only
        if rline.endswith(':'):
            key_indent = leading_spaces(line)
            idx = 0
            while line[idx] == ' ':  # this will end on ':'
                idx += 1
            prev_line_key_only = idx
            continue
        prev_line_key_only = None
    if seq_indent is None and map_indent is not None:
        seq_indent, offset = map_indent, 0
    elif map_indent is None and seq_indent is not None:
        map_indent = seq_indent
    if map_indent is not None:  # if this is set seq_indent is set as well
        yaml.indent(mapping=map_indent, sequence=seq_indent, offset=offset)

    return yaml.load(yaml_str)


def load_yaml_guess_indent2(stream, yaml):
    """guess the block mapping indent and block sequence indent of yaml stream/string

    returns round_trip_loaded stream, block mapping indent level, block sequence indent
    and sequence item indicator offset
    - offset is the number of spaces before a dash relative to previous indent
    - if there are no block sequences, settings are taken from mappings (offset 0) and vv.
    """

    # load a YAML document, guess the indentation, if you use TABs you are on your own
    def leading_spaces(line):
        idx = 0
        while idx < len(line) and line[idx] == ' ':
            idx += 1
        return idx

    if isinstance(stream, str):
        yaml_str = stream
    elif isinstance(stream, bytes):
        # most likely, but the Reader checks BOM for this
        yaml_str = stream.decode('utf-8')
    else:
        yaml_str = stream.read()
    map_indent = None
    indent = None  # default if not found for some reason
    block_seq_indent = None
    prev_line_key_only = None
    key_indent = 0
    for line in yaml_str.splitlines():
        rline = line.rstrip()
        lline = rline.lstrip()
        if lline.startswith('- '):
            l_s = leading_spaces(line)
            block_seq_indent = l_s - key_indent
            idx = l_s + 1
            while line[idx] == ' ':  # this will end as we rstripped
                idx += 1
            if line[idx] == '#':  # comment after -
                continue
            indent = idx - key_indent
            break
        if map_indent is None and prev_line_key_only is not None and rline:
            idx = 0
            while line[idx] in ' -':
                idx += 1
            if idx > prev_line_key_only:
                map_indent = idx - prev_line_key_only
        if rline.endswith(':'):
            key_indent = leading_spaces(line)
            idx = 0
            while line[idx] == ' ':  # this will end on ':'
                idx += 1
            prev_line_key_only = idx
            continue
        prev_line_key_only = None
    if indent is None and map_indent is not None:
        indent = map_indent

    return yaml.load(yaml_str), indent, indent, block_seq_indent


class YAMLCommand:
    def __init__(self, args, config=None):
        self._args = args
        self._config = config
        self._yaml = None

    @property
    def yaml(self):
        if self._yaml is None:
            self._yaml = ruamel.yaml.YAML()
            self._yaml.preserve_quotes = True
            self._yaml.default_flow_style = (
                True
                if getattr(self._args, 'flow', False)
                else None
                if getattr(self._args, 'semi', False)
                else False
            )
        return self._yaml

    def ini(self):
        return self.from_ini()

    def from_ini(self):
        try:
            from configobj import ConfigObj
        except ImportError:
            print('to convert from .ini you need to install configobj:')
            print('  pip install configobj:')
            sys.exit(1)
        errors = 0
        doc = []
        cfg = ConfigObj(open(self._args.file))
        if self._args.test:
            print(ruamel.yaml.dump(cfg))
            return
        for line in configobj_walker(cfg):
            doc.append(line)
        joined = '\n'.join(doc)
        rto = self.round_trip_single(joined)
        if self._args.basename:
            out_fn = os.path.splitext(self._args.file)[0] + '.yaml'
            if self._args.verbose > 0:
                print('writing', out_fn)
            with open(out_fn, 'w') as fp:
                print(rto, end='', file=fp)  # already has eol at eof
        else:
            print(rto, end='')  # already has eol at eof
        # print()
        # if rto != joined:
        #     self.diff(joined, rto, "test.ini")
        return 1 if errors else 0

    def pon(self):
        return self.from_pon()

    def from_pon(self):
        errors = 0
        docs = []
        data = None
        for file_name in self._args.file:
            file_path = Path(file_name).expanduser()
            if not self._args.write and file_name == '-':
                data = _loads(sys.stdin.read())
            else:
                data = _loads(file_path.read_text())
            if 'glbl' in data and 'global' not in data:
                # cannot have reserved word global in dict(global=....)
                data['global'] = data.pop('glbl')
            if self._args.write:
                yaml_file_name = file_path.with_suffix('.yaml')
                self.yaml.dump(data, yaml_file_name)
            else:
                docs.append(data)
        if self._args.write:
            return 1 if errors else 0
        if self._args.literal:
            from ruamel.yaml.scalarstring import walk_tree

            for doc in docs:
                walk_tree(doc)
        self.yaml.dump_all(docs, sys.stdout)
        return 1 if errors else 0

    def test(self):
        self._args.event = self._args.node = True
        dbg = 0
        if self._args.event:
            dbg |= DBG_EVENT
        if self._args.node:
            dbg |= DBG_NODE
        os.environ['YAMLDEBUG'] = str(dbg)
        if False:
            x = ruamel.yaml.comment.Comment()
            print(sys.getsizeof(x))
            return

        def print_input(input):
            print(input, end='')
            print('-' * 15)

        def print_tokens(input):
            print('Tokens (from scanner) ' + '#' * 50)
            raise NotImplementedError
            tokens = ruamel.yaml.scan(input, ruamel.yaml.RoundTripLoader)
            for idx, token in enumerate(tokens):
                # print(token.start_mark)
                # print(token.end_mark)
                print('{0:2} {1}'.format(idx, token))

        def rt_events(input):
            raise NotImplementedError
            dumper = ruamel.yaml.RoundTripDumper
            events = ruamel.yaml.parse(input, ruamel.yaml.RoundTripLoader)
            print(ruamel.yaml.emit(events, indent=False, Dumper=dumper))

        def rt_nodes(input):
            raise NotImplementedError
            dumper = ruamel.yaml.RoundTripDumper
            nodes = ruamel.yaml.compose(input, ruamel.yaml.RoundTripLoader)
            print(ruamel.yaml.serialize(nodes, indent=False, Dumper=dumper))

        def print_events(input):
            raise NotImplementedError
            print('Events (from parser) ' + '#' * 50)
            events = ruamel.yaml.parse(input, ruamel.yaml.RoundTripLoader)
            for idx, event in enumerate(events):
                print('{0:2} {1}'.format(idx, event))

        def print_nodes(input):
            raise NotImplementedError
            print('Nodes (from composer) ' + '#' * 50)
            x = ruamel.yaml.compose(input, ruamel.yaml.RoundTripLoader)
            x.dump()  # dump the node

        def scan_file(file_name):
            inp = open(file_name).read()
            print('---------\n', file_name)
            print('---', repr(self.first_non_empty_line(inp)))
            print('<<<', repr(self.last_non_empty_line(inp)))

        if False:
            for x in self._args.file:
                scan_file(x)
            return

        if True:
            import pickle

            lines = 0
            for x in self._args.file:
                print(x, end=' ')
                if x.endswith('.yaml'):
                    data = ruamel.yaml.load(open(x))
                    print(len(data), end=' ')
                    lines += len(data)
                    out_name = x.replace('.yaml', '.pickle')
                    with open(out_name, 'w') as fp:
                        pickle.dump(data, fp)
                elif x.endswith('.pickle'):
                    with open(x) as fp:
                        data = pickle.load(fp)
                    print(len(data), end=' ')
                    lines += len(data)
                print()
            print('lines', lines)
            return

        input = textwrap.dedent(
            """
        application: web2py
        version: 1
        runtime: python27
        api_version: 1
        threadsafe: false

        default_expiration: "24h"

        handlers:
        - url: /(?P<a>.+?)/static/(?P<b>.+)
          static_files: 'applications/\\1/static/\\2'
          upload: applications/(.+?)/static/(.+)
          secure: optional
        """
        )

        input = textwrap.dedent(
            """\
        a:
            b: foo
            c: bar
        """
        )

        print_input(input)
        print_tokens(input)
        print_events(input)
        # rt_events(input)
        print_nodes(input)
        # rt_nodes(input)

        raise NotImplementedError
        data = ruamel.yaml.load(input, ruamel.yaml.RoundTripLoader)
        print('data', data)
        if False:
            data['american'][0] = 'Fijenoord'
            r = data['american']
        r = data
        if True:
            # print type(r), '\n', dir(r)
            comment = getattr(r, '_yaml_comment', None)
            print('comment_1', comment)
        dumper = ruamel.yaml.RoundTripDumper
        print('>>>>>>>>>>')
        # print(ruamel.yaml.dump(data, default_flow_style=False,
        #    Dumper=dumper), '===========')
        print('{0}========='.format(ruamel.yaml.dump(data, indent=4, Dumper=dumper)))
        comment = getattr(r, '_yaml_comment', None)
        print('comment_2', comment)

        # test end

    def json(self):
        return self.from_json()

    def from_json(self):
        # use roundtrip to preserve order
        errors = 0
        docs = []
        yaml = ruamel.yaml.YAML()
        data = None
        dfs = True if self._args.flow else None if self._args.semi else False
        yaml.default_flow_style = (
            True if self._args.flow else None if self._args.semi else False
        )
        for file_name in self._args.file:
            if not self._args.write and file_name == '-':
                inp = sys.stdin.read()
            elif self._args.mozlz4:
                with open(file_name, 'rb') as fp:
                    assert fp.read(8) == b'mozLz40\0'
                    inp = lz4.block.decompress(fp.read()).decode('utf-8')
                    import ujson

                    data = ujson.loads(inp)
            else:
                inp = open(file_name).read()
            if data is None:
                yaml = ruamel.yaml.YAML()
                try:
                    data = yaml.load(inp)
                except ruamel.yaml.composer.ComposerError as e:
                    pm = (e.problem_mark.line, e.problem_mark.column)
                    if 'expected' in e.context and 'single' in e.context and pm == (1, 0):
                        try:
                            data = self._from_line_json(inp)
                        except Exception as e:
                            raise e
                data = commentify(data)
            if self._args.write:
                raise NotImplementedError
                # os.path.copy(path, edit_path)  # edit_path.write_bytes(path.read_bytes)
                # with open(yaml_file_name, 'w') as fp:
                #     yaml.dump(data, fp)
            else:
                docs.append(data)
        if self._args.write:
            return 1 if errors else 0
        if self._args.literal:
            from ruamel.yaml.scalarstring import walk_tree

            for doc in docs:
                walk_tree(doc)
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = dfs
        yaml.dump_all(docs, sys.stdout)
        return 1 if errors else 0

    def _from_line_json(self, inp):
        """parse line json (i.e. one json document per line) and convert to
           list of loaded constructs"""
        # yaml = ruamel.yaml.YAML(type='safe')
        import ujson

        data = []
        for line in inp.splitlines():
            data.append(ujson.loads(line))
        return data

    def pickle(self):
        import pickle

        # import dill as pickle
        data = []
        for arg in self._args.file:
            with open(arg, 'rb') as fp:
                data.append(pickle.load(fp, encoding='latin-1'))
        auto_add_representers(data, self.yaml, self._args.create_to_yaml)
        self.dump(data, self._args.file)

    @contextlib.contextmanager
    def yaml_out(self):
        # so you can do:
        # with yaml_out(self._args.output) as out:
        #     yaml.dump(data, out)
        path = getattr(self._args, 'output', False)
        if path is not None:
            yield Path(path)
        else:
            yield sys.stdout

    def dump(self, data, file_names):
        # literal transform
        if getattr(self._args, 'literal', False):
            for doc in data:
                walk_tree(doc)
        do_write = getattr(self._args, 'write', False)
        do_output = getattr(self._args, 'output', False)
        if do_write and do_output:
            print('can only specify one of --write and --output')
        if do_write:
            for idx, sd in enumerate(data):
                file_name = Path(file_names[idx]).with_suffix('.yaml')
                self.yaml.dump(sd, file_name)
            return
        if len(data) == 1:
            with self.yaml_out() as out:
                self.yaml.dump(data[0], out)
        else:
            with self.yaml_out() as out:
                self.yaml.dump_all(data, out)

    def htmltable(self):
        return self.to_htmltable(self)

    def to_htmltable(self):
        def vals(x):
            if isinstance(x, list):
                return x
            if isinstance(x, (dict, ordereddict)):
                return x.values()
            return []

        def seek_levels(x, count=0):
            my_level = count
            sub_level = 0
            for v in vals(x):
                if v is None:
                    continue
                sub_level = max(sub_level, seek_levels(v, my_level + 1))
            return max(my_level, sub_level)

        inp = open(self._args.file).read()
        yaml = ruamel.yaml.YAML()
        code = yaml.load(inp)
        # assert isinstance(code, [ruamel.yaml.comments.CommentedMap])
        assert isinstance(code, (dict, list))
        levels = seek_levels(code)
        if self._args.level:
            print('levels:', levels)
            return
        print(yaml_to_html(code, levels))

    def from_html(self):
        from ruamel.yaml.convert.html import HTML2YAML

        h2y = HTML2YAML(self._args)
        with open(self._args.file) as fp:
            print(h2y(fp.read()))

    def from_csv(self):
        from ruamel.yaml.convert.csv_yaml import CSV2YAML

        c2y = CSV2YAML(self._args)
        c2y(self._args.file)

    def from_dirs(self):
        import glob

        files = []
        for fn in [glob.glob(fns) for fns in self._args.file]:
            files.extend(fn)
        if self._args.sequence:
            yaml = ruamel.yaml.YAML()
            yaml.preserve_quotes = True
            tl_data = ruamel.yaml.comments.CommentedSeq()
            for fn in files:
                tl_data.append(yaml.load(open(fn)))
            return self.output(tl_data, yaml=yaml)
        if not self._args.use_file_names:
            dirs = set()
            for fn in files:
                dn = os.path.dirname(fn)
                if dn in dirs:
                    print('double directory {}, using file names'.format(dn))
                    self._args.use_file_names = True
                    break
                else:
                    dirs.add(dn)
        tl_data = ruamel.yaml.comments.CommentedMap()
        for fn in sorted(files):
            path = os.path.dirname(fn).split(os.path.sep)
            if self._args.use_file_names:
                bn, ext = os.path.splitext(fn)
                if ext == '.yaml':
                    path.append(bn)
                else:
                    path.append(fn)
            parent_data = tl_data
            while path:
                key, path = path[0], path[1:]
                if path:
                    data = ruamel.yaml.comments.CommentedMap()
                else:
                    data = ruamel.yaml.load(open(fn), Loader=ruamel.yaml.RoundTripLoader)
                parent_data = parent_data.setdefault(key, data)
            # parent_data =
        self.output(tl_data)

    def mapping(self):
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        self.indent(yaml)
        if self._args.file == '-':
            data = yaml.load(sys.stdin)
        else:
            with open(self._args.file) as fp:
                data = yaml.load(fp)
        tl_data = ruamel.yaml.comments.CommentedMap()
        tl_data[self._args.key] = data
        self.output(tl_data, yaml)

    def indent(self, yaml, data=None):
        x = self._args.indent
        if x == 'auto' and data is None:
            return
            raise NotImplementedError
        yaml.indent(*[int(y) for y in x.split(',')])

    def output(self, data, yaml=None):
        if yaml is None:
            yaml = ruamel.yaml.YAML()
            self.indent(yaml)
        if self._args.output:
            with open(self._args.output, 'w') as fp:
                yaml.dump(data, fp)
        else:
            yaml.dump(data, sys.stdout)

    def rt(self):
        return self.round_trip()

    def round_trip(self):
        if self._args.save:
            if self._args.smart_string:
                ruamel.yaml.RoundTripDumper.org_represent_str = (
                    ruamel.yaml.RoundTripDumper.represent_str
                )

                def repr_str(dumper, data):
                    if '\n' in data:
                        return dumper.represent_scalar(
                            'tag:yaml.org,2002:str', data, style='|'
                        )
                    return dumper.org_represent_str(data)

                ruamel.yaml.add_representer(str, repr_str, Dumper=ruamel.yaml.RoundTripDumper)
            for file_name in self._args.file:
                self.round_trip_save(file_name)
            return
        errors = 0
        warnings = 0
        for file_name in self._args.file:
            inp = open(file_name).read()
            e, w, stabilize, outp = self.round_trip_input(inp)
            if w == 0:
                if self._args.verbose > 0:
                    print('{0}: ok'.format(file_name))
                continue
            if not self._args.save or self._args.verbose > 0:
                print('{0}:\n     {1}'.format(file_name, ', '.join(stabilize)))
                self.diff(inp, outp, file_name)
            errors += e
            warnings += w
        if errors > 0:
            return 2
        if warnings > 0:
            return 1
        return 0

    def round_trip_save(self, file_name):
        inp = open(file_name).read()
        backup_file_name = file_name + '.orig'
        if not os.path.exists(backup_file_name):
            os.rename(file_name, backup_file_name)
        return self.round_trip_single(inp, out_file=file_name)

    def round_trip_input(self, inp):
        errors = 0
        warnings = 0
        stabilize = []
        outp = self.round_trip_single(inp)
        if inp == outp:
            return errors, warnings, stabilize, outp
        warnings += 1
        if inp.split() != outp.split():
            errors += 1
            stabilize.append('drops info on round trip')
        else:
            if self.round_trip_single(outp) == outp:
                stabilize.append('stabilizes on second round trip')
            else:
                errors += 1
        ncoutp = self.round_trip_single(inp, drop_comment=True)
        if self.round_trip_single(ncoutp, drop_comment=True) == ncoutp:
            stabilize.append('ok without comments')
        return errors, warnings, stabilize, outp

    def round_trip_single(self, inp, drop_comment=False, out_file=None):
        explicit_start = self.first_non_empty_line(inp) == '---'
        explicit_end = self.last_non_empty_line(inp) == '...'
        width = getattr(self._args, 'width', None)
        map_indent = self._args.indent
        if map_indent is not None:
            map_indent = int(map_indent)
        seq_indent = self._args.indent
        if seq_indent is not None:
            seq_indent = int(map_indent)
        block_seq_indent = self._args.block_seq_indent
        if map_indent is None or block_seq_indent is None:
            yaml = ruamel.yaml.YAML()
            # from ruamel.yaml.util import load_yaml_guess_indent
            _, mi2, si2, off2 = load_yaml_guess_indent2(inp, yaml)
            if map_indent is None:
                map_indent = mi2
            if seq_indent is None:
                seq_indent = si2
            if block_seq_indent is None:
                block_seq_indent = off2
        elif block_seq_indent is not None and seq_indent is None:
            map_indent = seq_indent = block_seq_indent + 2
        elif block_seq_indent is not None and seq_indent is not None:
            if block_seq_indent + 2 > seq_indent:
                raise Exception(
                    'No room in indentation for offset of block sequence indicator'
                )
        if seq_indent is None:
            seq_indent = 2
        else:
            seq_indent = max(seq_indent, 2)
        if map_indent is None:
            map_indent = 2
        else:
            map_indent = max(map_indent, 2)
        if block_seq_indent is not None:
            block_seq_indent = min(block_seq_indent, seq_indent - 2)

        if False:
            loader = ruamel.yaml.RoundTripLoader
            code = ruamel.yaml.load(inp, loader)
            if drop_comment:
                drop_all_comment(code) # NOQA
            dumper = ruamel.yaml.RoundTripDumper
            res = ruamel.yaml.dump(
                code,
                Dumper=dumper,
                # indent=indent,
                block_seq_indent=block_seq_indent,
                explicit_start=explicit_start,
                explicit_end=explicit_end,
            )
        else:
            yaml = ruamel.yaml.YAML()
            yaml.indent(map_indent, seq_indent, block_seq_indent)
            yaml.explicit_start = explicit_start
            yaml.explicit_end = explicit_end
            yaml.width = width
            code = yaml.load(inp)
            if out_file:
                with open(out_file, 'w') as fp:
                    yaml.dump(code, fp)
                res = None
            else:
                buf = ruamel.yaml.compat.StringIO()
                yaml.dump(code, buf)
                res = buf.getvalue()
        return res

    def first_non_empty_line(self, txt):
        """return the first non-empty line of a block of text (stripped)
        do not split or strip the complete txt
        """
        pos = txt.find('\n')
        if pos == -1:  # no newline in txt
            return txt.strip()
        prev_pos = 0
        while pos >= 0:
            segment = txt[prev_pos:pos].strip()
            if segment:
                break
            # print (pos, repr(segment))
            prev_pos = pos
            pos = txt.find('\n', pos + 1)
        return segment

    def last_non_empty_line(self, txt):
        """return the last non-empty line of a block of text (stripped)
        do not split or strip the complete txt
        """
        pos = txt.rfind('\n')
        if pos == -1:  # no newline in txt
            return txt.strip()
        prev_pos = len(txt)
        maxloop = 10
        while pos >= 0:
            segment = txt[pos:prev_pos].strip()
            if segment:
                break
            # print (pos, repr(segment))
            prev_pos = pos
            pos = txt.rfind('\n', 0, pos - 1)
            maxloop -= 1
            if maxloop < 0:
                break
        return segment

    def diff(self, inp, outp, file_name):
        import difflib

        inl = inp.splitlines(True)  # True for keepends
        outl = outp.splitlines(True)
        diff = difflib.unified_diff(inl, outl, file_name, 'round trip YAML')
        # 2.6 difflib has trailing space on filename lines %-)
        strip_trailing_space = sys.version_info < (2, 7)
        for line in diff:
            if strip_trailing_space and line[:4] in ['--- ', '+++ ']:
                line = line.rstrip() + '\n'
            sys.stdout.write(line)

    def me(self):
        return self.merge_expand()

    def merge_expand(self):
        yaml = YAML()
        yaml.Constructor.flatten_mapping = ruamel.yaml.SafeConstructor.flatten_mapping
        yaml.default_flow_style = False
        yaml.allow_duplicate_keys = True
        if not self._args.allow_anchors:
            yaml.representer.ignore_aliases = lambda x: True

        if self._args.file[0] == '-':
            data = yaml.load(sys.stdin)
        else:
            with open(self._args.file[0]) as fp:
                data = yaml.load(fp)
        if self._args.file[1] == '-':
            yaml.dump(data, sys.stdout)
        else:
            with open(self._args.file[1], 'w') as fp:
                yaml.dump(data, fp)

    @staticmethod
    def split_path(path):
        """if path is a list of one element, split that element on the first
           non-alphanumerid character and return the resulting list
        """
        if not isinstance(path, list):
            path = [path]
        if len(path) == 1:
            for ch in path[0]:
                if not ch.isalnum():
                    path = path[0].split(ch)
                    break
        return path

    def add(self):
        path = self._args.args
        value = self._args.value if self._args.value is not None else path.pop(-1)
        file_name = Path(self._args.file if self._args.file is not None else path.pop(0))
        path = self.split_path(path)
        # if len(path) == 1:
        #    for ch in path[0]:
        #        if not ch.isalnum():
        #            path = path[0].split(ch)
        #            break
        if not self._args.str:
            sr = SimpleResolver()
            value = sr(value)
        if self._args.verbose > 0:
            print(f'value: {value:!r}')
            print(f'file_name: {file_name}')
            print(f'path: {path}')
        ay = AddableYAML(file_name, create_ok=True)
        res = ay.add(
            path,
            value,
            create_parents=self._args.parents,
            create_item=self._args.item,
            create_key=self._args.key,
        )
        if res is not None:
            print(res)
            sys.exit(1)
        ay.save()

    def sort(self):
        path = self._args.args
        file_name = Path(self._args.file if self._args.file is not None else path.pop(0))
        yaml = YAML()
        data = d = load_yaml_guess_and_set_indent(file_name, yaml)
        path = self.split_path(path)
        while path:
            k = path.pop(0)
            d = d[k]
        assert isinstance(d, dict)
        keys = list(d.keys())
        sl = sorted(d.keys())
        if sl != keys:
            for key in sl:
                d[key] = d.pop(key)
        else:
            return
        # print(sl)
        # print(list(d.keys()))
        # print(sl == keys)
        yaml.dump(data, file_name)

    def edit(self):
        self.edit_one(Path(self._args.file).expanduser())

    def edit_one(self, path):
        edit_path = path.parent / ('.ye.' + path.name)
        if edit_path.exists():
            edit_path_time = edit_path.stat().st_mtime
            if edit_path.stat().st_mtime < path.stat().st_mtime:
                print(f'{edit_path} exists but is older than {path}, delete or touch it')
                return
            else:
                print(f're-editing {edit_path}')
        else:
            edit_path.write_bytes(path.read_bytes())
            edit_path_time = edit_path.stat().st_mtime
        # print(path, edit_path, edit_path.exists())
        editor = os.environ.get('EDITOR', 'kak')
        # print('editor', editor)
        subprocess.run([editor, str(edit_path)])
        if edit_path.stat().st_mtime == edit_path_time:
            print('not changed')
            edit_path.unlink()
        self.yaml.load(edit_path)
        path.unlink()
        edit_path.rename(path)


# ToDo: move to ruamel.yaml.base
class AddableYAML(ruamel.yaml.base.YAMLBase):
    def add(self, path, value, create_parents=False, create_item=False, create_key=False):
        """
          The path is a list/tuple of which each element is used to "descend" the data
          structure. If an element is an integer a list/sequence is assumed, else a dict/mapping.
          The path consists of zero or more parents, the last of which is the item, and a key.

          Without setting appropriate create_*, an error is thrown when a new parent/item/key is unknown
          If create_parents is false, the all parents needs to exists in the data structure 
          If create_item is false, then create last parent doens't exist, else error
          If not create_key, only set value if other children of parent have this key 
        """  # NOQA
        if create_parents:
            create_item = True
            create_key = True  # if you are allowed to create parents, also create attr
        # try to get parent
        d = self.data
        parent = None
        parent_path = path[:-1]
        attr = path[-1]
        while parent_path:
            k = parent_path.pop(0)
            try:
                tmp_d = d
                d = d[k]
                parent = tmp_d
            except KeyError:
                # if parent_path is not empty, we are not creating the item
                # that will contain the key/index
                if (parent_path and create_parents) or (not parent_path and create_item):
                    if isinstance(k, int):
                        d[k] = ruamel.yaml.comments.CommentedSeq()
                    else:
                        d[k] = ruamel.yaml.comments.CommentedMap()
                    parent = d
                    d = d[k]
                else:
                    if parent_path:
                        return f'parent "{k}" from {path} not in data structure'
                    return f'item "{k}" not in data structure'
        if attr in d:
            #     del d[attr]  # this resets quoting from earlier value that needs quoting
            pass
        elif not create_key:
            if isinstance(parent, list):
                for elem in parent:
                    try:
                        elem[attr]
                        break
                    except IndexError:
                        continue
                else:
                    return f'key "{attr}" not in siblings'
            else:
                for v in parent.values():
                    try:
                        if attr in v:
                            break
                    except (IndexError, TypeError):  # TypeError e.g. on datetime
                        continue
                else:
                    return f'key "{attr}" not in siblings'
        # update doesn't preserve forced quoting from previous value, assignment would
        d.update(**{attr: value})
        self._changed = True


# ToDo?: reference this in https://github.com/python-attrs/attrs/issues/741#
# or move it to `ruamel.yaml` itself?


def auto_add_representers(data, yaml, force=False, added=None):
    if added is None:
        added = set()
    # to automatically
    if not force and (type(data) not in added and hasattr(data, 'to_yaml')):
        yaml.register_class(type(data))
        added.add(type(data))
    elif type(data) not in added and hasattr(data, '__getstate__'):
        type(data).to_yaml = TaggedToYaml(data)
        yaml.register_class(type(data))
        added.add(type(data))
    if isinstance(data, dict):
        for k, v in data.items():
            auto_add_representers(k, yaml, force=force, added=added)
            auto_add_representers(v, yaml, force=force, added=added)
    elif isinstance(data, list):
        for elem in data:
            auto_add_representers(elem, yaml, force=force, added=added)


class TaggedToYaml:
    def __init__(self, data):
        t = data.__class__.__name__
        m = data.__class__.__module__
        if m in [None, '__builtin__']:
            self.tag = '!' + t
        else:
            self.tag = '!' + m + '.' + t

    def __call__(self, dumper, data):
        d = data.__getstate__()
        return dumper.represent_mapping(self.tag, d)


# class ConfigPON(ConfigBase):
#     suffix = '.pon'
#
#     def load(self) -> typing.Any:
#         try:
#             data = _loads(self._path.read_text())
#         except FileNotFoundError as e:
#             print(e)
#             data = {}
#         if 'glbl' in data and 'global' not in data:
#             # cannot have reserved word global in dict(global=....)
#             data['global'] = data.pop('glbl')
#         return data


# taken from pon.__init__.py
def _loads(
    node_or_string: typing.Union[_ast.Expression, str],
    dict_typ: typing.Any = dict,
    return_ast: bool = False,
    file_name: typing.Optional[str] = None,
) -> typing.Any:
    """
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, bytes, numbers, tuples, lists, dicts,
    sets, booleans, and None.
    """
    if sys.version_info < (3, 4):
        _safe_names = {'None': None, 'True': True, 'False': False}
    if isinstance(node_or_string, str):
        node_or_string = compile(
            node_or_string,
            '<string>' if file_name is None else file_name,
            'eval',
            _ast.PyCF_ONLY_AST,
        )
    if isinstance(node_or_string, _ast.Expression):
        node_or_string = node_or_string.body  # type: ignore
    else:
        raise TypeError('only string or AST nodes supported')

    def _convert(node: typing.Any, expect_string: bool = False) -> typing.Any:
        if isinstance(node, ast.Str):
            if sys.version_info < (3,):
                return node.s
            return node.s
        elif isinstance(node, ast.Bytes):
            return node.s
        if expect_string:
            pass
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, _ast.Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, _ast.List):
            return list(map(_convert, node.elts))
        elif isinstance(node, _ast.Set):
            return set(map(_convert, node.elts))
        elif isinstance(node, _ast.Dict):
            return dict_typ(
                (_convert(k, expect_string=False), _convert(v))
                for k, v in zip(node.keys, node.values)
            )
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif sys.version_info < (3, 4) and isinstance(node, ast.Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif (
            isinstance(node, _ast.UnaryOp)
            and isinstance(node.op, (_ast.UAdd, _ast.USub))
            and isinstance(node.operand, (ast.Num, _ast.UnaryOp, _ast.BinOp))
        ):
            operand = _convert(node.operand)
            if isinstance(node.op, _ast.UAdd):
                return +operand
            else:
                return -operand
        elif (
            isinstance(node, _ast.BinOp)
            and isinstance(node.op, (_ast.Add, _ast.Sub, _ast.Mult))
            and isinstance(node.right, (ast.Num, _ast.UnaryOp, _ast.BinOp))
            and isinstance(node.left, (ast.Num, _ast.UnaryOp, _ast.BinOp))
        ):
            left = _convert(node.left)
            right = _convert(node.right)
            if isinstance(node.op, _ast.Add):
                return left + right
            elif isinstance(node.op, _ast.Mult):
                return left * right
            else:
                return left - right
        elif isinstance(node, _ast.Call):
            func_id = getattr(node.func, 'id', None)
            if func_id == 'dict':
                return dict_typ((k.arg, _convert(k.value)) for k in node.keywords)
            elif func_id == 'set':
                return set(_convert(node.args[0]))
            elif func_id == 'date':
                return datetime.date(*[_convert(k) for k in node.args])
            elif func_id == 'datetime':
                return datetime.datetime(*[_convert(k) for k in node.args])
            elif func_id == 'dedent':
                return textwrap.dedent(*[_convert(k) for k in node.args])
        elif isinstance(node, ast.Name):
            return node.s  # type: ignore
        err = SyntaxError('malformed node or string: ' + repr(node))
        err.filename = '<string>'
        err.lineno = node.lineno
        err.offset = node.col_offset
        err.text = repr(node)
        err.node = node  # type: ignore
        raise err

    res = _convert(node_or_string)
    if not isinstance(res, dict_typ):
        raise SyntaxError('Top level must be dict not ' + repr(type(res)))
    if return_ast:
        return res, node_or_string
    return res


# def drop_all_comment(code):
#     if isinstance(code, ruamel.yaml.comments.CommentedBase):
#         if hasattr(code, 'ca'):
#             delattr(code, ruamel.yaml.comments.Comment.attrib)
#     if isinstance(code, list):
#         for elem in code:
#             drop_all_comment(elem)
#     elif isinstance(code, dict):
#         for key in code:
#             drop_all_comment(code[key])
