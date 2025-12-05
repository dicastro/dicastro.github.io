---
title: Building a Kubernetes Cluster with Raspberry Pi (Part II)
summary: Second part of a series where I explain how I built a Kubernetes cluster using Raspberry Pi. In this article I describe which operating system to install on the nodes and how to install Docker on them.
date: 2020-09-27
lastmod: 2025-12-03
tags:
  - kubernetes
  - cluster
  - raspberry
  - docker
  - ubuntu
  - ansible
  - cloud-init
---

> [!WARNING]
> This series remained unfinished and I currently have no plans to continue it. Still, the published content may be useful.

This is the second part of a series of posts in which I explain how I built a Kubernetes cluster using Raspberry Pi. Here I describe which operating system I chose for the nodes and how I installed Docker on them.

| Part                                                             | Title                           |
|------------------------------------------------------------------|---------------------------------|
| [P01]({{< ref "building-kubernetes-cluster-with-rpi-part-i" >}}) | Hardware                        |
| **P02**                                                          | **Operating System and Docker** |
| [P03]({{< ref "building-kubernetes-cluster-with-rpi-part-iii" >}})  | K3S Cluster                     |
| [P04]({{< ref "building-kubernetes-cluster-with-rpi-part-iv" >}})   | Power Consumption               |

## Operating System

Once all the hardware was assembled, the next decision was which operating system to install on the Raspberry Pis. At that time, I was considering three options:

- Raspbian
- Hypriot
- Ubuntu

*Raspbian* is the official distribution for Raspberry Pi and would have been a good choice. However, I did not go with this option, mainly because at the time there was no final 64-bit version available (it was still in beta).

*Hypriot* was a distribution I didn’t know about and comes with Docker preinstalled, which would have simplified the installation process and saved time. But I didn’t choose it either, for the same reason as Raspbian: no 64-bit version.

After discarding both distributions, I began to doubt whether choosing a 64-bit OS was even necessary. Initially, I thought that with a 32-bit system I wouldn’t be able to take advantage of the 8 GB of RAM on the Raspberry Pi, which is why I insisted on 64-bit. After doing some research, I realized that this wasn’t entirely true: with a 32-bit distribution, the 8 GB of RAM *can* be used. A single process could use up to 4 GB, but multiple processes could collectively consume all 8 GB. Even so, I stuck with my initial plan of installing a 64-bit distribution, because it didn’t make sense to start a new project today using 32-bit, even if it had some small “advantages”.

Finally, I discovered that *Ubuntu* provides *ARM* distributions and that 64-bit images are available. So:

> Ladies and gentlemen, we have a winner!

With the operating system chosen, the next steps were:

- flash the 5 SD cards
- update and configure the 5 Raspberry Pis
- install Docker on the 5 Raspberry Pis

This is when I started regretting having bought 5 Raspberry Pis, because everything I needed to do had to be done 5 times. If you have a clear process, it’s just a matter of following it strictly and repeating it as needed. The problem appears when the process isn’t perfectly defined yet, and each repetition refines it. This refinement shouldn’t be a problem in itself. *The real problem is me and my obsession* with certain things. In this case, my obsession wouldn’t allow me to feel comfortable knowing that I hadn’t applied exactly the same process to all Raspberry Pis. If I discovered on the last one that something should have been done differently, I would feel compelled to redo everything on all of them. That’s where the situation could get out of control and waste a lot of time, with the *only advantage* being that all Raspberry Pis are identical.

Before configuring the Raspberry Pis, I looked for a way to automate the entire process, which would allow me to sleep peacefully knowing that all the devices were *perfect twins*, without manually repeating the process for the *black sheep* of the cluster. And the search paid off: I found [Cloud-Init](https://cloudinit.readthedocs.io) and [Ansible](https://docs.ansible.com).

## Cloud-Init

*Cloud-Init* is a tool used to initialize a system instance, and it comes bundled with Ubuntu. Cloud-Init detects whether it’s the first boot of a system, and if so, it takes action and allows configuring: users, ssh keys, disk partitions, network configuration, etc. Cloud-Init can obtain the actions to execute from the system’s disk or from the network.

In my case, it reads the configuration directly from the SD card: once the card is flashed, I copy a couple of configuration files onto it. Specifically, I use Cloud-Init to:

- update system packages
- set the instance hostname
- configure DNS
- disable creation of the OS default user
- create a custom user
- configure an SSH key for the user
- disable password login
- configure a static IP address
- install additional packages: `curl`, `vim`, `git` and `aptitude`

Here is an example of a Cloud-Init configuration file from one of the cluster nodes:

``` yaml
#cloud-config

preserve_hostname: false
hostname: rpicluster01
fqdn: rpicluster01.test

package_update: true
package_upgrade: true
package_reboot_if_required: true

manage_resolv_conf: true
resolv_conf:
  nameservers: ['8.8.4.4', '8.8.8.8']

users:
## Disable creation of default user
#- default
## Create user
- name: rpicluster
  homedir: /home/rpicluster
  lock_passwd: true
  shell: /bin/bash
  # Generate key with command: ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  ssh_authorized_keys:
    - **************************************************************************************
  sudo:
    - ALL=(ALL) NOPASSWD:ALL

## Disable password authentication with the SSH daemon
ssh_pwauth: false

## Install additional packages on first boot
packages:
- curl
- vim
- git
- aptitude

final_message: "The system is finally up, after $UPTIME seconds"
```

Network configuration is defined in a separate file that looks like this:

```yaml
# This file contains a netplan-compatible configuration which cloud-init
# will apply on first-boot. Please refer to the cloud-init documentation and
# the netplan reference for full details:
#
# https://cloudinit.readthedocs.io/
# https://netplan.io/reference
#
# Some additional examples are commented out below

version: 2
ethernets:
  eth0:
    dhcp4: false
    addresses: [192.168.86.51/24]
    gateway4: 192.168.86.1
    mtu: 1500
    nameservers:
      addresses: [8.8.4.4, 8.8.8.8]
    optional: true
#wifis:
#  wlan0:
#    dhcp4: true
#    optional: true
#    access-points:
#      myhomewifi:
#        password: "S3kr1t"
#      myworkwifi:
#        password: "correct battery horse staple"
#      workssid:
#        auth:
#          key-management: eap
#          method: peap
#          identity: "me@example.com"
#          password: "passw0rd"
#          ca-certificate: /etc/my_ca.pem
```

To flash the OS image onto the SD card, I use [rpiimager](https://www.raspberrypi.org/blog/raspberry-pi-imager-imaging-utility). This tool provides a very simple graphical interface: first select the image, then the destination, and finally start the writing process. The tool even downloads the OS image automatically.

When the Raspberry Pi boots for the first time, Cloud-Init activates and executes the configuration. All you need to do is wait a few minutes. A sharp observer may have noticed that two items on the configuration list are different for each node: setting the hostname and configuring the static IP. This means that each node requires a different configuration file. And this is where *Ansible* comes into play.

> Even though each Raspberry Pi is assigned a static IP, you should reserve these IPs in the router as well. Otherwise, another device might connect to the network while the cluster is powered off and claim one of those addresses.

## Ansible

To summarize, *Ansible* is an automation tool. Given an inventory file that defines a set of machines and a *playbook* that defines a set of tasks, Ansible executes the tasks on the machines. Additionally, task execution is *idempotent*: if a task has already been applied to a machine, Ansible will not run it again. This is a very simplified explanation of Ansible’s universe, but in this article I only want to explain the minimum necessary to understand how the tool was used to build the cluster.

As mentioned earlier, I used Ansible to generate the Cloud-Init configuration files. This is a somewhat unusual use case, because we’re not using Ansible to execute tasks on the machines but rather to process inventory data and generate configuration files locally.

Here is an excerpt from the inventory file:

```ini
[rpicluster01]
192.168.86.51

[rpicluster01:vars]
custom_hostname=rpicluster01


[rpicluster02]
192.168.86.52

[rpicluster02:vars]
custom_hostname=rpicluster02


[rpicluster03]
192.168.86.53

[rpicluster03:vars]
custom_hostname=rpicluster03


[rpicluster04]
192.168.86.54

[rpicluster04:vars]
custom_hostname=rpicluster04


[rpicluster05]
192.168.86.55

[rpicluster05:vars]
custom_hostname=rpicluster05


[rpicluster:children]
rpicluster01
rpicluster02
rpicluster03
rpicluster04
rpicluster05
```

The inventory is defined in an `INI` file. Several groups are defined. Each machine has its own group so that it can be referenced individually:

- rpicluster01
- rpicluster02
- rpicluster03
- rpicluster04
- rpicluster05

There is also a group containing all machines, representing the entire cluster:

- rpicluster

Each machine has a property `custom_hostname`, which contains the name of the machine.

(You can see the complete file [here](https://github.com/dicastro/rpicluster/blob/master/playbooks/inventory))

Below is the Ansible playbook that generates the Cloud-Init configuration files for the nodes:

```yaml
---
- hosts: rpicluster
  gather_facts: false
  tasks:
    - name: create directories
      file:
        path: "../../cloud-init/{{ hostvars[inventory_hostname]['custom_hostname'] }}"
        state: directory
      delegate_to: localhost

    - name: generate user-data config file from template
      template:
        src: template_userdata.j2
        dest: "../../cloud-init/{{ hostvars[inventory_hostname]['custom_hostname'] }}/user-data"
      delegate_to: localhost

    - name: generate network-config file from template
      template:
        src: template_networkconfig.j2
        dest: "../../cloud-init/{{ hostvars[inventory_hostname]['custom_hostname'] }}/network-config"
      delegate_to: localhost
```

It defines 3 tasks:

- Task 1 creates a directory for each machine in the inventory
- Task 2 generates the `user-data` file from a template
- Task 3 generates the `network-config` file from a template

(The complete playbook can be found [here](https://github.com/dicastro/rpicluster/tree/master/playbooks/00_cluster_regenerate_cloudinit_config))

### How to install Ansible on Windows 10

The easiest way to use Ansible on Windows 10 is through WSL. To install Ansible, I used `pip`, so the first step is installing `pip3` and some necessary dependencies:

```bash
sudo apt install -y python3-pip python3-dev libffi-dev libssl-dev
```

Then install Ansible (user-level installation):

```bash
pip3 install ansible --user
```

Finally, update the `PATH`:

```bash
echo 'PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
```

Here are some useful utilities I recommend installing when working with Ansible:

```bash
pip3 install yamllint ansible-lint molecule
```

### Updating Ansible 2.9 to 2.10

Version 2.10 of Ansible was recently released, and it includes a major module restructuring. Because of this, the update cannot be performed by simply upgrading the installed package. You must uninstall version 2.9:

```bash
pip3 uninstall ansible ansible-base
```

And then install the new version (2.10):

```bash
pip3 install ansible --user
```

## Docker

Thanks to Ansible, installing Docker on all machines was extremely simple. I found a playbook—used almost as-is—that installs Docker on Debian systems. The version I used can be found [here](https://github.com/dicastro/rpicluster/tree/master/playbooks/02_cluster_install_docker).

## Conclusion

In conclusion, both *Cloud-Init* and *Ansible* have been great discoveries. Especially Ansible, as I now see it as a tool I can start using daily in my professional work.

The only drawback I’ve found with Ansible is that some features are not compatible with Windows. I currently use Windows 10 and I’ve been able to use Ansible without major issues through WSL. The only problem I’ve encountered so far is with *Ansible Vault*, which requires modifying file permissions in some situations—something that isn’t possible in WSL today (or at least I haven’t found a way).