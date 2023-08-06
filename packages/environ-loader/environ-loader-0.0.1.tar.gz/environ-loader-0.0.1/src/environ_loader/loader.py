import os
from collections import OrderedDict
from typing import MutableMapping
from .var_list import var_list


class dict_with_default_view:
    def __init__(self, store: MutableMapping[str, str], default: str = "") -> None:
        self.store = store
        self.default = default

    def __getitem__(self, k: str) -> str:
        if k in self.store:
            return self.store[k]
        return self.default


def load_vars_into_environment(
    vars: var_list, environ: MutableMapping[str, str] = os.environ, overwrite: bool = True
) -> None:
    """
    Load variables from 'vars' into dict-like environ (os.environ by default).
    """
    for k, v in vars.items():
        if not overwrite and k in environ:
            continue
        environ[k] = v.format_map(dict_with_default_view(environ))
