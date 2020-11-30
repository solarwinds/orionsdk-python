# Linux Startup and Shutdown scripts

Scripts in this folder can be used to add machine to the Orion while it is starting and removing it on the machine shutdown.

Additionally scripts are able to deploy agent on startup and uninstall/remove on shutdown.
* Startup script contains flag `deploy_agent`. If this flag is set to `True` agent will be deployed. Also credentials for Linux machine need to be populated.
* Shutdown script contains flag `should_uninstall_agent_from_node`. If this flag is set to `True` agent will be uninstalled from monitored node. Otherwise only information about agent will be removed from Orion. 

All scripts were tested on SolarWinds vRa Machines, both Ubuntu 18.04 and CentOS 8.

## Prerequisites

### Python

Linux machine have installed `python` and `pip` for the administrator/root account.

* for Ubuntu you can achieve it by
  * `apt install python` or `apt install python3`
  * `apt install python-pip` or `apt install python3-pip`
* for CentOS 8 both required packages were preinstalled on vRa image.

### Python packages

Two packages are required by startup script

* [orionsdk](https://github.com/solarwinds/orionsdk-python)
* [netifaces](https://github.com/al45tair/netifaces)

Depend on pip version it can be achieved by executing

```bash
pip install orionsdk
pip install netifaces
```

or

```bash
pip3 install orionsdk
pip3 install netifaces
```

### Linux machine setup

System hostname of Orion node needs to be added to /etc/hosts

## Script setup

Based on [https://transang.me/create-startup-scripts-in-ubuntu/] adding startup and shutdown scripts to the system:

1. Create folder /home/orionscripts/
2. Add to this folder [startup.sh](./startup.sh), [startup.py](./startup.py), [shutdown.sh](./shutdown.sh) and [shutdown.py](./shutdown.py)
    * If you are using `python3` instead of `python` please modify the `startup.sh` and `shutdown.sh`. Replace `python` by `python3`.
3. In `startup.py` and `shutdown.py` put Orion server settings and selected network interface to detect local ip
4. Add execute permissions for startup.sh and shutdown.sh file by `chmod +x startup.sh` and `chmod +x shutdown.sh`
5. To `/etc/systemd/system` copy [orion-startup.service](./orion-startup.service) and [orion-shutdown.service](./orion-shutdown.service)
6. Execute `systemctl enable orion-startup.service` and `systemctl enable orion-shutdown.service`
    * CentOS - if you encountered issues with above commands try to execute `chcon system_u:object_r:systemd_unit_file_t:s0 orion-startup.service` and `chcon system_u:object_r:systemd_unit_file_t:s0 orion-shutdown.service`.
7. Restart machine

If you want to make sanity check for python configuration. Switch account to root/administration then execute `python shutdown.py` or `python startup.py`
