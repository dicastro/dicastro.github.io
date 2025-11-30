---
title: HomeLab
summary: Personal infrastructure for data management, services, and privacy
date: 2025-03-07
lastmod: 2025-11-28
tags:
  - Proxmox
  - Docker
  - Ansible
  - Privacy
---

> [!NOTE]
> Still under development

Homelab is my personal server infrastructure used to manage self-hosted services, automate deployments, and ensure the privacy of my data. It grew out of my experience with a QNAP NAS, which became limited in resources and speed, and from my increasing interest in avoiding dependence on large IT companies' services.

The system is based on two miniPCs running Proxmox and Proxmox Backup Server:

- **Main miniPC:** i9 with 20 cores, 64 GB RAM, 2 TB storage. This is where all virtual machines run, depending on the services I want to deploy.
- **Secondary miniPC:** less powerful, dedicated to Proxmox Backup Server to optimize storage and keep a second local copy of backups.
- **Encrypted remote backup:** stored in a cloud provider, following the 3-2-1 backup strategy (three copies, two media types, one off-site).

Both the creation and configuration of virtual machines and the deployment of all services (via Docker containers) are fully automated using Ansible.

**Services I currently use**

| Service | Usage / what it is for |
|---------|--------------------------|
| {{<icon name="custom/homer" inline="true">}} [Homer](https://github.com/bastienwirtz/homer) | Dashboard to access all homelab services |
| {{<icon name="custom/vaultwarden" inline="true">}} [VaultWarden](https://github.com/dani-garcia/vaultwarden) | Self-hosted password manager compatible with Bitwarden |
| {{<icon name="custom/adguardhome" inline="true">}} [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome) | Internal DNS with ad-blocking, malware protection, and tracking filters |
| {{<icon name="custom/homeassistant" inline="true">}} [Home Assistant](https://www.home-assistant.io) | Home automation platform for integrating and controlling devices |
| {{<icon name="custom/zwave" inline="true">}} [ZWave](https://zwave-js.github.io/zwave-js-ui) | Control and integration of IoT devices using the Z-Wave protocol |
| {{<icon name="custom/peanut" inline="true">}} [PeaNut](https://github.com/Brandawg93/PeaNUT) | UPS status monitoring through a web interface |
| {{<icon name="custom/owncloud" inline="true">}} [OwnCloud](https://owncloud.com) | File storage, synchronization, and sharing |
| {{<icon name="custom/immich" inline="true">}} [Immich](https://immich.app) | Private photo hosting with automatic backup and mobile sync |
| {{<icon name="custom/memos" inline="true">}} [Memos](https://usememos.com) | Lightweight, self-hosted note-taking app |
| {{<icon name="custom/lubelogger" inline="true">}} [LubeLogger](https://lubelogger.com/) | Vehicle maintenance and expense tracking |
| {{<icon name="custom/tandoorrecipes" inline="true">}} [Tandoor Recipes](https://tandoor.dev) | Recipe manager, meal planner, and shopping list system |
| {{<icon name="custom/tailscale" inline="true">}} [Tailscale](https://tailscale.com) | Mesh VPN for secure remote access without opening ports |
| {{<icon name="custom/mailrise" inline="true">}} [MailRise](https://github.com/YoRyan/mailrise) | SMTP server that converts emails into notifications |
| {{<icon name="custom/apprise" inline="true">}} [AppRise](https://github.com/caronc/apprise) | REST API to send notifications to more than 90 services |
| {{<icon name="custom/mailpit" inline="true">}} [MailPit](https://github.com/axllent/mailpit) | Fake SMTP server for testing, with web UI to view emails |
| {{<icon name="devicon/portainer" inline="true">}} [Portainer](https://www.portainer.io) | GUI to manage Docker containers and stacks |
| {{<icon name="custom/actualbudget" inline="true">}} [ActualBudget](https://actualbudget.org) | Personal finance manager based on envelope budgeting |
| {{<icon name="custom/traefik" inline="true">}} [Traefik](https://traefik.io) | Reverse proxy and TLS certificate manager with Let's Encrypt |
| {{<icon name="devicon/prometheus" inline="true">}} [AlertManager](https://github.com/prometheus/alertmanager) | Metrics-based alert routing and notifications |
| {{<icon name="devicon/prometheus" inline="true">}} [Prometheus](https://prometheus.io) | System and service monitoring and metrics collection |

**Main goals achieved:**

- Secure remote access to all services without opening ports directly on the router.
- Access to services through internal DNS with automatic TLS certificate issuance and renewal using Let's Encrypt, avoiding exposed IPs and ports.
- Organization of services by hardware resources and data criticality, defining backup frequency and retention.
- Full control of my data, storage, and applications, replacing third-party services (Dropbox, Google Docs, Google Photos, Google Keep, etc).

{{< embed platform="github" resource="dicastro/homelab" type="repo" >}}
