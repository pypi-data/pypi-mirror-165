import ruamel.yaml


class SimpleResolver:
    def __init__(self):
        import ruamel.yaml.resolver

        self._ir = ruamel.yaml.resolver.implicit_resolvers
        self._resolvers = {}

        for idx, ir in enumerate(self._ir):
            assert len(ir) == 4  # tuple of length 4
            # skip 1.1 only
            if (1, 2) not in ir[0]:
                continue
            for ch in ir[3]:
                self._resolvers.setdefault(ch, []).append(idx)
            # print(ir[1:])
        # print(self._resolvers)

    def __call__(self, arg):
        assert isinstance(arg, str)
        try:
            idxs = self._resolvers[arg[0]]
        except KeyError:
            return arg
        for idx in idxs:
            ir = self._ir[idx]
            if not ir[2].match(arg):
                continue
            tag = ir[1].rsplit(':', 1)[1]
            if tag == 'bool':
                return arg[0].lower() == 't'
            if tag == 'float':
                return float(arg)
            if tag == 'int':
                return int(arg)
            if tag == 'null':
                return None
            if tag == 'timestamp':
                match = ruamel.yaml.util.timestamp_regexp.match(arg)
                return ruamel.yaml.util.create_timestamp(**match.groupdict())
                return self.ts(arg)
        return arg
