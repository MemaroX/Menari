import psutil

def get_network_info():
    net_if_addrs = psutil.net_if_addrs()
    info = {}
    for interface_name, interface_addresses in net_if_addrs.items():
        info[interface_name] = []
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                info[interface_name].append({
                    "family": "IPv4",
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast
                })
            elif str(address.family) == 'AddressFamily.AF_INET6':
                info[interface_name].append({
                    "family": "IPv6",
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast
                })
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                info[interface_name].append({
                    "family": "MAC",
                    "address": address.address
                })
    return info

if __name__ == "__main__":
    import json
    print(json.dumps(get_network_info(), indent=2))