import re
import os
import sys
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import imp

import json
from tempfile import gettempdir
from collections import OrderedDict
from ansible import modules as ansible_modules, __version__ as ansible_version
from .base import get_parser


def get_data(args):
    data = []
    pathes = list(args.path)

    if len(pathes) > 1:
        pathes = pathes[1:]

    for path in pathes:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=PendingDeprecationWarning)
            data += AnsibleModules(args.detail, path).get(args.get)
    return data


def get_from_cache(args):
    cache_dir = args.cachedir
    try:
        allowed_cache = cache_dir != 'NoCache'
        if allowed_cache and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    except:  # nocv
        allowed_cache = False
    if not allowed_cache or len(args.path) > 1:
        return get_data(args)  # nocv
    suffix = 'detail' if args.detail else 'list'
    cache_name = '{}/{}_{}'.format(cache_dir, args.get or 'all', suffix)
    try:
        with open(cache_name, 'r') as fd:
            return json.load(fd)
    except:
        data = get_data(args)
        with open(cache_name, 'w') as fd:
            json.dump(data, fd)
        return data


def import_module(path, directory=None):
    """
    Import module from directory

    :param path: module python path (dot separeted)
    :type path: str,unicode
    :param directory: directory search path
    :type directory: str,unicode,NoneType
    :return: imported module or None
    :rtype: object,NoneType
    """
    fp = None
    try:
        module_name = path.replace('polemarch.project.', '')
        module_names = module_name.split('.')
        if len(module_names) > 1:
            directory = '/'.join([directory] + module_names[:-1]).replace('//', '/')
        imp_args = imp.find_module(module_names[-1], [directory])
        fp = imp_args[0]
        return imp.load_module(path, *imp_args)
    except:  # nocv
        return None
    finally:
        fp.close() if fp else None


def import_class(path, directory=None):
    """
    Get class from string-path

    :param path: -- string containing full python-path
    :type path: str,unicode
    :return: -- return class or module in path
    :rtype: class, module, object
    """
    m_len = path.rfind(".")
    class_name = path[m_len + 1:len(path)]
    try:
        if directory is None:
            module = __import__(path[0:m_len], globals(), locals(), [class_name])
        else:
            module = import_module(path[0:m_len], directory)
        return getattr(module, class_name)
    except SystemExit:  # nocv
        return None  # nocv


class Modules(object):
    __slots__ = 'prefix', 'search_path', '_modules_list', '_key_filter'
    mod = ansible_modules

    def __init__(self, search_path=None, prefix='polemarch.project'):
        self.prefix = prefix
        self.search_path = os.path.abspath(search_path) if search_path else None
        self.clean()

    @property
    def mod_path(self):
        return self.search_path or self.mod.__path__[0] + "/"

    def _get_mod_list(self):
        # TODO: add cache between queries
        return self._modules_list

    def clean(self):
        self._modules_list = list()
        self._key_filter = None

    def _get_mods(self, files):
        return [
            f[:-3] for f in files
            if f[-3:] == ".py" and f[:-3] != "__init__" and "_" not in f[:2]
        ]

    def _get_info(self, key):  # nocv
        return key

    def _setup_key(self, key, files, search=None):
        _modules_list = list()
        _mods = self._get_mods(files)
        if self.search_path:
            key = self.prefix + key if key else self.prefix
        if _mods:
            for _mod in _mods:
                _mod_key = "{}.{}".format(key, _mod)
                if search is None or search.search(_mod_key):
                    info = self._get_info(_mod_key)
                    if info is not None:
                        _modules_list.append(info)
        return _modules_list

    def _filter(self, query):
        if self._key_filter == query:  # nocv
            return self._get_mod_list()
        self.clean()
        self._key_filter = query
        search = re.compile(query, re.IGNORECASE) if query else None
        for path, sub_dirs, files in os.walk(self.mod_path):
            if "__pycache__" in sub_dirs:
                sub_dirs.remove("__pycache__")  # nocv
            key = path.replace(self.mod_path, "").replace("/", ".")
            self._modules_list += self._setup_key(key, files, search)
        return self._get_mod_list()

    def get_mod_info(self, key, sub="DOCUMENTATION"):
        try:
            path_args = [self.mod.__name__, key, sub]
            directory = None
            if self.search_path:
                path_args = path_args[1:]
                directory = self.search_path
            path = '.'.join(path_args)
            return import_class(path, directory)
        except BaseException as exception_object:
            return exception_object

    def get(self, key=""):
        return self._filter(key)


class AnsibleModules(Modules):
    __slots__ = 'detailed',

    mod = ansible_modules

    def __init__(self, detailed=False, *args, **kwargs):
        super(AnsibleModules, self).__init__(*args, **kwargs)
        self.detailed = detailed

    def __get_detail_info(self, key, data):
        result = OrderedDict()
        result['path'] = key
        result['doc_data'] = data
        return result

    def _get_info(self, key):
        data = self.get_mod_info(key)
        if isinstance(data, BaseException) or data is None:
            return None
        if not self.detailed:
            return key
        return self.__get_detail_info(key, data)


def handler(args=sys.argv[1:], parser=get_parser()):
    default_cache_dir = '{}/pm_cache_ansible_{}'.format(gettempdir(), ansible_version)
    parser = parser
    parser.add_argument(
        '--detail', action='store_true', help='Get detailed info.'
    )
    parser.add_argument(
        '--get', type=str, default='',
        help='Get by key. Default return all keys.'
    )
    parser.add_argument(
        '--cachedir', type=str, default=default_cache_dir,
        help='Use filebased-cache. Default [{}]'.format(default_cache_dir)
    )
    parser.add_argument(
        '--path', type=str, default=[None], action='append',
        help='Additional path for modules searching.'
    )
    parser.add_argument(
        '--indent', type=int, default=None,
        help='Get indent json-output.'
    )
    _args = parser.parse_args(args)
    json.dump(get_from_cache(_args), sys.stdout, indent=_args.indent)
