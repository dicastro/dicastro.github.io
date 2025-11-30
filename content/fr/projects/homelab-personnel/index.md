---
title: HomeLab
summary: Infrastructure personnelle pour la gestion des données, des services et de la vie privée
date: 2025-03-07
lastmod: 2025-11-28
tags:
  - Proxmox
  - Docker
  - Ansible
  - Confidentialité
---

> [!NOTE]
> Encore en développement

Homelab est mon infrastructure personnelle de serveurs, utilisée pour gérer des services auto-hébergés, automatiser les déploiements et garantir la confidentialité de mes données. Il est né de mon expérience avec un NAS QNAP, devenu limité en ressources et en vitesse, ainsi que de mon intérêt croissant pour réduire ma dépendance aux services des grandes entreprises technologiques.

Le système repose sur deux miniPC fonctionnant avec Proxmox et Proxmox Backup Server :

- **MiniPC principal :** i9 avec 20 cœurs, 64 Go de RAM, 2 To de stockage. Toutes les machines virtuelles nécessaires y sont exécutées selon les services à déployer.
- **MiniPC secondaire :** moins puissant, dédié à Proxmox Backup Server pour optimiser l'espace et conserver une seconde copie locale des sauvegardes.
- **Sauvegarde distante chiffrée :** stockée dans un cloud, suivant la stratégie de sauvegarde 3-2-1 (trois copies, deux supports, un emplacement externe).

La création et la configuration des machines virtuelles ainsi que le déploiement de tous les services (au moyen de conteneurs Docker) sont entièrement automatisés via Ansible.

**Services que j'utilise actuellement**

| Service | Usage / à quoi ça sert |
|---------|--------------------------|
| {{<icon name="custom/homer" inline="true">}} [Homer](https://github.com/bastienwirtz/homer) | Tableau de bord pour accéder à tous les services du homelab |
| {{<icon name="custom/vaultwarden" inline="true">}} [VaultWarden](https://github.com/dani-garcia/vaultwarden) | Gestionnaire de mots de passe auto-hébergé compatible avec Bitwarden |
| {{<icon name="custom/adguardhome" inline="true">}} [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) | DNS interne avec blocage de publicités, malware et traqueurs |
| {{<icon name="custom/homeassistant" inline="true">}} [Home Assistant](https://www.home-assistant.io) | Plateforme domotique pour intégrer et automatiser les appareils du foyer |
| {{<icon name="custom/zwave" inline="true">}} [ZWave](https://zwave-js.github.io/zwave-js-ui) | Gestion et intégration d'appareils IoT basés sur le protocole Z-Wave |
| {{<icon name="custom/peanut" inline="true">}} [PeaNut](https://github.com/Brandawg93/PeaNUT) | Supervision de l'état de l'onduleur/UPS via interface web |
| {{<icon name="custom/owncloud" inline="true">}} [OwnCloud](https://owncloud.com) | Stockage de fichiers, synchronisation et partage |
| {{<icon name="custom/immich" inline="true">}} [Immich](https://immich.app) | Hébergement privé de photos avec sauvegarde automatique |
| {{<icon name="custom/memos" inline="true">}} [Memos](https://usememos.com) | Application légère de prise de notes auto-hébergée |
| {{<icon name="custom/lubelogger" inline="true">}} [LubeLogger](https://lubelogger.com/) | Suivi de l'entretien et des dépenses des véhicules |
| {{<icon name="custom/tandoorrecipes" inline="true">}} [Tandoor Recipes](https://tandoor.dev) | Gestionnaire de recettes, planification des repas et listes de courses |
| {{<icon name="custom/tailscale" inline="true">}} [Tailscale](https://tailscale.com) | VPN mesh pour un accès distant sécurisé sans ouvrir de ports |
| {{<icon name="custom/mailrise" inline="true">}} [MailRise](https://github.com/YoRyan/mailrise) | Serveur SMTP transformant les emails en notifications |
| {{<icon name="custom/apprise" inline="true">}} [AppRise](https://github.com/caronc/apprise) | API REST pour envoyer des notifications à plus de 90 services |
| {{<icon name="custom/mailpit" inline="true">}} [MailPit](https://github.com/axllent/mailpit) | Faux serveur SMTP pour tests, avec interface web |
| {{<icon name="devicon/portainer" inline="true">}} [Portainer](https://www.portainer.io) | Interface graphique pour gérer conteneurs Docker et stacks |
| {{<icon name="custom/actualbudget" inline="true">}} [ActualBudget](https://actualbudget.org) | Gestionnaire de finances personnelles basé sur les budgets |
| {{<icon name="custom/traefik" inline="true">}} [Traefik](https://traefik.io) | Proxy inverse et gestionnaire de certificats TLS avec Let's Encrypt |
| {{<icon name="devicon/prometheus" inline="true">}} [AlertManager](https://github.com/prometheus/alertmanager) | Gestion et envoi d'alertes basées sur les métriques |
| {{<icon name="devicon/prometheus" inline="true">}} [Prometheus](https://prometheus.io) | Supervision et collecte de métriques système et services |

**Objectifs principaux atteints :**

- Accès distant sécurisé à tous les services sans ouvrir de ports sur le routeur.
- Accès via DNS interne avec génération et renouvellement automatique des certificats TLS grâce à Let's Encrypt, évitant les IPs et ports exposés.
- Organisation des services selon les ressources matérielles et la criticité des données, avec définition des politiques de sauvegarde.
- Contrôle total sur mes données, mon stockage et mes applications, remplaçant des services tiers (Dropbox, Google Docs, Google Photos, Google Keep, etc).

{{< embed platform="github" resource="dicastro/homelab" type="repo" >}}
