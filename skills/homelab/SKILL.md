---
name: homelab
description: |
  Comprehensive homelab networking suite covering subnet architecture, OPNsense/UniFi VLAN segmentation & firewall rules, Pi-hole DNS with unbound, WireGuard remote access VPN, and automated network verification scripts.
triggers:
  - "homelab"
  - "homelab network"
  - "vlan segmentation"
  - "pihole"
  - "pi-hole"
  - "wireguard vpn"
  - "opnsense"
  - "unifi"
  - "homelab readiness"
license: MIT
metadata:
  origin: ECC
---

# Homelab Infrastructure & Networking Suite

## Executive Table of Contents
- [Part 1: Homelab Network Setup](#part-1-homelab-network-setup)
- [Part 2: Homelab VLAN Segmentation](#part-2-homelab-vlan-segmentation)
- [Part 3: Homelab Pi-hole DNS](#part-3-homelab-pi-hole-dns)
- [Part 4: Homelab WireGuard VPN](#part-4-homelab-wireguard-vpn)
- [Part 5: Homelab Network Readiness](#part-5-homelab-network-readiness)

---

# Part 1: Homelab Network Setup

# Homelab Network Setup

Use this skill to design a home or small-lab network that can grow without
needing a full rebuild.

## When to Use

- Planning a new home network or redesigning an ISP-router-only setup.
- Choosing gateway, switch, and access point roles.
- Designing IP ranges, DHCP scopes, static reservations, and DNS.
- Preparing for future VLANs, Pi-hole, NAS, lab servers, or VPN access.
- Troubleshooting a new network that has double NAT, unstable Wi-Fi, or changing
  server addresses.

## How It Works

Start by separating device roles:

```text
Internet
  |
Modem or ONT
  |
Gateway or router      NAT, firewall, DHCP, DNS, inter-VLAN routing
  |
Managed switch         wired clients, AP uplinks, optional VLAN trunks
  |
Access points          Wi-Fi only; ideally wired backhaul
Servers and NAS        stable addresses, DNS names, monitoring
Clients and IoT        DHCP pools, isolated later if VLANs are available
```

Pick a gateway that matches the operator, not just the feature checklist:

| Option | Best fit | Notes |
| --- | --- | --- |
| ISP router | Basic internet only | Limited control and often poor VLAN support |
| UniFi gateway | Managed home network | Good UI, ecosystem lock-in |
| OPNsense or pfSense | Flexible homelab | Strong VLAN, firewall, VPN, and DNS control |
| MikroTik | Advanced network users | Powerful, but easy to misconfigure |
| Linux router | Tinkerers | Document rollback before using as primary gateway |

## IP Plan

Avoid the most common default, `192.168.1.0/24`, when you expect to use VPNs.
It often conflicts with hotels, offices, and ISP routers.

```text
Example small homelab plan:

192.168.10.0/24  trusted clients
192.168.20.0/24  IoT and media devices
192.168.30.0/24  servers and NAS
192.168.40.0/24  guest Wi-Fi
192.168.99.0/24  network management

Gateway convention: .1
Infrastructure reservations: .2 through .49
Dynamic DHCP pool: .50 through .240
Spare room: .241 through .254
```

Use `home.arpa` for local names. It is reserved for home networks and avoids the
leakage/conflict problems of ad hoc names like `home.lan`.

```text
nas.home.arpa
pihole.home.arpa
gateway.home.arpa
switch-01.home.arpa
```

## DHCP And DNS

- Use DHCP reservations for anything you SSH into, bookmark, monitor, or expose
  as a service.
- Hand out the gateway as DNS until a local resolver is intentionally deployed.
- If using Pi-hole or another DNS filter, give it a reservation first, then point
  DHCP DNS options at that address.
- Keep a small static/reserved range per subnet so replacements do not collide
  with dynamic leases.

## Cabling And Wi-Fi

- Prefer wired AP backhaul over mesh when you can run Ethernet.
- Use a PoE switch for APs and cameras if the budget allows it.
- Label both ends of each cable and keep a simple port map.
- Put the gateway, switch, DNS server, and NAS on UPS power if outages are common.

## Examples

### Beginner Upgrade

Goal: Keep the ISP router but stabilize a small lab.

1. Set DHCP reservations for NAS, Pi, and any SSH hosts.
2. Move local names to `home.arpa`.
3. Disable duplicate DHCP servers on secondary routers or APs.
4. Wire the main AP instead of relying on wireless backhaul.

### VLAN-Ready Plan

Goal: Prepare for future segmentation without enabling it immediately.

1. Choose non-overlapping /24 ranges for trusted, IoT, servers, guest, and
   management.
2. Reserve .1 for the gateway and .2-.49 for infrastructure on every subnet.
3. Buy a gateway and switch that support VLANs and inter-VLAN firewall rules.
4. Document which SSIDs and switch ports will eventually map to each network.

## Anti-Patterns

- Double NAT without a reason or documentation.
- Using `192.168.1.0/24` when VPN access is planned.
- Dynamic addresses for NAS, Pi-hole, Home Assistant, or other service hosts.
- Consumer routers repurposed as APs while their DHCP servers are still enabled.
- Flat networks with cameras, smart plugs, laptops, and servers all sharing the
  same trust boundary.

## See Also

- Skill: `network-interface-health`
- Skill: `network-config-validation`

---

# Part 2: Homelab VLAN Segmentation

# Homelab VLAN Segmentation

How to split a home network into isolated VLANs so IoT devices, guests, and your main
PCs cannot talk to each other. The most impactful security upgrade for a home network.

All firewall rules shown here add isolation between segments — they do not remove
existing protections. Apply changes in a maintenance window and verify connectivity
between segments after each step before moving on.

## When to Use

- Setting up VLANs on a home network for the first time
- Isolating IoT devices (smart bulbs, cameras, TVs) from trusted devices
- Creating a guest Wi-Fi network that cannot reach home devices
- Explaining how VLANs work to someone unfamiliar with the concept
- Configuring trunk ports, access ports, and SSID-to-VLAN mapping
- Troubleshooting inter-VLAN routing or firewall rule issues on pfSense/OPNsense/UniFi

## How It Works

```
Without VLANs — flat network:
  All devices on 192.168.1.0/24
  Smart TV (potential malware) → can reach your NAS, PCs, everything

With VLANs:
  VLAN 10 — Trusted    192.168.10.0/24  (PCs, phones, laptops)
  VLAN 20 — IoT        192.168.20.0/24  (smart TV, bulbs, cameras)
  VLAN 30 — Servers    192.168.30.0/24  (NAS, Pi, VMs)
  VLAN 40 — Guest      192.168.40.0/24  (visitor Wi-Fi)
  VLAN 99 — Management 192.168.99.0/24  (switch/AP web UIs)

  Smart TV → blocked from reaching 192.168.10.0/24 and 192.168.30.0/24
  Guests → internet only, cannot see any home devices
```

## VLAN Design Template

```
VLAN  Name        Subnet              Gateway         Purpose
10    trusted     192.168.10.0/24     192.168.10.1    PCs, phones, laptops
20    iot         192.168.20.0/24     192.168.20.1    Smart home devices
30    servers     192.168.30.0/24     192.168.30.1    NAS, Pi, self-hosted
40    guest       192.168.40.0/24     192.168.40.1    Visitor Wi-Fi
99    management  192.168.99.0/24     192.168.99.1    Network gear web UIs
```

## Examples

**Typical homelab with UniFi AP and managed switch:**

```
Scenario: 3-bedroom house, UniFi Dream Machine + UniFi 8-port switch + 2 APs

VLAN 10 — Trusted    192.168.10.0/24   MacBook, iPhones, iPad
VLAN 20 — IoT        192.168.20.0/24   Nest thermostat, Philips Hue, Ring doorbell, smart TVs
VLAN 30 — Servers    192.168.30.0/24   Synology NAS (192.168.30.10), Pi-hole (192.168.30.2)
VLAN 40 — Guest      192.168.40.0/24   Visitor Wi-Fi — internet only

SSID → VLAN mapping:
  "Home"      → VLAN 10 (WPA2, strong password, trusted devices only)
  "IoT"       → VLAN 20 (WPA2, separate password, printed on router for setup)
  "Guest"     → VLAN 40 (WPA2, simple password you can share freely)

Switch port behavior:
  Port 1  → trunk to router (tagged VLANs 10,20,30,40,99)
  Port 2  → trunk to APs (tagged VLANs 10,20,40; AP handles per-SSID tagging)
  Port 3  → access VLAN 30 (NAS — untagged, no VLAN awareness needed)
  Port 4  → access VLAN 30 (Pi-hole — untagged)
  Port 5–8 → access VLAN 10 (wired workstations)

Firewall rules applied (all rules add isolation, none remove existing protections):
  IoT → Trusted: BLOCK
  IoT → Servers: BLOCK except 192.168.30.2:53 (Pi-hole DNS allowed)
  IoT → Internet: ALLOW
  Guest → Local networks: BLOCK
  Guest → Internet: ALLOW
  Trusted → everywhere: ALLOW
```

## UniFi Configuration

### Create Networks in UniFi Controller

```
Settings → Networks → Create New Network

For each VLAN:
  Name: IoT
  Purpose: Corporate  (gives DHCP + routing)
  VLAN ID: 20
  Network: 192.168.20.0/24
  Gateway IP: 192.168.20.1
  DHCP: Enable
  DHCP Range: 192.168.20.100 – 192.168.20.254
```

### Map SSIDs to VLANs (UniFi)

```
Settings → WiFi → Create New WiFi

  Name: IoT-Network
  Password: <separate password>
  Network: IoT  ← select your VLAN here
  # All devices connecting to this SSID land in VLAN 20

  Name: Guest
  Password: <guest password>
  Network: Guest
  Guest Policy: Enable  ← isolates guests from each other too
```

### UniFi Firewall Rules (Traffic Rules)

```
Settings → Traffic & Security → Traffic Rules

# Block IoT from reaching Trusted VLAN
  Action: Block
  Category: Local Network
  Source: IoT (192.168.20.0/24)
  Destination: Trusted (192.168.10.0/24)

# Allow IoT to reach internet only
  Action: Allow
  Source: IoT
  Destination: Internet

# Block Guest from all local networks
  Action: Block
  Source: Guest
  Destination: Local Networks
```

## pfSense / OPNsense Configuration

### Create VLANs

```
Interfaces → Assignments → VLANs → Add

  Parent Interface: em1  (your LAN NIC)
  VLAN Tag: 20
  Description: IoT

# Repeat for each VLAN, then assign each VLAN to an interface:
Interfaces → Assignments → Add
  Select the VLAN you created → click Add
  Enable the interface, set IP to gateway address (192.168.20.1/24)
```

### DHCP for Each VLAN

```
Services → DHCP Server → Select your VLAN interface

  Enable DHCP
  Range: 192.168.20.100 to 192.168.20.254
  DNS Servers: 192.168.30.2  ← Pi-hole IP if you have one
```

### Firewall Rules (pfSense/OPNsense)

```
# Rules are processed top-to-bottom, first match wins.

# On the IoT interface (VLAN 20):
  Rule 1: Allow IoT → Pi-hole DNS  ← MUST come before the RFC1918 block rule
    Protocol: UDP/TCP
    Source: IoT net
    Destination: 192.168.30.2 port 53
    Action: Allow

  Rule 2: Block IoT → RFC1918 (all private IP ranges)
    Protocol: any
    Source: IoT net
    Destination: RFC1918  (192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12)
    Action: Block

  Rule 3: Allow IoT → internet
    Protocol: any
    Source: IoT net
    Destination: any
    Action: Allow

# On the Trusted interface (VLAN 10):
  Allow all (trusted devices can reach everything)
    Source: Trusted net
    Destination: any
    Action: Allow

# Additional exceptions for IoT devices that need specific local services:
  Insert before Rule 2 (the RFC1918 block):
    Protocol: TCP
    Source: IoT net
    Destination: 192.168.30.x port 8123  ← Home Assistant
    Action: Allow
```

## MikroTik Configuration

```
# Step 1: Create a bridge with VLAN filtering enabled
/interface bridge
add name=bridge vlan-filtering=yes

# Step 2: Add physical ports to the bridge
# Trunk port to router/uplink (tagged for all VLANs)
/interface bridge port
add bridge=bridge interface=ether1 frame-types=admit-only-vlan-tagged

# Access port for trusted devices (untagged VLAN 10)
/interface bridge port
add bridge=bridge interface=ether2 pvid=10 frame-types=admit-only-untagged-and-priority-tagged

# Access port for IoT devices (untagged VLAN 20)
/interface bridge port
add bridge=bridge interface=ether3 pvid=20 frame-types=admit-only-untagged-and-priority-tagged

# Step 3: Define which VLANs are allowed on which ports
/interface bridge vlan
add bridge=bridge tagged=ether1 untagged=ether2 vlan-ids=10
add bridge=bridge tagged=ether1 untagged=ether3 vlan-ids=20

# Step 4: Create VLAN interfaces on the bridge (gateway IPs)
/interface vlan
add interface=bridge name=vlan10 vlan-id=10
add interface=bridge name=vlan20 vlan-id=20

# Step 5: Assign gateway IPs
/ip address
add interface=vlan10 address=192.168.10.1/24
add interface=vlan20 address=192.168.20.1/24

# Step 6: DHCP pools and servers
/ip pool
add name=pool-trusted ranges=192.168.10.100-192.168.10.254
add name=pool-iot ranges=192.168.20.100-192.168.20.254

/ip dhcp-server
add interface=vlan10 address-pool=pool-trusted name=dhcp-trusted
add interface=vlan20 address-pool=pool-iot name=dhcp-iot

/ip dhcp-server network
add address=192.168.10.0/24 gateway=192.168.10.1
add address=192.168.20.0/24 gateway=192.168.20.1

# Step 7: Firewall — block IoT from reaching trusted VLAN
/ip firewall filter
add chain=forward src-address=192.168.20.0/24 dst-address=192.168.10.0/24 \
    action=drop comment="Block IoT to Trusted"
```

## Switch Trunk vs Access Ports

```
# Trunk port: carries multiple VLANs (tagged) — connects switch-to-switch, switch-to-router, switch-to-AP
# Access port: carries one VLAN (untagged) — connects to end devices (PC, camera, NAS)

# A managed switch port connected to your router should be a trunk:
  Allowed VLANs: 10, 20, 30, 40, 99

# A port connecting to a PC should be an access port:
  VLAN: 10 (trusted)
  No tagging — the PC does not know or care about VLANs

# A port connecting to an AP must be a trunk:
  The AP tags traffic from each SSID with the right VLAN ID
  Allowed VLANs: 10, 20, 40  (whichever SSIDs the AP serves)
```

## Anti-Patterns

```
# BAD: Creating VLANs without adding firewall rules
# VLANs without firewall rules do not provide security — inter-VLAN routing is open by default
# GOOD: Add explicit block rules immediately after creating VLANs

# BAD: Putting the Pi-hole in the IoT VLAN
# IoT devices can reach it but trusted devices cannot (without extra rules)
# GOOD: Pi-hole in the Servers VLAN with a rule allowing all VLANs to reach port 53

# BAD: Native VLAN equals management VLAN
# Untagged traffic landing in your management VLAN enables VLAN hopping attacks
# GOOD: Use a dedicated unused VLAN as native (e.g. VLAN 999), keep management traffic tagged

# BAD: Same Wi-Fi password for IoT SSID and trusted SSID
# Anyone who learns the password can connect IoT devices to the wrong segment
```

## Best Practices

- Start with 4 VLANs: Trusted, IoT, Servers, Guest — add more as needed
- Put Pi-hole in the Servers VLAN (192.168.30.x)
- Add a firewall rule allowing DNS (port 53) from all VLANs to the Pi-hole IP — before any RFC1918 block rule
- Test isolation after every rule change: from the IoT VLAN, try to ping a trusted device — it should fail
- Use a management VLAN for switch and AP web UIs and restrict access to the Trusted VLAN only
- Document your VLAN design in a table (VLAN ID, name, subnet, purpose)

## Related Skills

- homelab-network-setup
- homelab-pihole-dns
- homelab-wireguard-vpn

---

# Part 3: Homelab Pi-hole DNS

# Homelab Pi-hole DNS

Pi-hole is a network-wide DNS ad blocker that runs on a Raspberry Pi or any Linux host.
Every device on your network gets ad and malware domain blocking automatically — no browser
extension needed.

## When to Use

- Installing Pi-hole on a Raspberry Pi or Linux host
- Configuring Pi-hole as the DNS server for a home network
- Adding or managing blocklists
- Setting up DNS-over-HTTPS (DoH) upstream resolvers
- Creating local DNS records (e.g. `nas.home.lan`, `pi.home.lan`)
- Troubleshooting devices that lose internet access after Pi-hole is installed
- Running Pi-hole alongside or instead of DHCP

## How Pi-hole Works

```
Normal flow (without Pi-hole):
  Device → requests ads.tracker.com → ISP DNS → real IP → ads load

With Pi-hole:
  Device → requests ads.tracker.com → Pi-hole DNS → blocked (returns 0.0.0.0) → no ad

All DNS queries go through Pi-hole first.
Pi-hole checks against blocklists.
Blocked domains return a null response — the ad/tracker never loads.
Allowed domains get forwarded to your upstream resolver (Cloudflare, Google, etc.).
```

## Installation

### Docker (Recommended)

Docker is the easiest way to install Pi-hole and makes updates and backups
straightforward.

```yaml
# docker-compose.yml
services:
  pihole:
    image: pihole/pihole:<pinned-release-tag>
    container_name: pihole
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"          # Web admin
    environment:
      TZ: "America/New_York"
      WEBPASSWORD: "${PIHOLE_WEBPASSWORD}"   # set via .env file or secret
      PIHOLE_DNS_: "1.1.1.1;1.0.0.1"
      DNSMASQ_LISTENING: "all"
    volumes:
      - "./etc-pihole:/etc/pihole"
      - "./etc-dnsmasq.d:/etc/dnsmasq.d"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN              # only needed if Pi-hole will serve DHCP
```

Replace `<pinned-release-tag>` with a current Pi-hole release tag before deploying.
Avoid `latest` for long-lived DNS infrastructure so upgrades are deliberate and
reviewable.

Set `PIHOLE_WEBPASSWORD` in a `.env` file next to `docker-compose.yml`, chmod it to
`600`, and keep it out of git — do not put the password directly in the compose file.

Access web admin at: `http://<pi-ip>/admin`

### Bare-Metal Install (Raspberry Pi OS / Debian / Ubuntu)

Pi-hole requires a static IP before installing.

```bash
# Step 1: Assign a static IP (edit /etc/dhcpcd.conf on Pi OS)
sudo nano /etc/dhcpcd.conf
# Add at the bottom:
interface eth0
static ip_address=192.168.3.2/24
static routers=192.168.3.1
static domain_name_servers=192.168.3.1

# Step 2: Download and inspect the installer before running it.
# Prefer the package or installer path documented by Pi-hole for your OS/version.
curl -sSL https://install.pi-hole.net -o pi-hole-install.sh
less pi-hole-install.sh   # review before proceeding

# Step 3: Run
bash pi-hole-install.sh

# Follow the interactive installer:
# 1. Select network interface (eth0 for wired — recommended)
# 2. Select upstream DNS (Cloudflare or leave default — can change later)
# 3. Confirm static IP
# 4. Install the web admin interface (recommended)
# 5. Note the admin password shown at the end
```

## Pointing Your Network at Pi-hole

```
# Method 1: Change DNS in your router DHCP settings (recommended)
  Router admin UI → DHCP Settings → DNS Server
  Primary DNS: 192.168.3.2  (Pi-hole IP)
  Secondary DNS: leave blank for strict blocking, or use a second Pi-hole.
                 A public fallback such as 1.1.1.1 improves availability during
                 rollout but can bypass blocking because clients may query it.

  All devices get Pi-hole as DNS automatically on next DHCP renewal.
  Force renewal: reconnect Wi-Fi or run 'sudo dhclient -r && sudo dhclient' on Linux

# Method 2: Per-device DNS (useful for testing before network-wide rollout)
  Windows: Control Panel → Network Adapter → IPv4 Properties → set DNS manually
  macOS: System Settings → Network → Details → DNS → set manually
  Linux: /etc/resolv.conf or NetworkManager

# Method 3: Pi-hole as DHCP server (replaces router DHCP)
  Pi-hole admin → Settings → DHCP → Enable
  Disable DHCP on your router first — two DHCP servers on the same network cause conflicts
  Advantage: hostname resolution works automatically (devices register their names)
```

## Blocklist Management

```
# Pi-hole admin → Adlists → Add new adlist

# Recommended blocklists:
  https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
  # default — 200k+ domains

  https://blocklistproject.github.io/Lists/malware.txt
  # malware domains

  https://blocklistproject.github.io/Lists/tracking.txt
  # tracking/telemetry

# After adding a list:
  Tools → Update Gravity  (downloads and compiles all blocklists)

# If a site is blocked that should not be (false positive):
  Pi-hole admin → Whitelist → Add domain
  Example: api.my-legitimate-service.com

# Check what is being blocked in real time:
  Dashboard → Query Log  (live DNS query stream with block/allow status)
```

## DNS-over-HTTPS Upstream

DNS-over-HTTPS encrypts your DNS queries so your ISP cannot see what sites you resolve.

```bash
# Install cloudflared (Cloudflare's DoH proxy).
# Prefer Cloudflare's package repository for automatic signed package verification.
# If you download a binary directly, pin a release version and verify its checksum.
CLOUDFLARED_VERSION="<pinned-version>"
curl -LO "https://github.com/cloudflare/cloudflared/releases/download/${CLOUDFLARED_VERSION}/cloudflared-linux-arm64"
# Verify the checksum/signature from Cloudflare's release notes before installing.
sudo mv cloudflared-linux-arm64 /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared

# Create cloudflared config
sudo mkdir -p /etc/cloudflared
sudo tee /etc/cloudflared/config.yml << EOF
proxy-dns: true
proxy-dns-port: 5053
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://1.0.0.1/dns-query
EOF

# Create systemd service
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared

# Now point Pi-hole at the local DoH proxy:
# Pi-hole admin → Settings → DNS → Custom upstream DNS
# Set to: 127.0.0.1#5053
# Uncheck all other upstream resolvers
```

## Local DNS Records

Make your services reachable by name (e.g. `nas.home.lan`, `grafana.home.lan`).

> **Domain name note:** `.home.lan` is widely used in homelabs and works in practice.
> The IETF-reserved suffix for local use is `.home.arpa` (RFC 8375) — use that to
> follow the standard. Avoid `.local` for Pi-hole DNS records as it conflicts with
> mDNS/Bonjour.

```
# Pi-hole admin → Local DNS → DNS Records

  Domain              IP
  nas.home.lan        192.168.30.10
  pi.home.lan         192.168.30.2
  grafana.home.lan    192.168.30.3
  proxmox.home.lan    192.168.30.4

# From any device on your network:
  ping nas.home.lan        → 192.168.30.10
  http://grafana.home.lan  → your Grafana dashboard

# For subdomains, add a CNAME:
  Pi-hole admin → Local DNS → CNAME Records
  Domain: portainer.home.lan → Target: pi.home.lan
```

## Troubleshooting

```bash
# Pi-hole blocking something it should not
pihole -q example.com          # Check if domain is blocked and which list
pihole -w example.com          # Whitelist immediately

# DNS not resolving at all
pihole status                  # Check if pihole-FTL is running
dig @192.168.3.2 google.com   # Test DNS directly against Pi-hole

# Restart Pi-hole DNS
pihole restartdns

# Check query logs for a specific device
pihole -t                      # Live tail of all queries
# Or filter by client in the web admin Query Log

# Pi-hole gravity update (refresh blocklists)
pihole -g
```

## Anti-Patterns

```
# BAD: Depending on one Pi-hole without a recovery path
# If Pi-hole crashes or the Pi loses power, DNS can stop working
# GOOD: Keep a documented router fallback for rollback during setup
# BETTER: Run two Pi-hole instances for redundancy; avoid public fallback DNS for strict blocking

# BAD: Installing Pi-hole without a static IP
# If the Pi gets a new DHCP IP, all devices lose DNS
# GOOD: Set static IP first, then install Pi-hole

# BAD: Enabling Pi-hole DHCP without disabling the router's DHCP first
# Two DHCP servers on the same network hand out conflicting IPs
# GOOD: Disable router DHCP, then enable Pi-hole DHCP

# BAD: Never updating gravity (blocklists)
# New ad and malware domains accumulate — stale lists miss them
# GOOD: Schedule weekly gravity update: pihole -g (or enable in Settings → API)
```

## Best Practices

- Give the Pi a static IP or DHCP reservation before installing Pi-hole
- Use Pi-hole as primary DNS; for redundancy, add a second Pi-hole instead of a
  public resolver if you need strict blocking
- Enable DoH (DNS-over-HTTPS) with cloudflared for encrypted upstream queries
- Set `home.lan` as your local domain and create DNS records for all your services
- Review the Query Log occasionally — blocked queries show you what devices are doing

## Related Skills

- homelab-network-setup
- homelab-vlan-segmentation
- homelab-wireguard-vpn

---

# Part 4: Homelab WireGuard VPN

# Homelab WireGuard VPN

WireGuard is a fast, modern VPN protocol. It is the right choice for remote access to a
home network — simpler to configure than OpenVPN and faster than most alternatives.

All configuration examples show common setups. Review each command — especially the
iptables forwarding rules and key file permissions — before applying them to your
system, and make changes in a maintenance window.

## When to Use

- Setting up WireGuard server on a Raspberry Pi, Linux host, pfSense, or router
- Generating WireGuard keypairs and writing peer config files
- Configuring remote access from a phone or laptop to a home network
- Explaining split tunneling (route only home traffic) vs full tunnel (route all traffic)
- Troubleshooting WireGuard connections that will not come up
- Automating peer configuration generation for multiple clients

## How WireGuard Works

```
Your phone (WireGuard client)
    │
    │  Encrypted UDP tunnel (port 51820)
    │
Your home router (WireGuard server — needs a public IP or DDNS)
    │
    Your home network (192.168.1.0/24, NAS, Pi, etc.)

Every device has a keypair (public + private key).
The server knows each client's public key.
The client knows the server's public key + endpoint (IP:port).
Traffic is encrypted end-to-end with no central server or certificate authority.
```

## Server Setup (Linux)

```bash
# Install WireGuard
sudo apt update && sudo apt install wireguard -y

# Generate server keypair — create files with private permissions from the start
sudo mkdir -p /etc/wireguard
sudo sh -c 'umask 077; wg genkey > /etc/wireguard/server_private.key'
sudo sh -c 'wg pubkey < /etc/wireguard/server_private.key > /etc/wireguard/server_public.key'

# Write server config — substitute the actual private key value
# Do not store private keys in version control or share them
sudo tee /etc/wireguard/wg0.conf << 'EOF'
[Interface]
Address = 10.8.0.1/24              # VPN subnet — server gets .1
ListenPort = 51820
PrivateKey = <paste_server_private_key_here>

# Scoped forwarding rules: allow VPN traffic in/out, not a blanket FORWARD ACCEPT
PostUp   = iptables -A FORWARD -i wg0 -o eth0 -j ACCEPT
PostUp   = iptables -A FORWARD -i eth0 -o wg0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
PostUp   = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -o eth0 -j ACCEPT
PostDown = iptables -D FORWARD -i eth0 -o wg0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Phone — replace with the actual phone public key
PublicKey = <phone_public_key>
AllowedIPs = 10.8.0.2/32

[Peer]
# Laptop — replace with the actual laptop public key
PublicKey = <laptop_public_key>
AllowedIPs = 10.8.0.3/32
EOF
sudo chmod 600 /etc/wireguard/wg0.conf

# Replace eth0 with your actual outbound interface name
# Check with: ip route show default

# Enable IP forwarding (required for routing traffic through the server)
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl --system

# Start WireGuard and enable on boot
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

## Client Configuration

```bash
# Generate a unique keypair for each client device
# Run on the client, or on the server and transfer the private key securely — never in plaintext
umask 077
wg genkey | tee phone_private.key | wg pubkey > phone_public.key

# Client config file (phone_wg0.conf):
[Interface]
PrivateKey = <phone_private_key>
Address = 10.8.0.2/32
DNS = 192.168.1.2                  # Optional: use Pi-hole for DNS over the tunnel

[Peer]
PublicKey = <server_public_key>
Endpoint = your-home-ip.ddns.net:51820  # Your public IP or DDNS hostname
AllowedIPs = 192.168.1.0/24            # Split tunnel: only home network traffic
# AllowedIPs = 0.0.0.0/0, ::/0        # Full tunnel: all traffic through VPN

PersistentKeepalive = 25              # Keep NAT hole open (required for mobile clients)
```

## Split Tunnel vs Full Tunnel

```
# Split tunnel: AllowedIPs = 192.168.1.0/24
  Only traffic destined for your home network goes through the VPN.
  Internet traffic (YouTube, Spotify) goes directly — better performance on mobile.
  Best for: "I just want to reach my NAS and Pi from anywhere."

# Full tunnel: AllowedIPs = 0.0.0.0/0, ::/0
  ALL traffic goes through your home internet connection.
  Useful for: piggybacking home DNS/Pi-hole ad blocking.
  Downside: home upload speed becomes your bottleneck everywhere.

# Multi-subnet split tunnel (most common homelab use case):
  AllowedIPs = 192.168.10.0/24, 192.168.20.0/24, 192.168.30.0/24, 10.8.0.0/24
  Routes all your VLANs through the tunnel; internet stays direct.
```

## Key Generation and Peer Management

```python
import subprocess

def generate_keypair() -> tuple[str, str]:
    """Generate a WireGuard keypair. Returns (private_key, public_key)."""
    private = subprocess.check_output(["wg", "genkey"]).decode().strip()
    public = subprocess.run(
        ["wg", "pubkey"], input=private.encode(), capture_output=True
    ).stdout.decode().strip()
    return private, public

def generate_preshared_key() -> str:
    return subprocess.check_output(["wg", "genpsk"]).decode().strip()

def build_client_config(
    client_private_key: str,
    client_vpn_ip: str,       # e.g. "10.8.0.3"
    server_public_key: str,
    server_endpoint: str,     # e.g. "home.example.com:51820"
    allowed_ips: str = "192.168.1.0/24",
    dns: str = "",
) -> str:
    dns_line = f"DNS = {dns}\n" if dns else ""
    return f"""[Interface]
PrivateKey = {client_private_key}
Address = {client_vpn_ip}/32
{dns_line}
[Peer]
PublicKey = {server_public_key}
Endpoint = {server_endpoint}
AllowedIPs = {allowed_ips}
PersistentKeepalive = 25
"""

def build_server_peer_block(
    client_public_key: str,
    client_vpn_ip: str,
    comment: str = "",
) -> str:
    comment_line = f"# {comment}\n" if comment else ""
    return f"""
{comment_line}[Peer]
PublicKey = {client_public_key}
AllowedIPs = {client_vpn_ip}/32
"""
```

Keep private keys out of source control. If you use this script, write key material
to files with mode 600 and never log or print it.

## pfSense / OPNsense WireGuard

```
# pfSense: VPN → WireGuard → Add Tunnel
  Interface Keys: Generate (creates keypair automatically)
  Listen Port: 51820
  Interface Address: 10.8.0.1/24

# Add Peer (one per client):
  Public Key: <client public key>
  Allowed IPs: 10.8.0.2/32

# Assign the WireGuard interface:
  Interfaces → Assignments → Add (select wg0)
  Enable interface, no IP needed (it is set in the tunnel config)

# Firewall rules:
  WAN → Allow UDP port 51820 inbound (so clients can reach the server)
  WireGuard interface → Allow traffic to LAN networks you want reachable
```

## DDNS (Dynamic DNS) for Home Servers

Most home internet connections have a dynamic IP. Use DDNS so your VPN endpoint
stays reachable after an IP change.

```bash
# Option 1: Cloudflare DDNS — store credentials in a secrets file, not inline
# docker-compose entry using an env file:
  ddns-updater:
    image: qmcgaw/ddns-updater
    env_file: ./ddns.env   # store zone_id and token here, not in compose
    restart: unless-stopped

# ddns.env (chmod 600, not committed to git):
# SETTINGS_CLOUDFLARE_ZONE_ID=your_zone_id
# SETTINGS_CLOUDFLARE_TOKEN=your_api_token

# Option 2: DuckDNS (free, simple)
  Sign up at duckdns.org → get a token and subdomain (myhome.duckdns.org)
  Store token in /etc/ddns.env (mode 600), then use a small root-owned script:

  # /usr/local/bin/update-duckdns
  #!/bin/sh
  set -eu
  . /etc/ddns.env
  curl --fail --silent --show-error --max-time 10 \
    --get "https://www.duckdns.org/update" \
    --data-urlencode "domains=myhome" \
    --data-urlencode "token=${DUCKDNS_TOKEN}" \
    --data-urlencode "ip="

  # Cron job:
  */5 * * * * /usr/local/bin/update-duckdns >/dev/null 2>&1
```

## Troubleshooting

```bash
# Check WireGuard status and last handshake
sudo wg show

# If "latest handshake" is never or very old, the tunnel is not connected.
# Check:
# 1. Is UDP port 51820 open on the router/firewall?
sudo ufw status  # or check pfSense/UniFi firewall rules

# 2. Is the server public key in the client config correct?
sudo wg show wg0 public-key   # Compare to what is in the client config

# 3. Is IP forwarding enabled on the server?
cat /proc/sys/net/ipv4/ip_forward  # Should be 1

# 4. Does the client AllowedIPs cover the IP you are trying to reach?
# If AllowedIPs = 192.168.1.0/24 and you are trying to reach 192.168.3.5, it will not route.

# Check kernel logs for WireGuard errors
dmesg | grep wireguard

# Restart WireGuard
sudo wg-quick down wg0 && sudo wg-quick up wg0
```

## Anti-Patterns

```
# BAD: Storing private keys in version control or sharing them
# Private keys are equivalent to passwords — never commit them to git

# BAD: Using AllowedIPs = 0.0.0.0/0 on mobile without considering the impact
# Full tunnel routes all mobile traffic through your home upload — usually slow

# BAD: Not setting PersistentKeepalive on mobile clients
# Mobile clients behind NAT drop idle tunnels without it

# BAD: Opening port 51820 in the firewall but forgetting IP forwarding on the server
# Tunnel connects but no traffic routes — confusing to debug

# BAD: Sharing a keypair across multiple client devices
# Each device must have its own unique keypair — shared keys break the security model

# BAD: Using a broad "FORWARD ACCEPT" iptables rule
# Scope forwarding rules to the wg0 interface and direction only
```

## Best Practices

- Generate a unique keypair per client device — never reuse keys
- Use split tunneling (`AllowedIPs = <home subnets>`) for mobile
- Set `PersistentKeepalive = 25` on all mobile clients
- Use DDNS if your ISP assigns a dynamic IP; store credentials in env files, not inline
- Use scoped iptables forwarding rules (inbound on wg0 only) rather than a blanket FORWARD ACCEPT
- Add Pi-hole's IP as `DNS =` in client configs to get ad blocking over the VPN
- Rotate the server keypair periodically and update all client configs

## Related Skills

- homelab-network-setup
- homelab-vlan-segmentation
- homelab-pihole-dns

---

# Part 5: Homelab Network Readiness

# Homelab Network Readiness

Use this skill before changing a home or small-lab network that mixes VLANs,
Pi-hole or another local DNS resolver, firewall rules, and remote VPN access.

This is a planning and review skill. Do not turn it into copy-paste router,
firewall, or VPN configuration unless the target platform, current topology,
rollback path, console access, and maintenance window are all known.

## When to Use

- Preparing to split a flat network into trusted, IoT, guest, server, or
  management VLANs.
- Moving DHCP clients to Pi-hole, AdGuard Home, Unbound, or another local DNS
  resolver.
- Adding WireGuard, Tailscale, ZeroTier, OpenVPN, or router-native VPN access.
- Reviewing whether a homelab change can lock the operator out of the gateway,
  switch, access point, DNS server, or VPN server.
- Turning an informal home-network idea into a staged migration plan with
  validation evidence.

## Safety Rules

- Keep the first answer read-only: inventory, risks, staged plan, validation,
  and rollback.
- Do not expose gateway admin panels, DNS resolvers, SSH, NAS consoles, or VPN
  management UIs directly to the public internet.
- Do not provide firewall, NAT, VLAN, DHCP, or VPN commands without a confirmed
  platform and a rollback procedure.
- Require out-of-band or same-room console access before changing management
  VLANs, trunk ports, firewall default policies, or DHCP/DNS settings.
- Keep a working path back to the internet before pointing the whole network at
  a new DNS resolver or VPN route.
- Treat IoT, guest, camera, and lab-server networks as different trust zones
  until the operator explicitly chooses otherwise.

## Required Inventory

Collect this before giving implementation steps:

| Area | Questions |
| --- | --- |
| Internet edge | What is the modem or ONT? Is the ISP router bridged or still routing? |
| Gateway | What routes, firewalls, handles DHCP, and terminates VPNs? |
| Switching | Which switch ports are uplinks, access ports, trunks, or unmanaged? |
| Wi-Fi | Which SSIDs map to which networks, and are APs wired or mesh? |
| Addressing | What subnets exist today, and which ranges conflict with VPN sites? |
| DNS/DHCP | Which service currently hands out leases and resolver addresses? |
| Management | How will the operator reach the gateway, switch, and AP after changes? |
| Recovery | What can be reverted locally if DNS, DHCP, VLANs, or VPN routes break? |

## VLAN And Trust-Zone Plan

Start with intent rather than vendor syntax.

| Zone | Typical contents | Default policy |
| --- | --- | --- |
| Trusted | Laptops, phones, admin workstations | Can reach shared services and management only when needed |
| Servers | NAS, Home Assistant, lab hosts, DNS resolver | Accepts narrow inbound flows from trusted clients |
| IoT | TVs, smart plugs, cameras, speakers | Internet access plus explicit exceptions only |
| Guest | Visitor devices | Internet-only, no LAN reachability |
| Management | Gateway, switches, APs, controllers | Reachable only from trusted admin devices |
| VPN | Remote clients | Same or narrower access than trusted clients |

Before recommending VLAN IDs or subnets, confirm:

1. The gateway supports inter-VLAN routing and firewall rules.
2. The switch supports the required tagged and untagged port behavior.
3. The APs can map SSIDs to VLANs.
4. The operator knows which port they are connected through during the change.
5. The management network remains reachable after trunk and SSID changes.

## DNS Filtering Readiness

Pi-hole or another local resolver should be introduced as a dependency, not as a
single point of failure.

1. Give the resolver a reserved address before using it in DHCP options.
2. Confirm it can resolve public DNS and local `home.arpa` names.
3. Keep the gateway or a second resolver available as a temporary fallback.
4. Test one client or one VLAN before changing every DHCP scope.
5. Document which networks may bypass filtering and why.
6. Check that blocking rules do not break captive portals, work VPNs, firmware
   updates, or medical/security devices.

Useful validation evidence:

```text
Client gets expected DHCP lease
Client receives expected DNS resolver
Public DNS lookup succeeds
Local home.arpa lookup succeeds
Blocked test domain is blocked only where intended
Gateway and DNS admin interfaces are not reachable from guest or IoT networks
```

## Remote Access Readiness

For WireGuard-style access, decide what the VPN is allowed to reach before
generating keys or opening ports.

| Mode | Use when | Risk notes |
| --- | --- | --- |
| Split tunnel to one subnet | Remote admin for NAS or lab hosts | Keep route list narrow |
| Split tunnel to trusted services | Access selected apps by IP or DNS | Requires precise firewall rules |
| Full tunnel | Untrusted networks or travel | More bandwidth and DNS responsibility |
| Overlay VPN | Simpler remote access with identity controls | Still needs ACL review |

Do not recommend port forwarding until the operator confirms:

- The VPN endpoint is patched and actively maintained.
- The forwarded port goes only to the VPN service, not an admin UI.
- Dynamic DNS, public IP behavior, and ISP CGNAT status are understood.
- Peer keys can be revoked without rebuilding the whole network.
- Logs or connection status can verify who connected and when.

## Change Sequence

Prefer small, reversible changes:

1. Snapshot the current topology, IP plan, DHCP settings, DNS settings, and
   firewall rules.
2. Reserve infrastructure addresses for gateway, DNS, controller, APs, NAS, and
   VPN endpoint.
3. Create the new zone or VLAN without moving critical devices.
4. Move one test client and validate DHCP, DNS, routing, internet, and block
   behavior.
5. Add narrow firewall exceptions for required flows.
6. Move one low-risk device group.
7. Add VPN access with the narrowest route and firewall policy that satisfies
   the use case.
8. Document final state, known exceptions, and rollback commands or UI steps.

## Review Checklist

- Each network has a reason to exist and a clear trust boundary.
- No management interface is reachable from guest, IoT, or the public internet.
- DNS failure does not take down the operator's ability to recover locally.
- DHCP scope changes were tested on one client before broad rollout.
- VPN clients receive only the routes and DNS settings they need.
- Firewall rules are default-deny between zones, with named exceptions.
- The operator can still reach gateway, switch, AP, DNS, and VPN admin surfaces.
- Rollback is documented in the same vocabulary as the chosen platform UI or
  CLI.

## Anti-Patterns

- Segmenting networks before knowing which switch ports and SSIDs carry which
  VLANs.
- Moving the admin workstation off the only reachable management network.
- Pointing all DHCP scopes at a Pi-hole before testing fallback DNS.
- Publishing NAS, DNS, router, or hypervisor management directly to the
  internet.
- Treating VPN access as equivalent to full trusted-LAN access.
- Adding allow-all firewall rules temporarily and forgetting to remove them.
- Copying commands from another vendor or firmware version without checking the
  exact platform syntax.

## See Also

- Skill: `homelab-network-setup`
- Skill: `network-config-validation`
- Skill: `network-interface-health`

---
