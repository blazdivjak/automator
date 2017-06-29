# AUTOMATOR


**Author: Blaž Divjak, ARNES <blaz@arnes.si> <blaz@divjak.si>**
**Date: 1.11.2016**
**Version: v0.1**

Tool for uniform infrastructure for network and service management. Using **Ansible**, **OpenConfig**, **Django** and **AMQP** to simplify network automation.

## Architecture overview

![alt tag](https://dl.dropboxusercontent.com/u/318499/magistrska/automator_arhitektura_english.png)

## Configuration workflow

![alt tag](https://dl.dropboxusercontent.com/u/318499/magistrska/automator_arhitektura_workflow_english.png)

## Modules

**Inventory**

* Device types
* Device information
* Interfaces
* Switchport settings
* Networks
* Addresses
* Links

**ISC DHCP Service**

* DHCP Service for networks IPv4, IPv6
* Subnet and range
* Fixed hosts
* Custom Options
* IP Helper configuration

## REST API

Every module has its own API. It can be explored via. swagger gui interface at **/schema/** url address for each API.

* Authentication: /api/v1/auth/schema/
* Tenants: /api/v1/tenants/schema/
* Inventory: /api/v1/inventory/schema/
* DHCP service: /api/v1/dhcp/schema/

## Models

OpenConfig YANG models are used for network configuration data representation.
 
* interfaces
* vlan
* relay-agent

Custom models

* system configuration
* dhcp service configuration

## Roles

Includes roles for network devices and services.

**Services**

* dhcp
* elk

**Network devices**

* interfaces
* relay-agent
* system
* vlans

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

## User roles and permissions

**User roles**

* Admin - Staff inside user with permissions to all objects in database
* Technician: Technical person with a group that could have assigned special object and tenant permissions
* User - Normal user with permissions assigned for a specific Tenant and its objects (e.g. Devices, Projects, Locations, ...). Every user is a member of User group.

**Permissions**

Permissions can be assigned dynamicaly per object based on usecase. Supported permissions for each object. 

* Can view
* Can add
* Can change
* Can delete

Any user can have specific permissions asigned to them manualy using Django Admin interface od Django Shell. But it is discouraged ;).

_Additionaly based on serializer class defined for a specific view, different attributes can be modified for each object based on user permission_

**Permission assignment**
1. **ObjectPermission's:** As new object is added to tenant. Permissions are automaticaly assigned to **group** for this tenant. All users affiliated with this tenant are in the group.
2. **Admin's:** Have staff flag set in are staff and have full permissions for all objects in the database.

## Installation and configuration
 
### Easy and fast
For fast and easy startup use docker:
```
docker run -d -p 5672:5672 --name rabbitmq rabbitmq
docker build . -t automator
# build openconfig modules
docker run -d -p 8000:8000 -v $(pwd):/opt/automator --name automator automator
docker exec -it automator bash -c "cd lib/openconfig && ./openconfig.sh"
docker run -d -v $(pwd):/opt/automator --name celery automator celery -A automator worker -l info
docker run -d -p 5555:5555 -v $(pwd):/opt/automator --name flower automator celery -A automator flower --port=5555
```
 
SQLite is used for database by default and it is mounted to development directory.

Migrate database:
```
docker exec automator python manage.py migrate
```
Create superuser
```
docker exec -it automator python manage.py createsuperuser
```
Access the development environment: http://localhost:8000

Most common development copy-paste commands:
```
docker exec automator python manage.py reset_db --noinput
docker exec automator python manage.py test --noinput
docker exec automator python manage.py createcachetable
docker exec automator python manage.py collectstatic --noinput
```

### Dependencies for running native

Running service loccaly you will need:
* mysql

Hint: on macOS use `#brew install mysql`

**RabbitMQ server**

We recommend using official RabbitMQ container. Configure endpoint in settings.py.

```
#-----------------------------------------------
#AMQP
#-----------------------------------------------
BROKER_URL = 'amqp://guest@localhost//'
BACKEND_URL = 'amqp://guest@localhost//'
```
 
**Configure workspace for devel on your box**
Beware. Dragons inside. MAY Explode. Backup before starting and stand 5m away from your machine.
```bash
cd <automator_project_path>
./scripts/bootstrap_project.sh team-member
```

NOTE: We recommend using docker

**Configure Ansible environment**
Export Ansible configuration environment variable in Django project and Celery Daemon. Celery daemon should already be configured in automator/celery.py file. 
```
export ANSIBLE_CONFIG=/opt/laboratory/automator/ansible/ansible.cfg
```

**Enable Django signals before usage!!!!!!**
Change configuration in settings.py.
```
AUTOMATOR_ENABLE = True
```

## Develop

**Useful debug commands for development**
Cisco IOS debugging.
```
show archive config differences nvram:startup-config system:running-config
```

**Model image render**
Install pygraphviz to render model image.

```bash
sudo ports install graphviz-devel
pip install --install-option="--include-path=/opt/local/include" --install-option="--library-path=/opt/local/lib" pygraphviz
```
