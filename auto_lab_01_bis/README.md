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

### Start CLAB
```bash
sudo clab deploy --reconfigure
```

#### Example usage:

```bash
python3 deploy.py --get system_name
python3 deploy.py --config all

sudo docker exec -it clab-auto_lab_01_bis-pc1 traceroute -n 192.168.2.254
traceroute to 192.168.2.254 (192.168.2.254), 30 hops max, 46 byte packets
 1  192.168.1.1  1.378 ms  0.565 ms  0.992 ms
 2  99.1.2.2  1.280 ms  0.843 ms  0.852 ms
 3  192.168.2.254  0.368 ms  0.407 ms  0.320 ms

sudo docker exec -it clab-auto_lab_01_bis-pc1 traceroute -n 192.168.3.254
traceroute to 192.168.3.254 (192.168.3.254), 30 hops max, 46 byte packets
 1  192.168.1.1  1.032 ms  0.561 ms  0.877 ms
 2  99.1.3.2  1.756 ms  0.847 ms  0.887 ms
 3  192.168.3.254  0.551 ms  0.495 ms  0.387 ms
```

#### Useful Links:

- [YANG Browser](https://learn.srlinux.dev/yang/browser/)
- [YANG Tree v24.10.1](https://yang.srlinux.dev/releases/v24.10.1/tree)
- [YANG v24.10.1](https://yang.srlinux.dev/v24.10.1)
- [Nokia SR Linux NETCONF Documentation](https://documentation.nokia.com/srlinux/24-10/books/system-mgmt/netconf.html)