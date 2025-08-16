def vyos_parser(config):
    """
    Parses the configuration dictionary for VyOS in a recursive way and returns a array of arrays of strings
    The API request we will do is like that, we are generating the paths we will use later in the request:

    Loaded yaml input to this function:
        interfaces:
            dummy:
                dum0:
                    address:
                        - 2001:db8::1/128
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
                dum0:
                    passive:
        ...

    output of this function:
        [
            ['interfaces', 'ethernet', 'eth1'],
            ['interfaces', 'dummy', 'dum0', 'address', '2001:db8::1/128'],
            ['protocols', 'isis', 'level-2'],
            ['protocols', 'segment-routing', 'interface', 'eth2', 'srv6']
            ...
        """

    def parse_configuration(d, path=None):
        """
        Recursively parses the configuration dictionary and returns a list of paths.
        Each path is a list of strings representing the keys and values in the configuration.
        """

        if path is None:
            path = []

        if isinstance(d, dict):
            result = []
            for key, value in d.items():
                new_path = path + [ key ]
                result.extend(parse_configuration(value, new_path))
            return result
        
        elif isinstance(d, list):
            result = []
            for item in d:
                result.extend(parse_configuration(item, path))
            return result
        
        elif isinstance(d, str):
            return [path + [ d ]]

        elif isinstance(d, int):
            return [path + [ str(d) ]]
        
        elif d is None:
            return [path]
        
        else:
            raise TypeError(f"Unsupported type: {type(d)}")
    
    return parse_configuration(config)


# Expose the filter to Ansible as "vyos_parser".
class FilterModule(object):
    def filters(self):
        return {
            'vyos_parser': vyos_parser
        }