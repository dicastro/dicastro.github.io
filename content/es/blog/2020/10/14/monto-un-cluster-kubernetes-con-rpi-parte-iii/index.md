---
title: Monto un cluster Kubernetes con Raspberry Pi (parte III)
summary: Tercera parte de una serie donde explico cómo he montado un cluster de Kubernetes utilizando Raspberry Pi. En esta tercera entrega explico cómo instalar kubernetes con k3s.
date: 2020-10-14
lastmod: 2025-12-04
tags:
  - kubernetes
  - cluster
  - raspberry
  - k3s
---

> [!WARNING]
> Esta serie quedó incompleta y por ahora no tengo previsto continuarla. Aun así, el contenido publicado puede ser útil.

Esta es la tercera parte de una serie de posts en la que explico cómo he montado un cluster de Kubernetes utilizando Raspberry Pi. Aquí muestro cómo instalo kubernetes utilizando k3s.

| Parte                                                             | Título                     |
|-------------------------------------------------------------------|----------------------------|
| [P01]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-i" >}})  | Hardware                   |
| [P02]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-ii" >}}) | Sistema Operativo y Docker |
| **P03**                                                           | **Cluster K3S**            |
| [P04]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iv" >}}) | Consumo eléctrico          |

## K3s

[K3s](https://k3s.io/) es una distribución de kubernetes certificada que ha sido concebida para el mundo *IoT* y *[Edge Computing](https://en.wikipedia.org/wiki/Edge_computing)*. K3s ha sido optimizada para ARM (ARM64 y ARMv7) y esto es lo que ha hecho decidirme por esta distribución para instalar kubernetes en el cluster de raspberry pi. En K3s se han reducido las dependencias al máximo, haciendo posible que se distribuya como un único binario de menos de 40 MB. La reducción de dependencias también ha supuesto una simplificación del proceso de instalación.

## Instalación

La instalación es muy sencilla, ya que el equipo de K3s ha creado un *playbook* de Ansible para realizarla. Yo me he basado en dicho playbook y he realizado alguna pequeña adaptación/mejora.

Lo primero que he realizado ha sido adaptar el fichero de inventario a las necesidades del playbook, para ello he definido los grupos:

- `k3s_master`: que incluye el nodo maestro
- `k3s_node`: que incluye los nodos esclavos
- `k3s_cluster`: que incluye todos los miembros del cluster

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

(se puede ver el fichero completo [aquí](https://github.com/dicastro/rpicluster/blob/master/playbooks/inventory))

A continuación se muestra el playbook de instalación:

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

Como se puede observar, se basa en el uso de *roles*. Existen 3 roles de preparación (`prereq`, `download` y `ubuntu`) que se ejecutarán sobre todos los miembros del cluster. Estos roles se encargan de activar algunas configuraciones necesarias en el sistema operativo, así como de realizar la descarga del binario en función de la arquitectura sobre la que se esté realizando la instalación.

Además existe un role que se ejecutará sobre el nodo maestro y otro que se ejecutará sobre los nodos esclavos. Estos roles son los que crean el cluster K3s propiamente dicho.

(se puede ver el playbook completo [aquí](https://github.com/dicastro/rpicluster/tree/master/playbooks/03_cluster_k3s_cluster))

## Conclusión

Gracias al equipo de desarrollo de K3s, que nos proporciona un playbook de Ansible, se puede crear un cluster de kubernetes de una manera muy sencilla.