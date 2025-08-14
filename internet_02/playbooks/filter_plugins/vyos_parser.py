def vyos_parser(config):

    """
    Parses the configuration dictionary for VyOS in a recursive way and returns a array of arrays of strings
    The API request we will do is like that, we are generating the paths we will use later in the request:

    yaml input to this function:
        interfaces:
            ethernet:
                eth1:
                eth2:
                eth3:

        protocols:
        isis:
            level: level-2
            log-adjacency-changes:
            metric-style: wide
            interface:
            eth1:
                network: point-to-point
            eth2:
                network: point-to-point
            eth3:
                network: point-to-point
            dum0:
                passive:

    output of this function:
        [
            ['interfaces', 'ethernet', 'eth1'],
            ['protocols', 'isis', 'level-2'],
            ['protocols', 'segment-routing', 'interface', 'eth2', 'srv6']
            ...
        """

    def parse_dict(d, path=None):

        if path is None:
            path = []
        
        result = []
        
        for key, value in d.items():
            """
            If the value is a dictionary, we recursively call parse_dict.
            If the value is a list, we iterate through each item in the list and call parse
            parse_dict on each item.
            If the value is a string, we append the current path with the string value.
            """

            new_path = path + [ key ]
            
            if isinstance(value, dict):
                result.extend(parse_dict(value, new_path))
            elif isinstance(value, list):
                for item in value:
                    result.extend(parse_dict(item, new_path))
            elif isinstance(value, str):
                result.append(new_path + [value])
            else:
                result.append(new_path)

        return result

    return parse_dict(config)
    





# Expose the filter to Ansible as "vyos_parser".
class FilterModule(object):
    def filters(self):
        return {
            'vyos_parser': vyos_parser
        }