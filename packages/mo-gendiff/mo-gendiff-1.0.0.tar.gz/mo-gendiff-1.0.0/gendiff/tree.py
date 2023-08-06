def make_diff(file_1, file_2):
    diff = []
    deleted_from_file_1 = file_1.keys() - file_2.keys()
    added_to_file_2 = file_2.keys() - file_1.keys()
    common_files_keys = sorted(file_1.keys() | file_2.keys())
    for key in common_files_keys:
        if key in added_to_file_2:
            diff.append({
                'key': key,
                'value': file_2.get(key),
                'status': 'ADDED'
            })
        elif key in deleted_from_file_1:
            diff.append({
                'key': key,
                'value': file_1.get(key),
                'status': 'DELETED'
            })
        elif isinstance(file_1.get(key), dict) and isinstance(file_2.get(key), dict):  # noqa
            diff.append({
                'key': key,
                'children': make_diff(file_1.get(key), file_2.get(key)),
                'status': 'NESTED'
            })
        elif file_1.get(key) == file_2.get(key):
            diff.append({
                'key': key,
                'value': file_1.get(key),
                'status': 'UNCHANGED'
            })
        elif file_1.get(key) != file_2.get(key):
            diff.append({
                'key': key,
                'value1': file_1.get(key),
                'value2': file_2.get(key),
                'status': 'CHANGED'
            })
    return diff


def diff(file_data1, file_data2):
    return {
        'status': 'main',
        'children': make_diff(file_data1, file_data2)
    }
