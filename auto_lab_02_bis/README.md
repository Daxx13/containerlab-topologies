### What's this

A example CLAB lab that deploy 3 Nokia SR-Linux nodes doing OSPF, and 3 test hosts.
The goal is deploy infrastructure as code using ansible and the nokia.srlinux collection.

### Set up the environment

```bash
cd auto_lab_02_bis

# Install required dependencies
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv ansible_env

# Enable the python venv
source ansible_env/bin/activate

# Install dependencies inside venv
pip install ansible jinja2 requests ncclient xmltodict
ansible-galaxy collection install nokia.srlinux
ansible-galaxy collection install ansible.netcommon
```

### Start CLAB
```bash
sudo clab deploy --reconfigure
```

### Example usage:

```bash
ansible-inventory --list -i inventory
ansible-playbook playbooks/get_system_name_netconf.yml -i inventory
ansible-playbook playbooks/get_system_name_jsonrpc.yml -i inventory
ansible-playbook playbooks/set_base_config_jsonrpc.yml -i inventory
ansible-playbook playbooks/set_base_config_netconf.yml -i inventory

aios@dev-docker:~/clab/auto_lab_02_bis$ sudo docker exec -it clab-auto_lab_02_bis-pc3 ping 192.168.1.254
PING 192.168.1.254 (192.168.1.254): 56 data bytes
64 bytes from 192.168.1.254: seq=0 ttl=62 time=1.135 ms
64 bytes from 192.168.1.254: seq=1 ttl=62 time=0.606 ms
64 bytes from 192.168.1.254: seq=2 ttl=62 time=0.655 ms

aios@dev-docker:~/clab/auto_lab_02_bis$ sudo docker exec -it clab-auto_lab_02_bis-pc3 ping 192.168.2.254
PING 192.168.2.254 (192.168.2.254): 56 data bytes
64 bytes from 192.168.2.254: seq=0 ttl=62 time=1.802 ms
64 bytes from 192.168.2.254: seq=1 ttl=62 time=0.578 ms
64 bytes from 192.168.2.254: seq=2 ttl=62 time=0.635 ms
```

### Useful Links:

- [YANG Browser](https://learn.srlinux.dev/yang/browser/)
- [YANG Tree v24.10.1](https://yang.srlinux.dev/releases/v24.10.1/tree)
- [YANG v24.10.1](https://yang.srlinux.dev/v24.10.1)
- [Nokia SR Linux NETCONF Documentation](https://documentation.nokia.com/srlinux/24-10/books/system-mgmt/netconf.html)