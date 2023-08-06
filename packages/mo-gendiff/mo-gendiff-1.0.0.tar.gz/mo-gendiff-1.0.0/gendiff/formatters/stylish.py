STATUSES = {
    'ADDED': '+',
    'DELETED': '-',
    'NESTED': ' ',
    'CHANGED': ' ',
    'UNCHANGED': ' '
}


def rend_stylish(diff):
    return walk(diff)


def get_string_value(value, depth):
    if isinstance(value, dict):
        lines = []
        for key, val in value.items():
            lines.append('{0}  {1}: {2}'.format(
                get_intend(depth + 1), key, get_string_value(val, depth + 1)
            ))
        result = '\n'.join(lines)
        return f"{{\n{result}\n{get_intend(depth)}  }}"
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value


def get_intend(depth):
    return (4 * depth + 2) * ' '


def walk(data, depth=0):
    result = []
    key = data.get('key')
    value = get_string_value(data.get('value'), depth)
    value1 = get_string_value(data.get('value1'), depth)
    value2 = get_string_value(data.get('value2'), depth)
    status = data.get('status')
    children = data.get('children')
    intend = get_intend(depth)
    if status == 'NESTED':
        lines = map(lambda child: walk(child, depth + 1), children)
        res = '\n'.join(lines)
        return f"{intend}  {key}: {{\n{res}\n{intend}  }}"
    if status == 'ADDED':
        return f'{intend}{STATUSES[status]} {key}: {value}'
    if status == 'DELETED':
        return f'{intend}{STATUSES[status]} {key}: {value}'
    if status == 'UNCHANGED':
        return f'{intend}{STATUSES[status]} {key}: {value}'
    if status == 'CHANGED':
        return f'{intend}- {key}: {value1}\n' \
            f'{intend}+ {key}: {value2}'
    if status == 'main':
        lines = map(lambda child: walk(child, depth), children)
        result = '\n'.join(lines)
    return f'{{\n{result}\n}}'
