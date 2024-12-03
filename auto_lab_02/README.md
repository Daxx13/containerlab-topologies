### What's this

A example CLAB lab that deploy 3 Nokia SR-Linux nodes doing OSPF, and 3 test hosts.
The goal is deploy infrastructure as code using ansible and the nokia.srlinux collection.

### Set up the environment

```bash
cd auto_lab_02

# Install required dependencies
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv ansible_env

# Enable the python venv
source ansible_env/bin/activate

# Install dependencies inside venv
pip install ansible jinja2 requests
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
ansible-playbook playbooks/get_system_name.yml -i inventory
ansible-playbook playbooks/set_base_config.yml -i inventory

sudo docker exec -it clab-auto_lab_02-pc3 traceroute -n 192.168.1.254
traceroute to 192.168.1.254 (192.168.1.254), 30 hops max, 46 byte packets
 1  192.168.3.1  1.423 ms  0.667 ms  0.818 ms
 2  99.1.3.1  1.329 ms  0.754 ms  0.940 ms
 3  192.168.1.254  0.502 ms  0.290 ms  0.341 ms
```

### Useful Links:

- [YANG Browser](https://learn.srlinux.dev/yang/browser/)
- [YANG Tree v24.10.1](https://yang.srlinux.dev/releases/v24.10.1/tree)
- [YANG v24.10.1](https://yang.srlinux.dev/v24.10.1)
- [Nokia SR Linux NETCONF Documentation](https://documentation.nokia.com/srlinux/24-10/books/system-mgmt/netconf.html)