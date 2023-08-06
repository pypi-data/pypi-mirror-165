# encoding: utf-8

from __future__ import print_function

import os
import sys
import json
import stat
import argparse
import datetime

from . import logs
from . import utils
from . import errors
from . import registry
from . import interface
from . import codec, formatter, service, transport
from .utils.function import Param

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'

COLLECTION_TYPES = frozenset(['list', 'dict'])

def main():
    """Convenient entry-point."""
    Parser().main()

class Parser(object):
    def __init__(self):
        # global args
        self.base_parser = argparse.ArgumentParser(add_help=False)
        self.add_global_args(self.base_parser)

    def main(self):
        """Processes command-line arguments and calls any selected command."""

        # temp parser to grab connection arguments
        parser = argparse.ArgumentParser(add_help=False, parents=[self.base_parser])
        parser.add_argument('-h', '--help', action='store_true',
            help='show this help message and exit')
        parser.add_argument('rest', nargs=argparse.REMAINDER,
            help=argparse.SUPPRESS)

        args, extra_args = parser.parse_known_args()

        logs.init(args.verbose)

        # import built-in modules
        registry.init()

        # import additional modules
        for imp in args.imports:
            utils.path.import_module(imp)

        if args.list:
            meta = {
                'codecs': codec.CodecMeta,
                'formatters': formatter.FormatterMeta,
                'services': service.ServiceMeta,
                'transports': transport.TransportMeta,
                }[args.list]

            # select an output formatter
            try:
                fmt = formatter.get(args.format)
            except Exception as e:
                if args.verbose: raise
                parser.error(e)

            fmt.process(meta.names())
            return

        # parser for transport and service args
        parser = argparse.ArgumentParser(parents=[self.base_parser])

        cls = transport.get(args.url)
        if isinstance(cls, Exception):
            self.add_transport_exception(parser, args.url.scheme, cls)
        else:
            self.add_transport_args(parser, cls)

        # add service arguments
        used_aliases = set()
        for name in sorted(args.services):
            name, alias = service.parse_alias(name)
            cls = service.get_class(name)

            alias = alias or cls._name_
            if alias in used_aliases:
                raise ValueError('duplicate service alias: {}'.format(alias))
            used_aliases.add(alias)

            self.add_service_args(parser, cls, alias)

        # help
        if args.help:
            parser.print_help()
            parser.exit()

        # collect transport and service args
        sub_args = parser.parse_args(extra_args)
        trn_args, svc_args = self.get_prefixed_args(sub_args)

        trn_name = args.url.scheme
        trn = transport.get(args.url, trn_args.get(trn_name))

        # start client or server
        if args.server_mode:
            if args.rest:
                parser.error('unrecognized arguments: {}'.format(' '.join(args.rest)))
            self.start_server(trn, args, svc_args)
        else:
            self.start_client(trn, parser, args)

    def start_client(self, trn, parser, args):
        client = interface.Client(trn,
            codec=args.codec,
            retry_count=args.retry_count,
            retry_interval=args.retry_interval,
            )

        # get service metadata
        try:
            meta = client.service('_meta')

            if args.version:
                # show server status and exit
                status = meta.status()
                self.print_status(status)
                parser.exit()

            svcs = meta.services()

        except errors.RemoteError as e:
            if not args.verbose and e.name == 'KeyError':
                parser.error('metadata service not available')
            raise

        except Exception as e:
            if args.verbose: raise
            err = '{}\nconnection required for help on remote services'
            parser.error(err.format(e))

        # add services
        svc_subs = parser.add_subparsers(title='remote services')

        for svc in sorted(svcs, key=lambda s: s['name']):
            svc_name = svc['name']
            svc_desc = self.get_help(svc['doc'])
            svc_parser = svc_subs.add_parser(svc_name,
                help=svc_desc, description=svc['doc'])
            svc_parser.set_defaults(svc_name=svc_name)

            # add service commands
            cmd_subs = svc_parser.add_subparsers(title='commands', dest='command')
            cmd_subs.required = True

            for cmd in svc['commands']:
                cmd_name = cmd['name']
                cmd_desc = self.get_help(cmd['doc'])
                cmd_parser = cmd_subs.add_parser(cmd_name,
                    help=cmd_desc, description=cmd['doc'])
                self.add_command_args(cmd_parser, cmd)
                cmd_parser.set_defaults(cmd_name=cmd_name, cmd_meta=cmd)

        # help
        if args.help:
            parser.print_help()
            parser.exit()
        elif not args.rest:
            parser.print_usage()
            parser.exit()

        # select an output formatter
        try:
            fmt = formatter.get(args.format)
        except Exception as e:
            if args.verbose: raise
            parser.error(e)

        # get the command arguments
        verbose = args.verbose
        args = parser.parse_args(args.rest)
        cmd_args, cmd_kwargs = self.get_command_args(args)

        # get the command function
        svc = client.service(args.svc_name, metadata=[args.cmd_meta])
        func = getattr(svc, args.cmd_name)

        # call the command
        try:
            res = func(*cmd_args, **cmd_kwargs)
        except errors.RemoteError as e:
            if verbose: raise
            parser.error(e)
        fmt.process(res)

    def start_server(self, trn, args, svc_args):
        # create server
        s = interface.Server(trn, codec=args.codec, version=args.server_version,
            remote_tracebacks=args.remote_tracebacks)

        # add services
        for name in args.services:
            name, alias = service.parse_alias(name)
            s_args = svc_args.get(name, {})
            s.add_service(name, s_args, alias)

        s.serve()

    ## get arguments ##

    def get_prefixed_args(self, args):
        pfx_args = {}

        for name, value in vars(args).items():
            try:
                prefix, cls_name, arg_name = name.split('_', 2)
            except ValueError:
                continue

            cls_args = pfx_args.setdefault(prefix, {})
            cls_args.setdefault(cls_name, {})[arg_name] = value

        return pfx_args.get('transport', {}), pfx_args.get('service', {})

    def get_command_args(self, args):
        """Processes the command-line arguments and returns the arguments to
        pass to the selected command."""
        cmd = args.cmd_meta

        cmd_args = []
        cmd_kwargs = {}

        for param in cmd['params']:
            name = param['name']
            kind = param['kind']

            if param.get('hide', False):
                continue

            arg = getattr(args, param['name'])

            if kind in {Param.POSITIONAL_ONLY, Param.POSITIONAL_OR_KEYWORD}:
                cmd_args.append(arg)
            elif kind == Param.VAR_POSITIONAL:
                cmd_args.extend(arg)
            elif kind == Param.VAR_KEYWORD:
                cmd_kwargs.update(arg or {})
            elif kind == Param.KEYWORD_ONLY:
                cmd_kwargs[name] = arg
            else:
                assert False

        return cmd_args, cmd_kwargs

    ## add arguments ##

    def add_service_args(self, parser, cls, alias):
        svc_parser = parser.add_argument_group(
            '{} service arguments'.format(alias))

        # add a prefix to every param
        cmd = utils.function.func_to_dict(cls.__init__, remove_self=True)
        for param in cmd['params']:
            param['name'] = '_'.join(['service', alias, param['name']])
            # force keyword-only params for clarity
            if param['kind'] != Param.VAR_KEYWORD:
                param['kind'] = Param.KEYWORD_ONLY

            param.setdefault('default', argparse.SUPPRESS)

        self.add_command_args(svc_parser, cmd, single_flags=False)

    def add_transport_args(self, parser, cls):
        ignored = set(['url', 'timeout'])
        trn_parser = parser.add_argument_group(
            '{} transport arguments'.format(cls._name_),
            'To see arguments for another transport, set the "--url" argument'
            )

        # add a prefix to every param
        cmd = utils.function.func_to_dict(cls.__init__, remove_self=True)
        for param in cmd['params']:
            if param['name'] in ignored:
                param['hide'] = True
            param['name'] = '_'.join(['transport', cls._name_, param['name']])
            # force keyword-only params for clarity
            if param['kind'] != Param.VAR_KEYWORD:
                param['kind'] = Param.KEYWORD_ONLY

        self.add_command_args(trn_parser, cmd, single_flags=False)

    def add_transport_exception(self, parser, name, exc):
        parser.add_argument_group(
            '{} transport arguments'.format(name),
            'failed to load transport: {}'.format(exc),
            )

    def add_command_args(self, parser, cmd, single_flags=True):
        is_option_arg = lambda p: (
            p['kind'] == Param.VAR_KEYWORD or 'default' in p)

        if single_flags:
            # keep track of used single char flags
            chars = set(u'h')
            # include single char arguments
            chars.update(p['name'] for p in cmd['params']
                if len(p['name']) == 1 and not is_option_arg(p))
        else:
            chars = None

        for param in cmd['params']:
            name = param['name']
            kind = param['kind']
            hint = param.get('hint')
            doc = param.get('doc')
            default = param.get('default', Param.empty)

            if param.get('hide', False):
                continue

            kwargs = {'metavar': name}

            if default is not Param.empty:
                kwargs['default'] = default

            if kind in {Param.KEYWORD_ONLY, Param.VAR_KEYWORD}: # **kwargs
                self.add_option_arg(parser, param, chars)

            elif 'default' in param: # args with defaults
                self.add_option_arg(parser, param, chars)

            else: # positional args
                if kind == Param.VAR_POSITIONAL: # *args
                    kwargs['nargs'] = '*'

                kwargs.update({
                    'type': self.get_converter(hint),
                    'help': self.get_argument_help(doc, hint, default),
                    })
                parser.add_argument(name, **kwargs)

    def add_option_arg(self, parser, param, chars=None):
        name = param['name']
        kind = param['kind']
        hint = param.get('hint')
        doc = param.get('doc')
        default = param.get('default')

        # use dashes instead of underscores for param names
        flag_name = name.replace('_', '-')

        # check for possible short flags
        flags = []
        added = False
        c = flag_name[0]
        C = c.upper()

        # check if the lower or uppercase char is unique
        if not chars:
            # don't add a short flag
            pass
        elif c not in chars:
            flags.append('-' + c)
            chars.add(c)
            added = True
        elif C not in chars:
            flags.append('-' + C)
            chars.add(C)
            added = True

        # add a long flag if no short flag was added
        # add a long flag if the name is more than 1 character
        if not added or len(flag_name) > 1:
            flags.append('--' + flag_name)

        if hint == 'bool':
            # handle bool special case
            group = parser.add_mutually_exclusive_group()
            if not default:
                # in case default is None
                default = False

            help = self.get_argument_help(doc)

            # add a flag for the True value
            group.add_argument(*flags, action='store_true', default=default,
                dest=name, help=help + ' (default)' if default is True else '')

            # add a flag for the False value
            group.add_argument('--no-' + flag_name, action='store_false',
                dest=name, help=help + ' (default)' if default is False else '')

        elif kind == Param.VAR_KEYWORD:
            parser.add_argument(*flags,
                action='append', dest=name, type=self.get_converter('keyword'),
                metavar='name=value', default=default,
                help=self.get_argument_help(doc, None, default))

        else:
            parser.add_argument(*flags,
                dest=name, type=self.get_converter(hint),
                metavar=self.get_argument_hint(hint), default=default,
                help=self.get_argument_help(doc, None, default))

    def add_global_args(self, parser):
        """Adds an argument group to *parser* for global arguments."""

        egroup = parser.add_mutually_exclusive_group()
        egroup.add_argument('-C', '--client', action='store_false',
            dest='server_mode', help='start in client mode (default)',
            default=False)
        egroup.add_argument('-S', '--server', action='store_true',
            dest='server_mode', help='start in server mode')

        parser.add_argument('-l', '--list',
            choices=['codecs', 'formatters', 'services', 'transports'],
            help='list the modules available for the selected category')
        parser.add_argument('-v', '--verbose', action='count',
            default=0, help='enable verbose output (-vv for more)')
        parser.add_argument('-V', '--version', action='store_true',
            help='show server version')

        group = parser.add_argument_group('configuration arguments')

        group.add_argument('-i', '--import', action='append', dest='imports',
            metavar='IMPORT', default=[],
            help='import an additional (codec/formatter/service/transport) module')
        group.add_argument('-c', '--codec',
            help='the codec format to use (default: {} on server)'.format(
                interface.DEFAULT_CODEC))
        group.add_argument('-s', '--service', action='append', dest='services',
            metavar='SERVICE', default=[],
            help='add a service module (can be set multiple times) '
                'formats: "<built-in service>[:alias]" or '
                '"<module.ServiceClass>[:alias]"')

        group = parser.add_argument_group('client arguments')

        group.add_argument('-u', '--url', type=utils.url.Url,
            default=utils.DEFAULT_URL,
            help='URL to RPC server (default: {})'.format(utils.DEFAULT_URL))
        group.add_argument('-t', '--timeout', type=float,
            help='number of seconds to wait for a response (default: no timeout)')
        group.add_argument('-r', '--retry-count', type=int,
            help='number of retry attempts to make (-1 for unlimited, default: no retries)')
        group.add_argument('--retry-interval', type=float,
            help='number of seconds between retry attempts (default: 1.0)')

        group = parser.add_argument_group('server arguments')

        group.add_argument('--server-version',
            help='version string for the server')
        group.add_argument('--remote-tracebacks', action='store_true',
            help='send tracebacks with errors')

        group = parser.add_argument_group('output arguments')

        format_default = {
            'piped': 'json',
            'redirected': 'raw',
            'terminal': 'pretty',
            }[io_stat_mode()]
        group.add_argument('-f', '--format',
            default=format_default,
            help="select a formatter by name or provide a custom Formatter "
                "subclass (default: 'pretty' on terminals, "
                "'json' when piped, and 'raw' when redirected)")

    ## parser help ##

    def get_help(self, doc):
        doc = doc or '\n'
        return doc.splitlines()[0]

    def get_argument_help(self, doc=None, hint=None, default=None):
        if hint == 'stream':
            hint = "path or '-' for stdin"
        help = '<{}>'.format(hint) if hint else ''
        if doc:
            help = '{} {}'.format(doc, help)
        if default not in [Param.empty, argparse.SUPPRESS, None]:
            help += ' (default: {})'.format(default)
        return help

    def get_argument_hint(self, hint):
        if not hint:
            return '<str>'
        elif hint in COLLECTION_TYPES:
            return '<path or JSON>'
        else:
            return '<{}>'.format(hint)

    ## parser utils ##

    def get_converter(self, hint):
        """Returns a type converter keyed to a specific typehint."""
        if hint == 'int':
            conv = lambda v: int(v)
        elif hint == 'float':
            conv = lambda v: float(v)
        elif hint == 'bytes':
            conv = lambda v: utils.encoding.to_bytes(v)
        elif hint == 'stream':
            conv = lambda v: utils.path.iter_file(argparse.FileType('rb')(v))
        elif hint == 'keyword':
            conv = lambda v: v.split('=', 1)
        elif hint == 'datetime':
            def conv(v):
                try:
                    return datetime.datetime.strptime(v, DATETIME_FORMAT)
                except ValueError:
                    try:
                        return datetime.datetime.strptime(v, DATE_FORMAT)
                    except Exception:
                        return datetime.datetime.combine(
                            datetime.date.today(),
                            datetime.datetime.strptime(v, TIME_FORMAT).time(),
                            )
        elif hint == 'stream':
            conv = lambda v: (x for x in v)
        elif hint in COLLECTION_TYPES:
            def conv(v):
                try:
                    with open(v) as f:
                        return json.load(f)
                except Exception:
                    return json.loads(v)
        else:
            conv = lambda v: utils.encoding.to_unicode(v)

        # the converter name is used in error messages
        conv.__name__ = utils.function.get_func_name(hint or 'str')

        return conv

    def print_status(self, status):
        """Prints the server version and status data."""
        # TODO: abide by --format flag
        width = max(len(k) for k in status)
        for k, v in sorted(status.items()):
            print('{:>{}}: {}'.format(k, width, v))

##
## cli utils
##

def io_stat_mode():
    mode = os.fstat(sys.stdout.fileno()).st_mode
    if stat.S_ISFIFO(mode):
        return 'piped'
    elif stat.S_ISREG(mode):
        return 'redirected'
    else:
        return 'terminal'

# fix for open issue: https://bugs.python.org/issue14156
class FileType(argparse.FileType):
    def __call__(self, string):
        fp = super(FileType, self).__call__(string)
        if string == '-' and 'r' in self._mode:
            fp = getattr(fp, 'buffer', fp)
        return fp
