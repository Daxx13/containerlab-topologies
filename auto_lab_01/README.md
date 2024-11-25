#### What's this

A example CLAB lab that deploy 3 Nokia SR-Linux nodes doing OSPF, and 3 test hosts
The goal is deploy the configuration using Nornir framework and deploy the configuration using both JSON-RPC or NETCONF depending on the node.

#### Set up the environment

```bash
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv nornir_env
source nornir_env/bin/activate
pip install nornir nornir_utils jinja2 requests ncclient xmltodict
```

#### Example usage:

```bash
python3 deploy.py --get system_name
python3 deploy.py --config all
python3 deploy.py --config interfaces
python3 deploy.py --config ipv4_subinterfaces
python3 deploy.py --config network_instance_bindings
python3 deploy.py --config ospf_instances
python3 deploy.py --config ospf_area_interfaces
```

#### Useful Links:

- [YANG Browser](https://learn.srlinux.dev/yang/browser/)
- [YANG Tree v24.10.1](https://yang.srlinux.dev/releases/v24.10.1/tree)
- [YANG v24.10.1](https://yang.srlinux.dev/v24.10.1)
- [Nokia SR Linux NETCONF Documentation](https://documentation.nokia.com/srlinux/24-10/books/system-mgmt/netconf.html)