import re


def extract_forms(forms_str):
    result = []
    reg_form = re.compile('<form([\s\S]*?)>([\s\S]*?)</form>')
    form_strs = reg_form.findall(forms_str)
    for prop, param in form_strs:
        form = extract_form(prop, param)
        result.append(form)

    return result


def extract_form(prop_str, param_str):
    reg_name = re.compile('name="([\s\S]*?)"')
    name = reg_name.findall(prop_str)
    if len(name) > 0:
        name = name[0]
    else:
        name = None

    reg_action = re.compile('action="([\s\S]*?)"')
    action = reg_action.findall(prop_str)
    if len(action) > 0:
        action = action[0]
    else:
        action = None

    reg_method = re.compile('method="([\s\S]*?)"')
    method = reg_method.findall(prop_str)
    if len(method) > 0:
        method = method[0]
    else:
        method = None

    reg_input = re.compile('<(input)?(select)? ([\s\S]*?)>')
    input_strs = reg_input.findall(param_str)

    return {'name': name, 'action': action, 'method': method,
            'inputs': [extract_input(input_str) for input_str in input_strs]}


def extract_input(input_str):
    if isinstance(input_str, tuple):
        input_str = ' '.join(input_str)
    reg_name = re.compile('name="([\s\S]*?)"')
    name = reg_name.findall(input_str)
    if len(name) > 0:
        name = name[0]
    else:
        name = None

    reg_value = re.compile('value="([\s\S]*?)"')
    value = reg_value.findall(input_str)
    if len(value) > 0:
        value = value[0]
    else:
        value = None

    reg_type = re.compile('type="([\s\S]*?)"')
    type_ = reg_type.findall(input_str)
    if len(type_) > 0:
        type_ = type_[0]
    else:
        type_ = None

    return {'name': name, 'value': value, 'type': type_}


def generate_data(inputs):
    result = {}
    for i in inputs:
        if i['name'] not in result:
            result[i['name']] = i['value']

    return result
