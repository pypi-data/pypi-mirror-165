from gendiff.formatters import stylish, plain, json


def formatter(data, format):
    if format == 'stylish':
        return stylish.rend_stylish(data)
    elif format == 'plain':
        return plain.rend_plain(data)
    elif format == 'json':
        return json.rend_json(data)
    raise ValueError(f'Try use another format, not {format}')
