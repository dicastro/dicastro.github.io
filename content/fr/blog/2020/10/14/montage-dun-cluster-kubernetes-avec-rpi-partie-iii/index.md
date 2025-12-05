---
title: Montage d'un cluster Kubernetes avec Raspberry Pi (partie III)
summary: Troisième partie d'une série où j'explique comment j'ai monté un cluster Kubernetes en utilisant des Raspberry Pi. Dans cet article, j'explique comment installer Kubernetes avec k3s.
date: 2020-10-14
lastmod: 2025-12-04
tags:
  - kubernetes
  - cluster
  - raspberry
  - k3s
---

> [!WARNING]
> Cette série est restée incomplète et je n'ai pour l'instant pas prévu de la poursuivre. Malgré tout, le contenu publié peut être utile.

Ceci est la troisième partie d'une série d'articles dans laquelle j'explique comment j'ai monté un cluster Kubernetes en utilisant des Raspberry Pi. Ici je montre comment j'installe Kubernetes en utilisant k3s.

| Partie                                                                 | Titre                            |
|------------------------------------------------------------------------|----------------------------------|
| [P01]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-i" >}})  | Hardware                         |
| [P02]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-ii" >}}) | Système d'exploitation et Docker |
| **P03**                                                                | **Cluster K3S**                  |
| [P04]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-iv" >}}) | Consommation électrique          |

## K3s

[K3s](https://k3s.io/) est une distribution Kubernetes certifiée, conçue pour le monde de l'*IoT* et de l'*[Edge Computing](https://en.wikipedia.org/wiki/Edge_computing)*. K3s a été optimisé pour ARM (ARM64 et ARMv7), et c'est ce qui m'a poussé à choisir cette distribution pour installer Kubernetes sur mon cluster de Raspberry Pi. Les dépendances ont été réduites au minimum, ce qui permet de distribuer K3s sous la forme d'un seul binaire de moins de 40 MB. Cette réduction des dépendances simplifie également considérablement le processus d'installation.

## Installation

L'installation est très simple, car l'équipe de K3s fournit un playbook Ansible pour l'automatiser. Je me suis basé sur ce playbook et j'y ai apporté quelques petites adaptations/améliorations.

La première chose que j'ai faite a été d'adapter le fichier d'inventaire aux besoins du playbook. Pour cela, j'ai défini les groupes suivants :

- `k3s_master` : inclut le nœud maître
- `k3s_node` : inclut les nœuds esclaves
- `k3s_cluster` : inclut tous les membres du cluster

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

(le fichier complet est disponible [ici](https://github.com/dicastro/rpicluster/blob/master/playbooks/inventory))

Voici ensuite le playbook d'installation :

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

Comme on peut le voir, il repose sur l'utilisation de *rôles*. Trois rôles de préparation (`prereq`, `download` et `ubuntu`) sont exécutés sur tous les membres du cluster. Ces rôles activent certaines configurations nécessaires du système d'exploitation et téléchargent le binaire approprié en fonction de l'architecture.

Il existe également un rôle exécuté sur le nœud maître et un autre sur les nœuds esclaves. Ce sont eux qui créent réellement le cluster K3s.

(le playbook complet est disponible [ici](https://github.com/dicastro/rpicluster/tree/master/playbooks/03_cluster_k3s_cluster))

## Conclusion

Grâce à l'équipe de développement de K3s, qui fournit un playbook Ansible, il est possible de créer un cluster Kubernetes de manière très simple.