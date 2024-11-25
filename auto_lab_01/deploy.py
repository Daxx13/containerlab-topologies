import argparse
import jinja2
import requests
import xmltodict

from ncclient import manager
from ncclient.xml_ import to_ele

from nornir import InitNornir
from nornir.core.task import Result
from nornir_utils.plugins.functions import print_result


################################
######## Main functions ########
################################


# This function will render a Jinja2 template
# with the provided configuration data
# and return the rendered template as a string
def render_template(template_name, config_data={}):
    """Render a Jinja2 template."""

    with open(f"templates/{template_name}") as file:
        template = file.read()
        
        # Load teplate and render it
        j2_template = jinja2.Template(template)
        rendered_template = j2_template.render(config_data)

        return rendered_template


# This function will perform a JSON-RPC call
# to the provided host, port, username, password, and template
# and return the JSON response
def json_rpc_call(host, port, username, password, template):
    """Perform a JSON-RPC call."""

    url = f"http://{host}:{port}/jsonrpc"
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=template, auth=(username, password))

    if response.status_code != 200:
        raise Exception(f"JSON-RPC Error: {response.status_code} {response.text}")

    return response.json()


# This function will perform a NETCONF call
# to the provided host, port, username, password, and template
# and return the parsed XML response as a dictionary
def netconf_call(host, port, username, password, template, commit=True):
    """Perform a NETCONF call."""

    with manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=False
    ) as m:
        response = m.dispatch( to_ele(template) )
        parsed_result = xmltodict.parse(xml_input=response.xml)

        if commit:
            commit_template = render_template("netconf/commit.xml")
            m.dispatch(to_ele(commit_template))

        return parsed_result
    

################################
######### Nornir tasks #########
################################


def get_system_name(task):
    if task.host.platform == "srlinux_jsonrpc":
        rendered_template = render_template("json_rpc/get_system_name.j2")
            
        result = json_rpc_call(
            host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
            template=rendered_template
        )

        return Result( host=task.host, changed=False,
            result=f"System name on {task.host.hostname} is {result['result'][0]['host-name']}"
        )
    
    elif task.host.platform == "srlinux_netconf":
        rendered_template = render_template("netconf/get_system_name.xml")

        result = netconf_call(
            host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
            template=rendered_template,
            commit=False
        )

        return Result( host=task.host, changed=False,
            result=f"System name on {task.host.hostname} is {result['rpc-reply']['data']['system']['name']['host-name']}"
        )
    
    else: return Result(host=task.host, failed=True, result=f"Unsupported task/platform: {task.host.hostname} on {task.host.platform}")


def configure_interfaces(task):
    if task.host.platform == "srlinux_jsonrpc":
        host_data = task.host.get("data", [])
        for interface in host_data["interfaces"]:

            rendered_template = render_template("json_rpc/update_interface.j2", config_data=interface)

            result = json_rpc_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed interfaces configuration on {task.host.hostname}"
        )
    
    elif task.host.platform == "srlinux_netconf":
        host_data = task.host.get("data", [])
        for interface in host_data["interfaces"]:

            rendered_template = render_template("netconf/update_interface.xml", config_data=interface)

            result = netconf_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed interfaces configuration on {task.host.hostname}"
        )
    
    else: return Result(host=task.host, failed=True, result=f"Unsupported task/platform: {task.host.hostname} on {task.host.platform}")


def configure_ipv4_subinterfaces(task):
    if task.host.platform == "srlinux_jsonrpc":
        host_data = task.host.get("data", [])
        for interface in host_data["ipv4_subinterfaces"]:

            rendered_template = render_template("json_rpc/update_ipv4_subinterface.j2", config_data=interface)

            result = json_rpc_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed IPv4 subinterfaces configuration on {task.host.hostname}"
        )
    
    elif task.host.platform == "srlinux_netconf":
        host_data = task.host.get("data", [])
        for interface in host_data["ipv4_subinterfaces"]:

            rendered_template = render_template("netconf/update_ipv4_subinterface.xml", config_data=interface)

            result = netconf_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed IPv4 subinterfaces configuration on {task.host.hostname}"
        )
    
    else: return Result(host=task.host, failed=True, result=f"Unsupported task/platform: {task.host.hostname} on {task.host.platform}")


def configure_network_instance_bindings(task):
    if task.host.platform == "srlinux_jsonrpc":
        host_data = task.host.get("data", [])
        for binding in host_data["interface_bindings"]:

            rendered_template = render_template("json_rpc/update_network_instance_subinterface.j2", config_data=binding)

            result = json_rpc_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed network instance bindings configuration on {task.host.hostname}"
        )
    
    elif task.host.platform == "srlinux_netconf":
        host_data = task.host.get("data", [])
        for binding in host_data["interface_bindings"]:

            rendered_template = render_template("netconf/update_network_instance_subinterface.xml", config_data=binding)

            result = netconf_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed network instance bindings configuration on {task.host.hostname}"
        )

    else: return Result(host=task.host, failed=True, result=f"Unsupported task/platform: {task.host.hostname} on {task.host.platform}")


def configure_ospf_instances(task):
    if task.host.platform == "srlinux_jsonrpc":
        host_data = task.host.get("data", [])
        for ospf_instance in host_data["ospf_instances"]:

            rendered_template = render_template("json_rpc/update_ospf_instance.j2", config_data=ospf_instance)

            result = json_rpc_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed OSPF instances configuration on {task.host.hostname}"
        )
    
    elif task.host.platform == "srlinux_netconf":
        host_data = task.host.get("data", [])
        for ospf_instance in host_data["ospf_instances"]:

            rendered_template = render_template("netconf/update_ospf_instance.xml", config_data=ospf_instance)

            result = netconf_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed OSPF instances configuration on {task.host.hostname}"
        )

    else: return Result(host=task.host, failed=True, result=f"Unsupported task/platform: {task.host.hostname} on {task.host.platform}")


def configure_ospf_area_interfaces(task):
    if task.host.platform == "srlinux_jsonrpc":
        host_data = task.host.get("data", [])
        for ospf_area_interface in host_data["ospf_area_interfaces"]:

            rendered_template = render_template("json_rpc/update_ospf_area_interface.j2", config_data=ospf_area_interface)

            result = json_rpc_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed OSPF area interfaces configuration on {task.host.hostname}"
        )
    
    elif task.host.platform == "srlinux_netconf":
        host_data = task.host.get("data", [])
        for ospf_area_interface in host_data["ospf_area_interfaces"]:

            rendered_template = render_template("netconf/update_ospf_area_interface.xml", config_data=ospf_area_interface)

            result = netconf_call(
                host=task.host.hostname, port=task.host.port, username=task.host.username, password=task.host.password,
                template=rendered_template
            )

        return Result( host=task.host, changed=True,
            result=f"Deployed OSPF area interfaces configuration on {task.host.hostname}"
        )
    
    else: return Result(host=task.host, failed=True, result=f"Unsupported task/platform: {task.host.hostname} on {task.host.platform}")


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Deploy configurations using JSON-RPC")

    # Add arguments
    parser.add_argument("-g", "--get", type=str, help="Type of config to deploy", required=False)
    parser.add_argument("-c", "--config", type=str, help="Type of config to get", required=False)
    parser.add_argument("-d", "--debug", help="Enable debug info", required=False, action="store_true")
    args = parser.parse_args()

    if args.debug:
        print("Debug mode is enabled!")

    # Initialize Nornir
    nr = InitNornir(config_file="config/nornir_config.yaml")

    # Run the task based on the provided arguments
    if args.get == "system_name":
        print("Getting system name")
        result = nr.run(task=get_system_name)
        print_result(result)

    elif args.config == "all":
        print("Deploying all configurations")
        
        result = nr.run(task=get_system_name)
        print_result(result)
        result = nr.run(task=configure_interfaces)
        print_result(result)
        result = nr.run(task=configure_ipv4_subinterfaces)
        print_result(result)
        result = nr.run(task=configure_network_instance_bindings)
        print_result(result)
        result = nr.run(task=configure_ospf_instances)
        print_result(result)
        result = nr.run(task=configure_ospf_area_interfaces)
        print_result(result)


    elif args.config == "interfaces":
        print("Deploying interfaces configuration")
        result = nr.run(task=configure_interfaces)
        print_result(result)

    elif args.config == "ipv4_subinterfaces":
        print("Deploying IPv4 subinterfaces configuration")
        result = nr.run(task=configure_ipv4_subinterfaces)
        print_result(result)

    elif args.config == "network_instance_bindings":
        print("Deploying network instance bindings configuration")
        result = nr.run(task=configure_network_instance_bindings)
        print_result(result)

    elif args.config == "ospf_instances":
        print("Deploying OSPF instances configuration")
        result = nr.run(task=configure_ospf_instances)
        print_result(result)

    elif args.config == "ospf_area_interfaces":
        print("Deploying OSPF area interfaces configuration")
        result = nr.run(task=configure_ospf_area_interfaces)
        print_result(result)

    else:
        print("No configuration to get/deploy")


if __name__ == "__main__":
    main()
