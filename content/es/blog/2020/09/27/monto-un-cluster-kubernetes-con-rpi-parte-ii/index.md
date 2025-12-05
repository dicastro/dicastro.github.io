---
title: Monto un cluster Kubernetes con Raspberry Pi (parte II)
summary: Segunda parte de una serie donde explico cómo he montado un cluster de Kubernetes utilizando Raspberry Pi. En esta entrega describo qué sistema operativo instalar en los nodos y cómo instalar Docker en ellos.
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
> Esta serie quedó incompleta y por ahora no tengo previsto continuarla. Aun así, el contenido publicado puede ser útil.

Esta es la segunda parte de una serie de posts en la que explico cómo he montado un cluster de Kubernetes utilizando Raspberry Pi. Aquí describo qué sistema operativo elegí para los nodos y cómo instalé Docker en ellos.

| Parte                                                              | Título                         |
|--------------------------------------------------------------------|--------------------------------|
| [P01]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-i" >}})   | Hardware                       |
| **P02**                                                            | **Sistema Operativo y Docker** |
| [P03]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iii" >}}) | Cluster K3S                    |
| [P04]({{< ref "monto-un-cluster-kubernetes-con-rpi-parte-iv" >}})  | Consumo eléctrico              |

## Sistema Operativo

Una vez que todo el hardware está montado la siguiente decisión a tomar es qué sistema operativo instalar en las Raspberry. En el momento de tomar la decisión barajaba 3 opciones:

- Raspbian
- Hypriot
- Ubuntu

*Raspbian* es la distribución oficial para raspberry, y sería una buena elección. Sin embargo, no me he decantado por esta opción, y la razón principal es que en el momento de tomar la decisión no había una versión final de 64 bits (estaba en beta).

*Hypriot* es una distribución que desconocía totalmente y que viene con docker preinstalado, lo cual simplificaría el proceso de instalación y supondría un ahorro de tiempo. Tampoco me he decidido por esta opción, y el motivo es el mismo que con *Raspbian*, no existe una versión de 64 bits.

Tras haber descartado las dos distribuciones anteriores me entró la duda de si mi idea inicial de instalar una distribución de 64 bits era una buena idea. Inicialmente pensaba que con una distribución de 32 bits no podría aprovechar los 8 GB de RAM de las raspberry y de ahí que buscase una distribución de 64 bits. Tras investigar un poco, me di cuenta de que esto no era cierto del todo, con una distribución de 32 bits sí que se aprovecharían los 8 GB de RAM. Un mismo proceso del sistema operativo podría usar como mucho 4 GB de RAM, pero entre varios procesos se podrían consumir los 8 GB. Aún así, mantuve mi idea inicial de instalar una distribución de 64 bits, creo que no tiene sentido a día de hoy comenzar un proyecto optando por 32 bits, aunque esta elección traiga ciertas "ventajas" inicialmente.

Finalmente descubrí que *Ubuntu* tiene distribuciones para *ARM* y que estas pueden ser de 64 bits. Así que:

> Señores, ¡Ya tenemos caballo ganador!

Con el sistema operativo elegido lo siguiente era:

- flashear las 5 tarjetas de memoria
- actualizar y realizar ciertas configuraciones en las 5 raspberry
- instalar Docker en las 5 raspberry

En estos momentos me arrepentí un poco de haber comprado 5 raspberry porque todo lo que fuese a hacer lo tenía que repetir 5 veces. Si tienes claro el proceso, es cuestión de seguirlo a pies juntillas y repetirlo las veces que sea necesario. El problema viene cuando el proceso no está claramente definido, y con cada repetición se va refinando el mismo. Este "ir refinando el proceso a medida que lo vas repitiendo" no debería ser algo problemático. El problema radica en mi persona y mi obsesión con algunas cosas, y en este caso mi obsesión no me permitiría sentirme cómodo sabiendo que no he ejecutado el mismo proceso en todas las raspberry. Si cuando estoy en la última raspberry me doy cuenta de que sería mejor hacer algo de forma diferente, me vería obligado a volver a hacerlo en todas las raspberry. Aquí es donde la situación podría descontrolarse y llevarme muchísimo más tiempo del necesario con la *única ventaja* de tener todas las rapberry exactamente iguales.

Antes de lanzarme a configurar las raspberry busqué la forma de automatizar todo el proceso de configuración, lo cual me permitiría dormir tranquilo sabiendo que todas las raspberry son *almas gemelas* sin tener que repetir manualmente el proceso de configuración por enésima vez sobre la *oveja negra del rebaño*. Y la búsqueda fue fructífera, me topé con [Cloud-Init](https://cloudinit.readthedocs.io) y con [Ansible](https://docs.ansible.com).

## Cloud-Init

*Cloud-Init* es una tecnología que permite inicializar una instancia y que viene de caja con Ubuntu. Cloud-Init detecta si es el primer arranque del sistema y si es el caso entra en acción permitiendo configurar: usuarios, claves ssh, particiones de disco, configuración de red, etc. Cloud-Init puede obtener las acciones que tiene que ejecutar del propio disco de la instacia o podría obtenerlo a través de la red.

En mi caso, las acciones a actualizar las obtiene del propio disco: una vez flasheada la tarjeta SD copio un par de ficheros en la tarjeta con las configuraciones a realizar. Concretamente utilizo cloud-init para:

- actualizar los paquetes del sistema
- establecer el nombre de la instancia
- configurar el DNS
- desactivar la creación del usuario por defecto del sistema operativo
- crear un usuario específico
- establecer una clave SSH para el usuario
- deshabilitar el acceso al sistema con contraseña
- configuración de una ip fija
- instalación de paquetes adicionales: `curl`, `vim`, `git` y `aptitude`

Este es un ejemplo de fichero de configuración de cloud-init de uno de los nodos del cluster:

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

La configuración de red se establece en otro fichero diferente que tiene la siguiente pinta:

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

Para flashear la imagen del sistema operativo en la tarjeta SD utilizo [rpiimager](https://www.raspberrypi.org/blog/raspberry-pi-imager-imaging-utility). Esta herramienta te provee de una interfaz gráfica muy sencilla en la que en primer lugar se selecciona la imagen que quieres flashear, en segundo lugar se elige dónde la quieres flashear y por último se inicia la grabación. Esta herramienta te evita tener que descargar la imagen del sistema operativo ya que es la propia herramienta quien se encarga de descargarla.

Al arrancar la raspberry por primera vez cloud-init se activará y ejecutará las acciones anteriores, lo único que hay que hacer es esperar unos minutos. Alguien perspicaz, se habrá dado cuenta que hay dos acciones en la lista anterior que no son iguales para todas las raspberry del cluster: establecer el nombre de la instancia y configurar una ip fija. Esto hace que haya que tener para cada instancia del cluster un fichero de configuración diferente. Y en este punto es donde entra en acción *Ansible*.

> Aunque se le asigne una ip fija a las raspberry, en el router habrá que reservarla igualmente, ya que podría darse el caso de que mientras está apagado el cluster, se conecte algún dispositivo a la red y se le asigne una de las ips del cluster.

## Ansible

*Ansible*, resumiéndolo mucho, es una herramienta de automatización de tareas. Dado un fichero de inventario, en el que se definen una serie de máquinas; y un fichero de tareas (*playbook*), en el que se definen una serie de tareas; Ansible se encargará de ejecutar cada una de las tareas en cada una de las máquinas. Con el añadido de que la ejecución de dichas tareas es *idempotente*, es decir, que si alguna de las tareas ya se ha ejecutado en alguna de dichas máquinas, no la volverá a ejecutar. Esto es una simplificación muy grande de todo el universo de Ansible, pero en este post no quiero entrar en detalles sobre Ansible, sino en explicar lo mínimo para que se entienda de qué forma se ha utilizado esta herramienta para montar el cluster.

Como he mencionado anteriormente, he utilizado Ansible para la generación de los ficheros de configuración de cloud-init. Y este es un caso de uso un poco especial, puesto que no se ajusta a la descripción anterior sobre el funcionamiento básico de Ansible. Sí que disponemos de un fichero de inventario, pero no utilizamos Ansible para ejecutar ninguna tarea sobre las máquinas del inventario, sino para obtener unos datos sobre dichas máquinas y utilizarlos para generar unos ficheros de configuración en el puesto local.

Este es un extracto del fichero de inventario:

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

En este caso hemos definido el inventario en un fichero en formato `INI`. Se puede ver que se han definido varios grupos. Hay un grupo con un solo elemento para cada una de las máquinas del cluster y así poder hacer referencia a una máquina concreta:

- rpicluster01
- rpicluster02
- rpicluster03
- rpicluster04
- rpicluster05

También hay un grupo que está compuesto por todas las máquinas del cluster, para poder hacer referencia a todo el cluster:

- rpicluster

Para cada una de las máquinas se define una propiedad `custom_hostname` que contiene el nombre de la máquina.

(se puede ver el fichero completo [aquí](https://github.com/dicastro/rpicluster/blob/master/playbooks/inventory))

A continuación se muestra el *playbook* de ansible que genera los ficheros de configuración de cloud-init para las máquinas del cluster:

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

Se definen 3 tareas:

- La tarea 1 se encarga de crear un directorio para cada una de las máquinas del inventario
- La tarea 2 genera el fichero de configuración `user-data` a partir de un template
- La tarea 3 genera el fichero de configuración `network-config` a partir de un template

(se puede ver el playbook completo [aquí](https://github.com/dicastro/rpicluster/tree/master/playbooks/00_cluster_regenerate_cloudinit_config))

### Cómo instalar Ansible en Windows 10

La manera más fácil de utilizar Ansible en Windows 10 es a través del WLS. Para instalar Ansible he utilizado `pip`, por lo que el primer paso será instalar `pip3` y algunas dependencias necesarias:

```bash
sudo apt install -y python3-pip python3-dev libffi-dev libssl-dev
```

A continuación se instala Ansible (a nivel del usuario):

```bash
pip3 install ansible --user
```

Por último se actualiza el `PATH`:

```bash
echo 'PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
```

Estas son algunas utilidades interesantes que recomiendo tener instaladas para trabajar con Ansible:

```bash
pip3 install yamllint ansible-lint molecule
```

### Actualizar Ansible 2.9 a 2.10

Recientemente se ha lanzado la versión 2.10 de Ansible y en esta versión ha habido una reestructuración importante de módulos. Debido a esta reestructuración la actualización no se puede hacer ejecutando un *upgrade* del paquete ya instalado, sino que hay que desinstalar la versión instalada (la versión 2.9):

```bash
pip3 uninstall ansible ansible-base
```

Y a continuación instalar de nuevo (la última versión, 2.10):

```bash
pip3 install ansible --user
```

## Docker

Gracias a Ansible, la instalación de Docker en todas las máquinas se ha simplificado al máximo. He encontrado un playbook, que he utilizado casi tal cual, que se encarga de instalar Docker en sistemas debian. Se puede encontrar la versión que he utilizado [aquí](https://github.com/dicastro/rpicluster/tree/master/playbooks/02_cluster_install_docker).

## Conclusión

Como conclusión he de decir que tanto *cloud-init* como *Ansible* han sido dos grandes descubrimientos. Sobre todo Ansible, ya que veo que es una herramienta que puedo empezar a utilizar en mi día a día a nivel profesional.

La única pega que le veo a Ansible, es que algunos aspectos no son compatibles con Windows. Actualmente utilizo un Windows 10 y he podido hacer uso de Ansible sin grandes complicaciones a través de WLS. El único inconveniente que me he topado hasta el momento, ha sido a la hora de utilizar *Ansible Vault*, ya que para ciertas situaciones es necesario modificar los permisos de algunos ficheros, lo cual no es posible en WLS a día de hoy (o al menos yo no he encontrado la manera de hacerlo).