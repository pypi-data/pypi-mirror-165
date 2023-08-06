import ast
import copy
import inspect
import sys
from collections import ChainMap
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class DefaultValue:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


def get_default_value(lines: List[str], position: ast.AST) -> Optional[str]:
    try:
        if sys.version_info < (3, 8):  # only for py38+
            return None
        elif position.lineno == position.end_lineno:
            line = lines[position.lineno - 1]
            return line[position.col_offset : position.end_col_offset]
        else:
            # multiline value is not supported now
            return None
    except (AttributeError, IndexError):
        return None


def get_function_def(obj: Any) -> ast.FunctionDef:
    """Get FunctionDef object from living object.
    This tries to parse original code for living object and returns
    AST node for given *obj*.
    """
    try:
        source = inspect.getsource(obj)
        if source.startswith((" ", r"\t")):
            # subject is placed inside class or block.  To read its docstring,
            # this adds if-block before the declaration.
            module = ast.parse("if True:\n" + source)
            return module.body[0].body[0]  # type: ignore
        else:
            module = ast.parse(source)
            return module.body[0]  # type: ignore
    except (OSError, TypeError):  # failed to load source code
        return None


def remove_extra_attributes_from_sls_data(hub, sls_data_original: Dict[str, Any]):
    sls_data = copy.deepcopy(sls_data_original)
    for item in sls_data:
        resource_attributes = list(sls_data[item].values())[0]
        dict(ChainMap(*resource_attributes))
        resource_type = list(sls_data[item].keys())[0]
        func_obj = hub.idem_codegen.tool.remove_extra_attributes.get_func(resource_type)
        parameters = list(inspect.signature(func_obj).parameters.values())
        params_names = [params_obj.name for params_obj in parameters]
        resource_attributes_copy = copy.deepcopy(resource_attributes)

        for resource_attribute in resource_attributes_copy:
            resource_attribute_copy = copy.deepcopy(resource_attribute)
            for resource_attribute_key in resource_attribute_copy:
                if resource_attribute_key not in params_names:
                    if len(resource_attribute) > 1:
                        for resource_attribute_key_1 in resource_attribute_copy:
                            if (
                                resource_attribute_key_1 not in params_names
                                and resource_attribute_key_1 in resource_attribute
                            ):
                                resource_attribute.pop(resource_attribute_key_1)
                    else:
                        resource_attributes.remove(resource_attribute)
    return sls_data


def get_func(hub, resource_path):
    """
    Given the function , determine what function
    on the hub that can be run
    """
    func = getattr(hub, "states." + resource_path)
    return func
