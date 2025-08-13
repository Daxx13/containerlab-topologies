def deepmerge(a, b):
    if a is None:
        return b
    if b is None:
        return a

    # If both are dicts, merge them recursively
    if isinstance(a, dict) and isinstance(b, dict):
        merged = {}
        for k in set(a.keys()) | set(b.keys()):
            merged[k] = deepmerge(a.get(k), b.get(k))
        return merged

    # If both are lists, merge
    if isinstance(a, list) and isinstance(b, list):
        return a + [i for i in b if i not in a]

    # If different types, return b
    return b


class FilterModule(object):
    def filters(self):
        return {
            'deepmerge': deepmerge
        }