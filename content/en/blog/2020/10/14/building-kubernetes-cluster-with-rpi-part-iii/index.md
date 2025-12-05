---
title: Building a Kubernetes Cluster with Raspberry Pi (Part III)
summary: Third part of a series where I explain how I built a Kubernetes cluster using Raspberry Pi. In this article I explain how to install Kubernetes with k3s.
date: 2020-10-14
lastmod: 2025-12-04
tags:
  - kubernetes
  - cluster
  - raspberry
  - k3s
---

> [!WARNING]
> This series remained unfinished and I currently have no plans to continue it. Still, the published content may be useful.

This is the third part of a series of posts in which I explain how I built a Kubernetes cluster using Raspberry Pi. Here I show how I install Kubernetes using k3s.

| Part                                                          | Title                       |
|--------------------------------------------------------------|-----------------------------|
| [P01]({{< ref "building-kubernetes-cluster-with-rpi-part-i" >}}) | Hardware                    |
| [P02]({{< ref "building-kubernetes-cluster-with-rpi-part-ii" >}}) | Operating System and Docker |
| **P03**                                                       | **K3S Cluster**             |
| [P04]({{< ref "building-kubernetes-cluster-with-rpi-part-iv" >}}) | Power Consumption           |

## K3s

[K3s](https://k3s.io/) is a certified Kubernetes distribution designed for the *IoT* and *[Edge Computing](https://en.wikipedia.org/wiki/Edge_computing)* world. K3s has been optimized for ARM (ARM64 and ARMv7), and this is what made me choose this distribution to install Kubernetes on the Raspberry Pi cluster. K3s drastically reduces dependencies, making it possible to distribute it as a single binary of less than 40 MB. Reducing dependencies also simplifies the installation process.

## Installation

The installation is very simple, since the K3s team has created an Ansible playbook to perform it. I based my setup on that playbook and applied a few small adaptations/improvements.

The first thing I did was adapt the inventory file to the playbook's requirements. To do this, I defined the groups:

- `k3s_master`: includes the master node
- `k3s_node`: includes the worker nodes
- `k3s_cluster`: includes all cluster members

```ini
[k3s_master:children]
rpicluster01

[k3s_node:children]
rpicluster02
rpicluster03
rpicluster04
rpicluster05

[k3s_cluster:children]
k3s_master
k3s_node
```

(You can see the full file [here](https://github.com/dicastro/rpicluster/blob/master/playbooks/inventory))

Below is the installation playbook:

```yaml
- hosts: k3s_cluster
  gather_facts: true
  become: true
  roles:
    - role: prereq
    - role: download
    - role: ubuntu

- hosts: k3s_master
  become: true
  roles:
    - role: k3s/master

- hosts: k3s_node
  become: true
  roles:
    - role: k3s/node
```

As you can see, it is based on the use of *roles*. There are 3 preparation roles (`prereq`, `download`, and `ubuntu`) that will run on all members of the cluster. These roles enable certain necessary system configurations and download the correct binary depending on the architecture being targeted.

Additionally, there is a role that runs on the master node and another that runs on the worker nodes. These roles are the ones that actually create the K3s cluster.

(You can see the full playbook [here](https://github.com/dicastro/rpicluster/tree/master/playbooks/03_cluster_k3s_cluster))

## Conclusion

Thanks to the K3s development team, who provides an Ansible playbook, it is possible to create a Kubernetes cluster in a very simple way.