---
name: homelab
description: |
  Comprehensive homelab and small-network engineering suite covering Network Topology Planning, VLAN Segmentation & Firewall Rules (UniFi, pfSense/OPNsense, MikroTik), Local DNS Filtering & DoH (Pi-hole), WireGuard Remote Access VPN, and Pre-flight Readiness/Lockout Prevention.
triggers:
  - "homelab"
  - "vlan"
  - "pihole"
  - "wireguard"
  - "pfsense"
  - "opnsense"
  - "unifi"
  - "home network"
  - "network segmentation"
license: MIT
metadata:
  origin: community
---

# Homelab & Local Network Engineering Suite

Production-grade guide for designing, segmenting, securing, and operating resilient home and lab networks.

---

## 1. Network Topology & Planning

### Recommended Role Separation
```
Internet / ISP Fiber ONT
       │
Gateway / Firewall Router (pfSense / OPNsense / UniFi Gateway)
   - Handles NAT, DHCP, Routing, Inter-VLAN Firewalls, WireGuard VPN
       │ (802.1Q VLAN Trunk)
Managed Core Switch (UniFi / MikroTik / Cisco)
       ├── Access Port VLAN 10 (Trusted Workstations / NAS)
       ├── Access Port VLAN 20 (Untrusted IoT devices)
       ├── Access Port VLAN 40 (Lab Servers / Docker Hosts)
       └── Trunk Uplink to Access Points (Multi-SSID mapped to VLANs)
```

### IP Subnet Scheme
| VLAN | Subnet | Purpose | Isolation Rules |
|------|--------|---------|-----------------|
| **10 - Trusted** | `192.168.10.0/24` | Main PCs, Laptops, Mobile | Can initiate to all VLANs. |
| **20 - IoT** | `192.168.20.0/24` | Smart TV, Cameras, Bulbs, Home Assistant | Internet only. Blocked from initiating to other VLANs. |
| **30 - Guest** | `192.168.30.0/24` | Visitors | Client isolation + Internet only. |
| **40 - Servers** | `192.168.40.0/24` | NAS, Proxmox, Docker Hosts | Inbound restricted to explicit ports. |
| **50 - Mgmt** | `192.168.50.0/24` | Switch/AP/Router Admin interfaces | Restricted strictly to Trusted admin devices. |

---

## 2. VLAN Segmentation & Firewall Rules

### Inter-VLAN Firewall Rules (pfSense / OPNsense / UniFi)
Apply these rules in order on the IoT and Guest interfaces:

1. **Allow DNS & DHCP to Gateway/Pi-hole**:
   - Action: Pass
   - Protocol: UDP/TCP
   - Destination: `192.168.10.5` (Pi-hole) or Gateway IP, Port `53`, `67-68`
2. **Allow Established & Related Connections**:
   - Action: Pass (Stateful matching)
3. **Block Access to Private Networks (RFC 1918)**:
   - Action: Block
   - Destination: Alias `RFC1918_Subnets` (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)
4. **Allow Outbound to WAN (Internet)**:
   - Action: Pass
   - Destination: `*` (Any)

---

## 3. Local DNS & Ad-Blocking (Pi-hole + DoH)

Deploy Pi-hole and Cloudflare DNS-over-HTTPS securely with Docker Compose:

```yaml
services:
  pihole:
    container_name: pihole
    image: pihole/pihole:latest
    restart: unless-stopped
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "8080:80/tcp"
    environment:
      TZ: 'UTC'
      WEBPASSWORD: 'SecureAdminPassword'
      PIHOLE_DNS_: '172.20.0.3#5053' # Upstream DoH container
    volumes:
      - './etc-pihole:/etc/pihole'
      - './etc-dnsmasq.d:/etc/dnsmasq.d'
    networks:
      pihole_net:
        ipv4_address: 172.20.0.2

  cloudflared:
    container_name: cloudflared
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    command: proxy-dns --port 5053 --upstream https://1.1.1.1/dns-query --upstream https://1.0.0.1/dns-query
    networks:
      pihole_net:
        ipv4_address: 172.20.0.3

networks:
  pihole_net:
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

---

## 4. WireGuard Remote Access VPN

### Server Configuration (`/etc/wireguard/wg0.conf`)
```ini
[Interface]
Address = 10.100.0.1/24
ListenPort = 51820
PrivateKey = SERVER_PRIVATE_KEY
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Client: Mobile Phone
[Peer]
PublicKey = PHONE_PUBLIC_KEY
AllowedIPs = 10.100.0.2/32

# Client: Laptop
[Peer]
PublicKey = LAPTOP_PUBLIC_KEY
AllowedIPs = 10.100.0.3/32
```

### Client Split-Tunnel Profile (`phone.conf`)
```ini
[Interface]
PrivateKey = PHONE_PRIVATE_KEY
Address = 10.100.0.2/24
DNS = 192.168.10.5

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = your-home-ddns.example.com:51820
# Split tunnel: Route only homelab traffic through VPN
AllowedIPs = 192.168.10.0/24, 192.168.40.0/24, 10.100.0.0/24
PersistentKeepalive = 25
```

---

## 5. Pre-Flight Readiness & Lockout Prevention Checklist

Before making router, switch, or firewall changes:

- [ ] **Out-of-band Console Access**: Verify direct Ethernet console or serial connection to router/switch is available.
- [ ] **Configuration Backup**: Download current running configuration (`.xml` or `.unf`).
- [ ] **Maintenance Window**: Never apply network resegmentation during peak hours.
- [ ] **Rollback Plan**: Know the exact keystrokes/commands to revert firewall rule changes.
- [ ] **Never Expose Admin Panels**: Keep pfSense/UniFi management and SSH restricted to VLAN 50 / Trusted LAN; never expose to public WAN.
