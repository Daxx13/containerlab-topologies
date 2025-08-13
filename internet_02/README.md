### What's this

This lab demonstrates how to use [Containerlab](https://containerlab.dev/) and [Ansible](https://www.ansible.com/) to automate the deployment and configuration of a virtual internet topology using VyOS routers. It provides a reproducible environment for testing network automation workflows, experimenting with routing protocols, and learning about infrastructure-as-code practices in a controlled, containerized setup.

Current topology:

```
   [PE1]------[PE2]
     | \      / |
     |  \    /  |
     |   \  /   |
     |    \/    |
     |    /\    |
     |   /  \   |
     |  /    \  |
     | /      \ |
   [PE3]------[PE4]
```

### Set up the environment

```bash
cd internet_02

# Install required dependencies
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv ansible_env

# Enable the python venv
source ansible_env/bin/activate

# Install dependencies inside venv
pip install ansible paramiko
ansible-galaxy collection install vyos.vyos
ansible-galaxy collection install ansible.netcommon
```

### Start CLAB
```bash
sudo clab deploy --reconfigure
```

### Example usage:

```bash
ansible-inventory --list -i clab-internet_02/ansible-inventory.yml
ansible-inventory --list -i config/config.yml
ansible-inventory --list -i clab-internet_02/ansible-inventory.yml -i config/config.yml

ansible-playbook playbooks/deploy.yaml -i clab-internet_02/ansible-inventory.yml -i config/config.yml

```

### Useful Links:

- [VyOS Containerlab Kind](https://containerlab.dev/manual/kinds/vyosnetworks_vyos/)
- [VyOS Ansible collection](https://docs.ansible.com/ansible/latest/collections/vyos/vyos/index.html)
- [VyOS Ansible examples](https://docs.vyos.io/en/latest/configexamples/ansible.html)
- [VyOS SRv6 L3VPN reference guide](https://www.linkedin.com/posts/vyos_srv6-deployment-l3vpnvpnv6vpnv4-activity-7361003565294768130-pqyo)