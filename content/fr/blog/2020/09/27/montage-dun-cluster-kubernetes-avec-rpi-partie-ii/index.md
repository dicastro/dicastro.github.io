---
title: Montage d'un cluster Kubernetes avec Raspberry Pi (partie II)
summary: Deuxième partie d'une série où j'explique comment j'ai monté un cluster Kubernetes en utilisant des Raspberry Pi. Dans cet article, je décris quel système d'exploitation installer sur les nœuds et comment y installer Docker.
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
> Cette série est restée incomplète et je n'ai pour l'instant pas prévu de la poursuivre. Malgré tout, le contenu publié peut être utile.

Ceci est la deuxième partie d'une série d'articles dans laquelle j'explique comment j'ai monté un cluster Kubernetes en utilisant des Raspberry Pi. Ici, je décris quel système d'exploitation j'ai choisi pour les nœuds et comment j'y ai installé Docker.

| Partie                                                                  | Titre                                |
|-------------------------------------------------------------------------|--------------------------------------|
| [P01]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-i" >}})   | Matériel                             |
| **P02**                                                                 | **Système d'exploitation et Docker** |
| [P03]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-iii" >}}) | Cluster K3S                          |
| [P04]({{< ref "montage-dun-cluster-kubernetes-avec-rpi-partie-iv" >}})  | Consommation électrique              |

## Système d'exploitation

Une fois tout le matériel installé, la question suivante était : quel système d'exploitation installer sur les Raspberry Pi ? À ce moment-là, j'hésitais entre trois options :

- Raspbian
- Hypriot
- Ubuntu

*Raspbian* est la distribution officielle pour Raspberry Pi, et aurait pu être un bon choix. Cependant, je ne l'ai pas retenue, principalement parce qu'il n'existait pas encore de version finale 64 bits (seulement une bêta).

*Hypriot* était une distribution que je ne connaissais pas du tout et qui inclut Docker préinstallé, ce qui aurait simplifié l'installation. Mais je ne l'ai pas choisie non plus, pour la même raison que Raspbian : pas de version 64 bits.

Après avoir écarté ces deux options, j'ai commencé à douter de mon idée initiale d'installer une distribution 64 bits. Je pensais qu'une distribution 32 bits ne permettrait pas d'utiliser les 8 Go de RAM de la Raspberry. Après quelques recherches, je me suis rendu compte que ce n'était pas totalement vrai : une distribution 32 bits peut exploiter les 8 Go de RAM. Un seul processus du système ne peut utiliser que 4 Go au maximum, mais plusieurs processus peuvent ensemble utiliser les 8 Go. Malgré cela, j'ai maintenu mon idée initiale — commencer un nouveau projet aujourd'hui en 32 bits n'a pas vraiment de sens, même si cela apporte quelques petites "avantages".

Finalement, j'ai découvert que *Ubuntu* propose des distributions *ARM* et que celles-ci existent en 64 bits. Donc :

> Mesdames et messieurs, nous tenons notre vainqueur !

Avec le système choisi, les étapes suivantes étaient :

- flasher les 5 cartes SD
- mettre à jour et configurer les 5 Raspberry Pi
- installer Docker sur les 5 Raspberry Pi

C'est à ce moment-là que j'ai un peu regretté d'avoir acheté 5 Raspberry Pi, car tout devait être répété 5 fois. Si le processus est clair, il suffit de le suivre et de le répéter. Le problème survient lorsque le processus n'est pas encore parfaitement défini : chaque répétition tend à l'améliorer. Et c'est là que *mon obsession* entre en jeu : je ne serais pas capable d'utiliser des Raspberry Pi sachant qu'elles ne sont pas *strictement* identiques. Si, sur la dernière machine, je découvrais qu'il serait mieux de faire les choses autrement, je me sentirais obligé de tout refaire sur les quatre précédentes… Une spirale sans fin.

Avant de me lancer dans la configuration des Raspberry, j'ai cherché un moyen d'automatiser tout le processus, ce qui me permettrait de dormir sur mes deux oreilles en sachant que toutes les machines sont des *âmes sœurs* sans avoir à refaire tout manuellement pour la *brebis galeuse*. Et j'ai trouvé : [Cloud-Init](https://cloudinit.readthedocs.io) et [Ansible](https://docs.ansible.com).

## Cloud-Init

*Cloud-Init* est une technologie permettant d'initialiser une instance, incluse nativement dans Ubuntu. Cloud-Init détecte s'il s'agit du premier démarrage du système et, le cas échéant, permet de configurer : utilisateurs, clés SSH, partitions, réseau, etc. Cloud-Init peut récupérer ses instructions depuis le disque de l'instance ou via le réseau.

Dans mon cas, il récupère la configuration depuis la carte SD : une fois la carte flashée, j'y copie deux fichiers contenant les configurations. Concrètement, j'utilise Cloud-Init pour :

- mettre à jour les paquets du système
- définir le nom de l'instance
- configurer le DNS
- désactiver la création de l'utilisateur par défaut
- créer un utilisateur spécifique
- configurer une clé SSH
- désactiver l'accès par mot de passe
- configurer une IP statique
- installer des paquets supplémentaires : `curl`, `vim`, `git` et `aptitude`

Voici un exemple de fichier Cloud-Init pour un nœud du cluster :

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

La configuration réseau est définie dans un autre fichier ressemblant à ceci :

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

Pour flasher l'image du système, j'utilise [rpiimager](https://www.raspberrypi.org/blog/raspberry-pi-imager-imaging-utility), qui propose une interface graphique simple : choisir l'image, choisir la destination, lancer l'écriture. L'outil télécharge lui-même l'image si nécessaire.

Au premier démarrage, Cloud-Init s'exécute et applique la configuration. Il suffit d'attendre quelques minutes. Une personne attentive aura remarqué que deux paramètres diffèrent entre les Raspberry Pi : le nom d'hôte et l'IP statique. Chaque nœud a donc besoin d'un fichier de configuration distinct. C'est ici qu'intervient *Ansible*.

> Même si chaque Raspberry Pi possède une IP statique, il faut réserver cette adresse dans le routeur. Sinon, un autre appareil pourrait l'occuper pendant que le cluster est éteint.

## Ansible

En résumé, *Ansible* est un outil d'automatisation. À partir d'un fichier d'inventaire décrivant des machines et d'un fichier de tâches (*playbook*), il exécute ces tâches sur les machines. Les tâches sont *idempotentes* : si elles ont déjà été exécutées, Ansible ne les répète pas. Ceci est une simplification extrême, mais suffisante pour comprendre son utilisation dans ce projet.

Comme indiqué plus haut, j'ai utilisé Ansible non pas pour exécuter des tâches sur les machines, mais pour exploiter les données de l'inventaire et générer localement des fichiers de configuration Cloud-Init.

Voici un extrait du fichier d'inventaire :

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

L'inventaire est défini dans un fichier `INI`. Plusieurs groupes sont définis. Chaque machine possède son propre groupe, ce qui permet de faire référence individuellement à :

- rpicluster01
- rpicluster02
- rpicluster03
- rpicluster04
- rpicluster05

Un autre groupe contient toutes les machines :

- rpicluster

Chaque machine définit une propriété `custom_hostname` contenant son nom.

(Le fichier complet est disponible [ici](https://github.com/dicastro/rpicluster/blob/master/playbooks/inventory))

Voici maintenant le playbook Ansible qui génère les fichiers Cloud-Init :

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

Il comporte 3 tâches :

- créer un répertoire pour chaque machine
- générer le fichier `user-data` depuis un template
- générer le fichier `network-config` depuis un template

(Le playbook complet est disponible [ici](https://github.com/dicastro/rpicluster/tree/master/playbooks/00_cluster_regenerate_cloudinit_config))

### Installer Ansible sur Windows 10

Le moyen le plus simple d'utiliser Ansible sous Windows 10 est via WSL. Pour l'installer, j'ai utilisé `pip`. Il faut donc commencer par installer `pip3` ainsi que quelques dépendances :

```bash
sudo apt install -y python3-pip python3-dev libffi-dev libssl-dev
```

Puis installer Ansible (dans l'environnement utilisateur) :

```bash
pip3 install ansible --user
```

Enfin, mettre à jour le `PATH` :

```bash
echo 'PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
```

Voici quelques utilitaires que je recommande pour travailler avec Ansible :

```bash
pip3 install yamllint ansible-lint molecule
```

### Mettre à jour Ansible 2.9 vers 2.10

La version 2.10 d'Ansible est sortie récemment et comporte une importante restructuration des modules. Il est impossible de mettre à jour simplement la version installée : il faut d'abord désinstaller la 2.9 :

```bash
pip3 uninstall ansible ansible-base
```

Puis installer la nouvelle version :

```bash
pip3 install ansible --user
```

## Docker

Grâce à Ansible, l'installation de Docker sur toutes les machines a été extrêmement simple. J'ai trouvé un playbook—utilisé presque tel quel—qui installe Docker sur les systèmes Debian. La version que j'ai utilisée est disponible [ici](https://github.com/dicastro/rpicluster/tree/master/playbooks/02_cluster_install_docker).

## Conclusion

En conclusion, *Cloud-Init* et *Ansible* ont été deux très belles découvertes. Surtout Ansible, que je vois désormais comme un outil que je peux utiliser au quotidien à un niveau professionnel.

Le seul bémol que je trouve à Ansible est que certains aspects ne sont pas compatibles avec Windows. J'utilise actuellement Windows 10 et je peux utiliser Ansible sans grande difficulté via WSL. La seule véritable limitation concerne *Ansible Vault*, pour lequel certaines situations nécessitent de modifier les permissions de fichiers — ce qui n'est pas possible aujourd'hui dans WSL (ou du moins je n'ai pas trouvé comment).