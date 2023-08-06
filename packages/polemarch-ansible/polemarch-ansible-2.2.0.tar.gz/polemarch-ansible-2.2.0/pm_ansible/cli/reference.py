import os
import sys
import json
from contextlib import redirect_stderr, redirect_stdout
from collections import OrderedDict

from ansible import __version__ as ansible_version
from ansible.cli.adhoc import AdHocCLI
from ansible.cli.playbook import PlaybookCLI
from ansible.cli.galaxy import GalaxyCLI
from .base import get_parser


class AnsibleArgumentsReference(object):

    def __init__(self, cli_types=(), exclude=()):
        self._exclude = exclude or []
        self._cli_filter = cli_types
        self.raw_dict = self._extract_from_cli()

    @property
    def clis(self):
        """
        Ansible cli objects

        :return: dict with cli objects
        """
        return {
            "module": AdHocCLI(args=["", "all"]),
            "playbook": PlaybookCLI(args=["", "none.yml"]),
            "galaxy": GalaxyCLI(args=['', 'info'])
        }

    def __help_text_format(self, option):
        result = (option.help or '')
        try:
            result = result % {'default': option.default}
        except:  # nocv
            pass
        return result

    def __parse_option_less_29(self, option):  # nocv
        # pylint: disable=protected-access,
        cli_result = OrderedDict()
        for name in option._long_opts:
            name = name[2:]
            if name in self._exclude:
                continue
            shortopts = [opt[1:] for opt in option._short_opts]
            cli_result[name] = dict(
                type=option.type,
                help=self.__help_text_format(option),
                shortopts=shortopts
            )
        return cli_result

    def parse_cli_less_29(self, cli):  # nocv
        # pylint: disable=protected-access,
        cli.parse()
        cli_result = OrderedDict()
        for option in cli.parser._get_all_options():
            cli_result.update(self.__parse_option_less_29(option))
        return cli_result

    parse_cli25 = parse_cli_less_29
    parse_cli26 = parse_cli_less_29
    parse_cli27 = parse_cli_less_29
    parse_cli28 = parse_cli_less_29

    def parse_cli_gte_29(self, cli):  # nocv
        try:
            with open(os.devnull, 'w') as fd, redirect_stderr(fd), redirect_stdout(fd):
                cli.parse()
        except:
            pass
        cli_result = OrderedDict()
        for action in cli.parser._actions:
            if action.option_strings:
                name = list(i for i in action.option_strings if i.startswith('--'))[0][2:]
            else:
                name = action.dest
            if name in self._exclude:
                continue
            shortopts = list(i for i in action.option_strings if not i.startswith('--'))
            action_type = action.type
            if not action_type:
                class_name = action.__class__.__name__
                if class_name in ['_StoreAction', '_AppendAction', 'PrependAction']:
                    action_type = 'string'
                elif class_name in ['_CountAction', '_AppendAction']:
                    action_type = 'int'
            elif hasattr(action_type, '__name__'):
                action_type = action_type.__name__
            else:
                action_type = 'string'
            cli_result[name] = dict(
                type=action_type,
                help=self.__help_text_format(action),
                shortopts=shortopts
            )
        return cli_result

    parse_cli29 = parse_cli_gte_29

    def _extract_from_cli(self):
        """
        Format dict with args for API

        :return: args for ansible cli
        :rtype: dict
        """
        # pylint: disable=protected-access,
        result = OrderedDict()
        ansible_version_string = ''.join(ansible_version.split('.')[:2])
        parse_function = getattr(self, 'parse_cli'+ansible_version_string)
        for name, cli in self.clis.items():
            if len(self._cli_filter) == 0 or (name in self._cli_filter):
                # result[name] = self.__parse_cli(cli)
                result[name] = parse_function(cli)
        answer = OrderedDict()
        answer['version'] = ansible_version
        answer['keywords'] = result
        return answer


def handler(args=sys.argv[1:], parser=get_parser()):
    parser = parser
    parser.add_argument(
        'filter', type=str, nargs='*', action='append',
        help='Filter cli by type. Default is all.'
    )
    parser.add_argument(
        '--exclude', type=str, nargs='?', action='append',
        help='Filter args by name (comma separated). Default is empty string.'
    )
    parser.add_argument(
        '--indent', type=int, default=None,
        help='Get indent json-output.'
    )
    _args = parser.parse_args(args)
    reference = AnsibleArgumentsReference(
        cli_types=_args.filter[0], exclude=_args.exclude
    )
    json.dump(reference.raw_dict, sys.stdout, indent=_args.indent)
