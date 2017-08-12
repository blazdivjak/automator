# AUTOMATOR 

## Author: Blaž Divjak <blaz@divjak.si>
## Date: 1.11.2016
## Version: v0.1

## Network device and service automation layer for network and service orchestration

### Roles

Includes Ansible roles for network devices and services.

### Services

* dhcp (isc dhcpd service)
* elk (automatic remediation service)

### Network device modules

* interfaces
* relay-agent
* system
* vlans

### Variables

Several variables could be defined, `group_vars` could be used for all hosts, `host_vars` are generated dynamically by the system and `host_vars_static` could be edited manually and override both of the previous. See example YAML structures below.

#### Network devices

Static YAML structure that can be placed inside `host_vars_static`.
```yaml
# ----------------------------------------------------------------------#
# Static YAML Structure for devices.
# ----------------------------------------------------------------------#
dns:
  name-servers:
    name-server:
    - 193.2.1.66
    - 193.2.1.72
    - 2001:1470:8000::66
    - 2001:1470:8000::72
  domain-name: test.arnes.si
aaa:
  users:
    user:
      admin:
        name: admin
        access-class: admin
        encrypted-password: xxx
        ssh-key: []
  radius:
    servers:
      server:        
          name: test
          address: 10.0.18.171
          auth-port: 1812
          acct-port: 1813
          timeout: 2
          retry: 1
          secret: xxx
snmp:
  communities:
    community:
      labcomm:
        community: test
        clients:
        - 10.0.18.160/27
        - 10.0.1.128/25
ntp:
  servers:
    server:
    - 88.200.0.160
    - 88.200.0.161
    - 88.200.0.162
    - 88.200.0.163
    - 193.2.1.92
    - 193.2.1.117
    - 2001:1470:8000::92
    - 2001:1470:8000::117  
logging:
  hosts:
    host:
    - 10.0.18.170
source_interface: vlan.100
local_routing:
  static-routes:
    0.0.0.0/0:
      route: 0.0.0.0/0
      next-hop: 10.0.79.201
ospf:
  area: 0    
```

Dynamicaly outputed YAML structure that is produced by automator system when something on the infrastructure changes. Its stored in `host_vars` and it is based on OpenConfig models and custom models.
```yaml
# ----------------------------------------------------------------------#
# Dynamicaly outputed YAML structure based on OpenConfig models 
# and custom models.
# ----------------------------------------------------------------------#
interfaces:
  interface:
    ge-0/0/0:
      config:
        description: ge-0/0/0
        type: ethernetCsmacd
      name: ge-0/0/0
    ge-0/0/1:
      config:
        description: ge-0/0/1
        type: ethernetCsmacd
      ethernet:
        switched-vlan:
          config:
            access-vlan: 5
            interface-mode: ACCESS
      name: ge-0/0/1
    ge-0/0/10:
      config:
        description: ge-0/0/10
        type: ethernetCsmacd
      name: ge-0/0/10
    ge-0/0/11:
      config:
        description: ge-0/0/11
        type: ethernetCsmacd
      ethernet:
        switched-vlan:
          config:
            interface-mode: TRUNK
            native-vlan: 4
            trunk-vlans:
            - 5
      name: ge-0/0/11
    ge-0/0/12:
      config:
        description: ge-0/0/12
        type: ethernetCsmacd
      name: ge-0/0/12
    ge-0/0/13:
      config:
        description: ge-0/0/13
        type: ethernetCsmacd
      name: ge-0/0/13
    ge-0/0/14:
      config:
        description: ge-0/0/14
        type: ethernetCsmacd
      name: ge-0/0/14
    ge-0/0/15:
      config:
        description: ge-0/0/15
        type: ethernetCsmacd
      name: ge-0/0/15
    ge-0/0/16:
      config:
        description: ge-0/0/16
        type: ethernetCsmacd
      name: ge-0/0/16
    ge-0/0/17:
      config:
        description: ge-0/0/17
        type: ethernetCsmacd
      name: ge-0/0/17
    ge-0/0/18:
      config:
        description: ge-0/0/18
        type: ethernetCsmacd
      name: ge-0/0/18
    ge-0/0/19:
      config:
        description: ge-0/0/19
        type: ethernetCsmacd
      name: ge-0/0/19
    ge-0/0/2:
      config:
        description: ge-0/0/2
        type: ethernetCsmacd
      ethernet:
        switched-vlan:
          config:
            access-vlan: 5
            interface-mode: ACCESS
      name: ge-0/0/2
    ge-0/0/20:
      config:
        description: ge-0/0/20
        type: ethernetCsmacd
      name: ge-0/0/20
    ge-0/0/21:
      config:
        description: ge-0/0/21
        type: ethernetCsmacd
      name: ge-0/0/21
    ge-0/0/22:
      config:
        description: ge-0/0/22
        type: ethernetCsmacd
      name: ge-0/0/22
    ge-0/0/23:
      config:
        description: ge-0/0/23
        type: ethernetCsmacd
      ethernet:
        switched-vlan:
          config:
            interface-mode: TRUNK
            trunk-vlans:
            - 2
            - 3
            - 4
            - 5
            - 100
      name: ge-0/0/23
    ge-0/0/3:
      config:
        description: ge-0/0/3
        type: ethernetCsmacd
      ethernet:
        switched-vlan:
          config:
            access-vlan: 5
            interface-mode: ACCESS
      name: ge-0/0/3
    ge-0/0/4:
      config:
        description: ge-0/0/4
        type: ethernetCsmacd
      name: ge-0/0/4
    ge-0/0/5:
      config:
        description: ge-0/0/5
        type: ethernetCsmacd
      name: ge-0/0/5
    ge-0/0/6:
      config:
        description: ge-0/0/6
        type: ethernetCsmacd
      name: ge-0/0/6
    ge-0/0/7:
      config:
        description: ge-0/0/7
        type: ethernetCsmacd
      name: ge-0/0/7
    ge-0/0/8:
      config:
        description: ge-0/0/8
        type: ethernetCsmacd
      name: ge-0/0/8
    ge-0/0/9:
      config:
        description: ge-0/0/9
        type: ethernetCsmacd
      name: ge-0/0/9
    lo0:
      config:
        description: lo0
        type: softwareLoopback
      name: lo0
      subinterfaces:
        subinterface:
          '0':
            index: '0'
    me0:
      config:
        description: me0
        type: other
      name: me0
    vlan.1:
      config:
        description: -- management --
        type: propVirtual
      name: vlan.100
      routed-vlan:
        config:
          vlan: 100
        ipv4:
          addresses:
            address:
              10.0.79.204:
                config:
                  ip: 10.0.79.204
                  prefix-length: 29
                ip: 10.0.79.204
relay_agent: {}
system:
  active: true
  description: sbravos2.arnes.si
  hostname: sbravos2.arnes.si
  inventory_number: 6
  managed: true
  model: EX2200-24T-4G
  os: junos
  serial_number: CW0212465586
  tenant_id: 3
  tenant_name: Braavos
  usage: ACCESS
  vendor: juniper
  version: 14.1X53-D26.2
vlans:
  vlan:
    '2':
      config:
        name: pedagosko
      vlan-id: '2'
    '3':
      config:
        name: admin
      vlan-id: '3'
    '4':
      config:
        name: management
      vlan-id: '4'
    '5':
      config:
        name: eduroam
      vlan-id: '5'
    '100':
      config:
        name: 100
      vlan-id: '100'

```

#### DHCP service and ELK service
Static YAML structure that can be placed inside `host_vars_static`.
```yaml
ansible_connection: ssh
ansible_user: root
ansible_ssh_pass: xxx
static_configuration_folder: /etc/dhcpd.conf.d/
static_configuration_files:
  v4: /etc/dhcpd.conf.d/static4.conf
  v6: /etc/dhcpd.conf.d/static6.conf
pattern_folder: /etc/logstash/patterns/  
elastalert_configuration_folder: /opt/elastalert.conf.d/ 
```

## Playbooks

Includes playbooks for network device and service provisioning.

**Example playbook runs**

Get network device facts.

```
ansible-playbook get_facts.yml --inventory-file develop --limit sbravos2.arnes.si
```

Generate configuration for network device.

```
ansible-playbook config_generate.yml --inventory-file develop --limit sbravos2.arnes.si
```

Get diff between latest generated configuration and configuration on device. Diff is stored inside __configuration/__ folder. 

```
ansible-playbook config_diff.yml --inventory-file develop --limit sbravos2.arnes.si
```

Install configuration on network device.

```
ansible-playbook config_install.yml --inventory-file develop --limit sbravos2.arnes.si
```

Provision server for ISC DHCP service.
```
ansible-playbook provision_dhcp.yml --inventory-file infrastructure --limit dhcp
```

Provision server running elastic stack and automatic remediation scripts in elastalert service.
```
ansible-playbook provision_elk.yml --inventory-file infrastructure --limit elk
```

