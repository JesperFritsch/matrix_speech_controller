import docstring_parser
import re


def get_func_info(obj):
    """Get function information from its docstring """
    option_pattern = re.compile(r'- \"(.+?)\"')
    doc_obj = docstring_parser.parse(obj.__doc__)
    func_info = {}
    func_info["name"] = obj.__name__
    func_info["description"] = doc_obj.long_description
    func_info["parameters"] = []
    for param in doc_obj.params:
        param_info = {}
        param_info["name"] = param.arg_name
        param_info["type"] = param.type_name
        param_info["description"] = param.description
        if options := option_pattern.findall(param.description):
            param_info["options"] = options
        func_info["parameters"].append(param_info)
    return func_info
