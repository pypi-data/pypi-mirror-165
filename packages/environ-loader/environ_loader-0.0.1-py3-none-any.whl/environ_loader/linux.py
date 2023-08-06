import os
import pathlib
from .var_list import var_list


def get_environ_vars_from_sh_file(file:str) -> var_list:
    """
    Load environment variables from a bash .sh file.
    """
    filepath = pathlib.Path(file)

    vars : var_list = var_list()

    text = filepath.read_text()
    lines = filter( lambda l: l is not None and len(l) > 0 and l.count("=") == 1, map(lambda l: l.strip(), text.strip().split("\n") ) )

    for line in lines:
        k:str
        v:str
        k,v = line.split("=")
        # pretty simple here. since we only support ${VAR} interpolation (not $VAR) right now, we can just remove the dollar signs.
        count : int = v.count("$")
        if count != v.count("${"):
            raise RuntimeError(f"Found '$' without following '{{' char in value for var {k}. This is probaby a $VAR style variable expansion, which is not supported yet.")
        v = v.replace("$","")

        vars.add(k,v)
        


    return vars


