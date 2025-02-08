import docstring_parser
import re


def get_tool_definition(obj):
    """Get function information from its docstring """
    doc_obj = docstring_parser.parse(obj.__doc__)
    required_params = []
    fn_props = {}
    for param in doc_obj.params:
        param_info = {}
        param_info["name"] = param.arg_name
        param_info["type"] = param.type_name
        param_info["description"] = param.description
        fn_props[param.arg_name] = param_info
        required_params.append(param.arg_name)
    tool_info = {
        "type": "function",
        "function": {
            "name": obj.__name__,
            "description": doc_obj.long_description,
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": fn_props,
                "required": required_params,
                "additionalProperties": False,
            }
        }
    }
    return tool_info
