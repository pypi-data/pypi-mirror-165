import os
import pathlib
from .var_list import var_list
import typing


def get_environ_vars_from_bat_file(file:str) -> var_list:
    """
    Load environment variables from a Windows .bat file.
    """
    filepath = pathlib.Path(file)

    vars : var_list = var_list()

    text = filepath.read_text()
    lines = filter( lambda l: l is not None and len(l) > 0 and l.count("=") == 1, map(lambda l: l.strip(), text.strip().split("\n") ) )

    for line in lines:
        k:str
        v:str
        k,v = line.split("=")
        # I know, we should probably just be using pyparsing here...
        count : int = v.count("%")
        if count % 2:
            raise RuntimeError(f"Found an odd number of '%' chars in value for var {k}. I do not know how to handle this, so it is not supported yet.")
        if v.count("%") > 1:
            count = 0
            mutable_v : typing.List[str] = [ c for c in v ]
            for i in range(len(mutable_v)):
                if mutable_v[i] == '%':
                    if count % 2 == 0:
                        mutable_v[i] = '{'
                    else:
                        mutable_v[i] = '}'
                    count += 1
            v = "".join(mutable_v)

        vars.add(k,v)
        


    return vars


