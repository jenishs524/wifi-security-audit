# 📡 WiFi Security Auditing Tool

### An Educational WPA/WPA2 Handshake Capture & Offline Dictionary Attack Framework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-557C94.svg)](https://www.kali.org/)
[![License](https://img.shields.io/badge/License-MIT%20%2B%20Educational-green.svg)](#license--disclaimer)
[![Status](https://img.shields.io/badge/Status-Educational%20Only-red.svg)](#legal--ethical-notice)

> ⚠️ **FOR EDUCATIONAL USE ONLY — HOME LAB / OWNED NETWORKS ONLY** ⚠️
>
> This tool demonstrates how WPA/WPA2 handshake capture and offline dictionary
> attacks work. It must be used **only on networks you own** or have **explicit
> written permission** to test. Unauthorized use is a criminal offense under the
> Computer Fraud and Abuse Act (USA), Computer Misuse Act (UK), Electronic
> Transactions Act 2063 (Nepal), IT Act 2000 (India), and similar laws worldwide.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Legal & Ethical Notice](#-legal--ethical-notice)
- [Features](#-features)
- [What This Tool Does NOT Do](#-what-this-tool-does-not-do)
- [Workflow / How It Works](#-workflow--how-it-works)
- [Hardware Requirements](#-hardware-requirements)
- [Software Requirements](#-software-requirements)
- [Installation](#-installation)
- [Recommended Lab Setup](#-recommended-lab-setup)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Code Architecture](#-code-architecture)
- [Troubleshooting](#-troubleshooting)
- [Known Limitations](#-known-limitations)
- [Defensive Countermeasures](#-defensive-countermeasures)
- [Learning Outcomes](#-learning-outcomes)
- [Project Structure](#-project-structure)
- [FAQ](#-faq)
- [References](#-references)
- [License & Disclaimer](#-license--disclaimer)
- [Author](#-author)
- [Contributing](#-contributing)
- [Changelog](#-changelog)

---

## 🎯 Overview

This project is a **Python-based WiFi security auditing tool** built as an
educational exercise to understand the mechanics of WPA/WPA2 authentication
and why password entropy — not protocol design — is the real defense against
offline dictionary attacks.

The tool wraps standard, publicly available utilities from the `aircrack-ng`
suite into a guided, phase-by-phase workflow with clear feedback at every step.
It is designed to be **transparent rather than magical**: every phase shows
what is happening and why, so the user learns the underlying concepts.

### Design Philosophy

| Principle | Implementation |
|---|---|
| **Educational transparency** | Every phase prints its purpose and current action |
| **Ethical guardrails** | Multiple confirmation prompts; SSID must be re-typed |
| **Fail-safe defaults** | Auto cleanup on Ctrl+C; refuses to attack ISP-owned SSIDs |
| **No magic** | Uses standard tools; no hidden exploits or zero-days |
| **Reproducibility** | Deterministic workflow; works on any compatible lab |

### Intended Audience

- Cybersecurity students learning wireless security fundamentals
- Penetration testers practicing on home lab equipment
- Network administrators auditing their own infrastructure
- CTF participants preparing for wireless challenges

---

## ⚖️ Legal & Ethical Notice

### By using this tool, you agree that:

1. You will use it **only on networks you personally own**, or on networks
   where you have obtained **explicit, written authorization** from the owner.
2. You understand that **unauthorized network access is a crime** in virtually
   every jurisdiction, with penalties including fines and imprisonment.
3. You understand that **deauthentication attacks disrupt service** to real
   users, which is illegal even on "open" networks you don't own.
4. You will not use this tool against any network named after another person,
   ISP, business, or organization you do not control.
5. You accept **full legal and ethical responsibility** for your actions.

The author(s) of this repository **do not condone, encourage, or take
responsibility for** any misuse. This is a study aid, not an attack kit.

### The "Home Lab" Rule

> If you cannot answer **"I own this router and I know its admin password"**
> with a confident **YES**, you must not target that network.
>
> Seeing a network in the scan list is **not** permission to attack it.

### Legal Reference by Jurisdiction

| Jurisdiction | Statute | Penalty |
|---|---|---|
| USA | Computer Fraud and Abuse Act (18 U.S.C. § 1030) | Up to 10 years imprisonment |
| UK | Computer Misuse Act 1990, §1 | Up to 2 years imprisonment |
| Nepal | Electronic Transactions Act 2063, §45 | Fine + imprisonment |
| India | IT Act 2000, §43, §66 | Up to 3 years imprisonment |
| EU | Directive 2013/40/EU | Member-state dependent |

**You have been warned.**

---

## ✨ Features

### Core Capabilities

| Phase | Feature |
|---|---|
| **1. Interface Discovery** | Enumerates wireless adapters via `iw dev` |
| **2. Reconnaissance** | Scans all nearby APs — SSID, BSSID, channel, signal, security |
| **3. Target Confirmation** | Requires SSID re-type to prove ownership; blocks known ISP SSIDs |
| **4. Monitor Mode** | Automated `airmon-ng` workflow with interference handling |
| **5. Handshake Capture** | `airodump-ng` + `aireplay-ng` to capture the WPA/WPA2 4-way handshake |
| **6. Offline Crack** | `aircrack-ng` dictionary attack with configurable wordlist |
| **7. Cleanup** | Automatic monitor mode teardown and `NetworkManager` restart |

### Safety & Usability Features

- ✅ **Ethical acknowledgement gate** — must type `I AGREE` to proceed
- ✅ **SSID re-type confirmation** — prevents accidental targeting of neighbors
- ✅ **ISP blocklist** — refuses to attack SSIDs matching known ISP patterns
- ✅ **Graceful Ctrl+C handling** — always restores network state
- ✅ **Input validation** — accepts target by number OR BSSID
- ✅ **BSSID extraction from `.cap`** — robust cracking without shell substitution
- ✅ **Old capture cleanup** — no stale `.cap` files confusing the cracker
- ✅ **Colored/structured output** — clear phase separation for learning

---

## ❌ What This Tool Does NOT Do

To be transparent about scope, this tool deliberately excludes:

| Excluded | Why |
|---|---|
| ❌ WPA3 (SAE) attacks | Dragonfly handshake resists offline dictionary attacks |
| ❌ WPS PIN brute force | Different attack class (Reaver/Bully territory) |
| ❌ PMKID clientless attacks | Requires `hcxdumptool` and modern drivers |
| ❌ Evil twin / captive portal phishing | Credential theft, not password cracking |
| ❌ KARMA / MANA attacks | Rogue AP attacks; different scope entirely |
| ❌ Handshake-free attacks | Requires a legitimate client to associate |
| ❌ "One-click" WiFi hacking | Does not exist; real attacks are chains |

Anyone claiming a "one-click WiFi hacker" exists is selling snake oil.
Real WPA2 auditing is a multi-step process with preconditions, and this tool
faithfully reflects that reality.

---

## 🔄 Workflow / How It Works

### High-Level Attack Chain

```
┌──────────────────────────────────────────────────────────────┐
│                     PHASE 1: RECON                           │
│  iw dev → list adapters → user picks one                     │
│  nmcli device wifi rescan → fresh scan                       │
│  nmcli device wifi list → dump SSID/BSSID/CH/SIG/SEC         │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              PHASE 2: TARGET CONFIRMATION                    │
│  User picks # or BSSID                                       │
│  ISP blocklist check → refuse if matches                     │
│  SSID re-type → proves ownership                             │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  PHASE 3: MONITOR MODE                       │
│  airmon-ng check kill → stops NetworkManager + wpa_supplicant│
│  airmon-ng start wlan0 → creates wlan0mon VIF                │
│  Adapter switches: managed → monitor mode                    │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│               PHASE 4: HANDSHAKE CAPTURE                     │
│  airodump-ng locks to target BSSID + channel                 │
│  aireplay-ng sends deauth frames (needs injection)           │
│  Client reconnects → 4-way handshake captured to .cap        │
│  aircrack-ng verifies "1 handshake" present                  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                PHASE 5: OFFLINE CRACK                        │
│  aircrack-ng iterates wordlist                               │
│  For each word: PMK = PBKDF2(word, SSID, 4096, 256)          │
│  Derives PTK → compares MIC against captured handshake       │
│  On match: prints "KEY FOUND! [ password ]"                  │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    PHASE 6: CLEANUP                          │
│  airmon-ng stop wlan0mon → back to managed mode              │
│  systemctl restart NetworkManager → restore normal WiFi      │
└──────────────────────────────────────────────────────────────┘
```

### Detailed Technical Explanation

#### Phase 1 — Reconnaissance

- `iw dev` enumerates wireless interfaces using the `nl80211` kernel API.
- `nmcli device wifi rescan` triggers a fresh scan at the driver level.
- `nmcli -f BSSID,SSID,CHAN,SIGNAL,SECURITY device wifi list` queries the
  NetworkManager cache for discovered APs.

**Why `nmcli` and not `iwlist`?** `nmcli` doesn't require monitor mode, so
the adapter stays usable for normal networking during recon.

#### Phase 2 — Target Confirmation

Two defense-in-depth checks:

1. **ISP blocklist** — SSIDs matching known ISP patterns are refused outright.
2. **SSID re-type** — the user must type the exact SSID to confirm ownership.
   This is a psychological speed bump: no one accidentally types a neighbor's
   SSID character-by-character.

#### Phase 3 — Monitor Mode

- `airmon-ng check kill` terminates `NetworkManager` and `wpa_supplicant`
  because they periodically switch the adapter's channel and would silently
  break the capture.
- `airmon-ng start wlan0` creates a monitor VIF via `iw phy phyX interface
  add wlan0mon type monitor`. Monitor mode receives **all** 802.11 frames on
  the configured channel, not just those addressed to the adapter.

#### Phase 4 — Handshake Capture

This is the crux of the attack:

```
Normal WPA2 association:
  Client ──(1) 802.11 Auth Request──► AP
  Client ◄─(2) 802.11 Auth Response── AP
  Client ──(3) Assoc Request────────► AP
  Client ◄─(4) Assoc Response──────── AP

  4-Way Handshake (EAPOL):
  AP    ──(M1) ANonce ──────────────► Client
  Client ─(M2) SNonce + MIC ────────► AP
  AP    ──(M3) GTK + MIC ───────────► Client
  Client ─(M4) ACK ────────────────► AP
```

Capturing M1 + M2 (or M2 + M3) is enough to attempt an offline crack.

**The deauth trigger:** Because the handshake only happens when a client
joins, we force reconnection by sending forged deauthentication frames. In
WPA2 without PMF (802.11w), deauth frames are unauthenticated — any station
can send them.

#### Phase 5 — Offline Dictionary Attack

For each candidate password `P`:

```
PMK  = PBKDF2-HMAC-SHA1(P, SSID, iterations=4096, dklen=256)
PTK  = PRF-512(PMK, "Pairwise key expansion",
               min(AP_MAC, Client_MAC) ||
               max(AP_MAC, Client_MAC) ||
               min(ANonce, SNonce) ||
               max(ANonce, SNonce))
MIC  = HMAC-SHA1(KCK_from_PTK, EAPOL_frame)
```

If `MIC_computed == MIC_captured`, then `P` is the correct passphrase.

**Complexity:** `PBKDF2` with 4096 iterations means ~1,000–10,000 guesses/sec
on CPU, ~100,000–1,000,000 on GPU. A 12-character random password from a
90-character alphabet has ~90^12 ≈ 2.8 × 10^23 possibilities — computationally
infeasible. This is why **password entropy matters**.

#### Phase 6 — Cleanup

- `airmon-ng stop wlan0mon` removes the monitor VIF.
- `systemctl restart NetworkManager` restores normal WiFi management.
- Without this step, your laptop would have no working WiFi until reboot.

---

## 💻 Hardware Requirements

### WiFi Adapter (Most Common Point of Failure)

| Chipset | Monitor Mode | Injection | Notes |
|---|---|---|---|
| **Atheros AR9271** | ✅ | ✅ | **Best for Kali** — Alfa AWUS036NHA (~$35) |
| **Realtek RTL8812AU** | ✅ | ✅ | Alfa AWUS036ACH, dual-band (~$60) |
| **Ralink RT5572** | ✅ | ✅ | Panda PAU09 (~$35) |
| **MediaTek MT7612U** | ✅ | ✅ | Alfa AWUS036ACM |
| **Intel AX200 / AX210** | ⚠️ Partial | ❌ | Monitor yes, injection unreliable |
| **Qualcomm QCA6174** | ✅ | ❌ | **Monitor yes, injection NO** |
| **Broadcom BCM43xx** | ⚠️ Fragile | ⚠️ | Driver-dependent |

> **Test your adapter:**
> ```bash
> sudo airmon-ng start wlan0
> sudo aireplay-ng --test wlan0mon
> ```
> - `Injection is working!` → you're good
> - `Found 0 APs` / `No Answer` → cannot inject; the deauth phase will fail

### Client Device (Required)

The 4-way handshake **only** happens when a client joins. You need at least
one device connected to the target AP:

- A phone connected to your lab router
- A tablet or spare laptop
- A second wireless adapter on the same machine

### Recommended Home Lab Kit

| Item | Purpose | Est. Cost |
|---|---|---|
| Old router (yours) | Target AP — reset, set `password123` | $0 (reuse) |
| Phone | "Victim" client for handshake generation | $0 (reuse) |
| Laptop with Kali | Attack machine | $0 (reuse) |
| Alfa AWUS036NHA | Injection-capable adapter | ~$35 |
| **Total** | | **~$35** |

---

## 🛠️ Software Requirements

| Component | Version | Purpose |
|---|---|---|
| **Kali Linux** | 2023+ | Recommended OS (or Parrot OS) |
| **Python** | 3.8+ | Runtime |
| **aircrack-ng** | 1.7+ | Includes `airmon-ng`, `airodump-ng`, `aireplay-ng` |
| **network-manager** | 1.40+ | Provides `nmcli` |
| **iw** | 5.0+ | Wireless device management |
| **rockyou.txt** | — | Default wordlist |

### Install Missing Dependencies

```bash
sudo apt update
sudo apt install aircrack-ng network-manager iw
sudo gunzip /usr/share/wordlists/rockyou.txt.gz  # Kali ships it compressed
```

---

## 📥 Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/wifi-security-audit.git
cd wifi-security-audit

# 2. Verify dependencies
for tool in aircrack-ng aireplay-ng airodump-ng airmon-ng nmcli iw; do
    command -v $tool >/dev/null || echo "MISSING: $tool"
done

# 3. Run (root required for monitor mode)
sudo python3 main.py
```

---

## 🧪 Recommended Lab Setup

### Lab Topology

```
    Internet
        │
        ▼
 ┌──────────────┐         ┌──────────────────────┐
 │  Router 1    │◄──eth──►│  Kali Attack Laptop  │
 │  (your home) │         │                      │
 └──────────────┘         │  wlan0  = Alfa USB   │
                          │  eth0   = wired net  │
                          └──────────┬───────────┘
                                     │ monitor mode
                                     ▼
                          ┌──────────────────────┐
                          │  Router 2 (LAB)      │
                          │  SSID: TargetLab     │
                          │  Pass: password123   │
                          │  Ch: 6, WPA2-PSK AES │◄── your phone
                          └──────────────────────┘        (client)
```

### Router 2 Configuration (The Target)

| Setting | Value | Reason |
|---|---|---|
| SSID | `TargetLab` | Easy to identify in scan |
| SSID broadcast | **ON** | Hidden SSIDs are harder to attack |
| Password | `password123` | Deliberately weak for the crack to succeed |
| Security | **WPA2-PSK (AES)** | WPA3 defeats this attack class |
| Band | 2.4 GHz | Broader adapter support |
| Channel | Fixed (e.g., 6) | Auto-channel changes break capture |

### Step-by-Step Lab Setup

1. **Factory reset Router 2** (hold reset button 10s).
2. Log into admin panel (`http://192.168.0.1` or `192.168.1.1`).
3. Configure:
   - SSID: `TargetLab`
   - Password: `password123`
   - Security: WPA2-PSK AES
   - Channel: 6 (fixed)
   - Disable WPS
4. **Connect your phone** to `TargetLab`. Confirm "Connected".
5. **Laptop:** connect Router 1 via **Ethernet** so `wlan0` is free for monitor.

---

## 🚀 Usage

```bash
sudo python3 main.py
```

### Sample Walkthrough

```
==============================================================
   WiFi Security Auditing Tool - EDUCATIONAL USE ONLY
   Test ONLY on networks you own or have permission to test.
==============================================================

[!] ETHICAL ACKNOWLEDGEMENT REQUIRED
    You must confirm you are testing YOUR OWN network
    in a home lab environment, not a public or third-party AP.

Type 'I AGREE' to continue: I AGREE
[+] Acknowledgement received.

[PHASE 1] Available Wireless Interfaces
------------------------------------------
  [1] wlan0
  [2] wlan1

Select interface number: 2

[PHASE 2] Scanning networks on wlan1...
------------------------------------------
#   BSSID               CH   SIG  SEC             SSID
----------------------------------------------------------------------
1   AA:BB:CC:DD:EE:FF   6    65   WPA2            TargetLab
2   11:22:33:44:55:66   11   40   WPA2            NeighborWiFi
3   22:33:44:55:66:77   1    35   WPA2            NTFiber-XXXX

Select target by number (from '#' column) or paste BSSID: 1

[+] Target: TargetLab (AA:BB:CC:DD:EE:FF) Ch 6

[!] STOP and answer honestly:
    Do you OWN this router (you know its admin password)?
    Is it a dedicated LAB router, NOT a neighbor's?
Type the SSID EXACTLY to confirm it is YOURS: TargetLab

[PHASE 3] Enabling monitor mode on wlan1...
------------------------------------------
[+] Monitor interface: wlan1mon

[PHASE 4] Capturing WPA handshake from TargetLab...
------------------------------------------
[*] airodump-ng running: airodump-ng --bssid AA:BB:CC:DD:EE:FF -c 6 \
    -w ./captures/handshake wlan1mon
[*] Waiting 10s for a client to associate...
[*] Sending deauth frames to force handshake...
[*] Watching for handshake (max 90s)...
[+] Handshake captured: ./captures/handshake-01.cap

[PHASE 5] Offline dictionary attack...
------------------------------------------
[*] Wordlist: /usr/share/wordlists/rockyou.txt
[*] Running aircrack-ng (be patient)...
[00:00:02] 14320000 keys tested (7200.32 k/s)
                        KEY FOUND! [ password123 ]

[+] PASSWORD FOUND: password123
[!] Your network's password is weak — change it!

[PHASE 6] Cleaning up...
[+] Monitor mode disabled. NetworkManager restarted.
```

### What to Watch For

| Symptom | Meaning |
|---|---|
| `WPA handshake: <BSSID>` in `airodump-ng` top-right | ✅ Capture succeeded |
| `KEY FOUND! [ xxx ]` | ✅ Crack succeeded |
| `0 handshakes` after Phase 4 | ❌ No client reconnected |
| `Found 0 APs` in injection test | ❌ Card cannot inject |

---

## ⚙️ Configuration

Edit the constants at the top of `main.py`:

```python
# ---------------- CONFIG ----------------
CAPTURE_DIR   = "./captures"                        # Where .cap files go
WORDLIST      = "/usr/share/wordlists/rockyou.txt"  # Wordlist path
SCAN_WAIT     = 8       # Seconds to wait after rescan
CLIENT_WAIT   = 10      # Seconds to look for clients before deauth
MAX_CAP_WAIT  = 90      # Max seconds to wait for handshake
# ----------------------------------------
```

### Custom Wordlists

```bash
# Option 1: SecLists (much larger than rockyou)
sudo apt install seclists
# Then in main.py:
# WORDLIST = "/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"

# Option 2: Generate your own (educational)
# Create a file with one candidate password per line
echo -e "password123\nTargetLab2024\nlab123" > /tmp/mylist.txt
# Then edit WORDLIST to point to /tmp/mylist.txt
```

### Adjusting Timeouts

| Scenario | Recommended Setting |
|---|---|
| Strong signal, fast client | `CLIENT_WAIT = 5`, `MAX_CAP_WAIT = 30` |
| Weak signal, quiet client | `CLIENT_WAIT = 20`, `MAX_CAP_WAIT = 180` |
| Automated lab testing | `SCAN_WAIT = 5` |

---

## 🏗️ Code Architecture

```
main.py
│
├── Utilities
│   ├── run(cmd)                    Wrapper for subprocess.run with timeout
│   ├── banner()                    Prints ASCII banner
│   └── ethical_checkpoint()        Forces "I AGREE" acknowledgement
│
├── Phase 1: Interface Discovery
│   ├── list_interfaces()           Parses `iw dev`
│   └── choose_interface()          User selection with validation
│
├── Phase 2: Reconnaissance
│   ├── scan_networks(iface)        nmcli scan + parse
│   └── choose_target(aps)          #/BSSID selection + ISP block + SSID confirm
│
├── Phase 3: Monitor Mode
│   └── enable_monitor_mode(iface)  airmon-ng workflow
│
├── Phase 4: Handshake Capture
│   └── capture_handshake(mon, tgt) airodump-ng + aireplay-ng
│
├── Phase 5: Offline Crack
│   └── crack_handshake(cap, wl)    aircrack-ng wrapper
│
├── Phase 6: Cleanup
│   └── disable_monitor_mode(mon)   airmon-ng stop + NetworkManager restart
│
└── main()                          Orchestrates all phases with try/finally
```

### Key Design Decisions

| Decision | Rationale |
|---|---|
| Use `subprocess` over pure Python | `aircrack-ng` suite is battle-tested; reinventing is wasteful |
| `nmcli` for scanning | Doesn't require monitor mode; less disruptive |
| Root check at start | Monitor mode needs `CAP_NET_ADMIN` |
| `try/finally` for cleanup | Ensures monitor mode is always disabled, even on Ctrl+C |
| ISP blocklist | Prevents accidental targeting of real networks |
| SSID re-type | Psychological speed bump to prevent careless attacks |
| BSSID parsed from `.cap` | More robust than shell command substitution |

---

## 🔧 Troubleshooting

### "Found 0 APs" during `aireplay-ng --test`

**Cause:** Card doesn't support packet injection (common with laptop cards).

**Fix:**
- Buy an injection-capable USB adapter (Alfa AWUS036NHA).
- **OR:** Skip the deauth step; manually toggle your phone's WiFi to force
  reconnects. The card can still passively capture the handshake.

### `airodump-ng` shows column headers but no APs

**Cause:** `wpa_supplicant` / `NetworkManager` interfering with the card.

**Fix:**
```bash
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

### "No handshake captured" after 90 seconds

**Possible causes:**
1. No client connected during attack.
2. Deauth frames not sent (injection failure).
3. Wrong channel locked.

**Fix:**
- Confirm a client is connected (bottom of `airodump-ng` output).
- Manually toggle the client's WiFi on/off during capture.
- Re-scan and confirm the AP's channel.

### `apt install` fails: "Temporary failure resolving"

**Cause:** `NetworkManager` was stopped, killing DNS.

**Fix:**
```bash
sudo systemctl start NetworkManager
sleep 5
sudo apt update
```

### `aircrack-ng` returns "0 handshakes"

**Cause:** `.cap` file lacks a complete handshake.

**Fix:**
- Recapture. Ensure a client connected *during* the capture window.
- Move closer to the AP for cleaner signal.
- Increase deauth count: `aireplay-ng --deauth 30 ...`.

### Monitor mode won't start

**Cause:** Some drivers (Broadcom, some Realtek) don't support it.

**Fix:**
```bash
# Manual method
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
sudo iw dev wlan0 info   # should show "type monitor"
```

### WiFi doesn't work after the tool exits

**Cause:** `NetworkManager` still stopped.

**Fix:**
```bash
sudo systemctl start NetworkManager
sudo nmcli device status
```

---

## ⚠️ Known Limitations

| Limitation | Impact | Workaround |
|---|---|---|
| **No WPA3 support** | Cannot crack SAE | Use WPA2 target; WPA3 is the defense |
| **No WPS attacks** | Cannot exploit WPS PIN | Use `reaver` / `bully` separately |
| **No PMKID attack** | Needs a connected client | Use `hcxdumptool` separately |
| **No evil twin** | Out of scope (phishing) | Not provided by design |
| **Client required** | No handshake without one | Connect a device to the target |
| **Injection depends on adapter** | Most laptop cards fail | Use Alfa AWUS036NHA |
| **Single-adapter limit** | Can't do AP + monitor at once | Dual-adapter setup |

---

## 🛡️ Defensive Countermeasures

As a security professional, understanding the **defense** is as important as
the attack. Here's how to protect against this class of attack:

### For Network Owners

| Measure | Effect |
|---|---|
| **Use WPA3** | Defeats offline dictionary attacks via SAE |
| **Enable 802.11w (PMF)** | Authenticates deauth frames → blocks deauth attacks |
| **20+ character passphrase** | Makes dictionary attacks computationally infeasible |
| **Disable WPS** | Removes PIN brute-force vector |
| **Disable SSID broadcast** | Mild obscurity (not real security) |
| **Update router firmware** | Patches known vulnerabilities |
| **Monitor for deauth floods** | Use a WIDS (e.g., Kismet, Wazuh) |
| **Use a RADIUS server (WPA2-Enterprise)** | Each user has unique credentials |

### For Enterprise Networks

- Deploy **802.11w (PMF)** mandatory.
- Use **WPA3-Enterprise** with 192-bit security.
- Implement **WIDS/WIPS** to detect rogue APs and deauth floods.
- Use **certificate-based authentication** (EAP-TLS) instead of PSK.
- Segment IoT devices onto separate VLANs.
- Rotate credentials periodically.

### Why WPA3 Matters

| Attack | WPA2 | WPA3 |
|---|---|---|
| Offline dictionary | ✅ Works | ❌ Defeated by SAE |
| Deauth flood | ✅ Works | ❌ Blocked by PMF |
| KRACK | ⚠️ Possible | ✅ Patched |
| Evil twin | ✅ Works | ⚠️ Harder (SAE commits) |

---

## 🎓 Learning Outcomes

After completing a lab with this tool, you should be able to explain:

1. **802.11 frame types** — management, control, data; why deauth frames are
   unauthenticated in WPA2 (and authenticated in WPA3).
2. **The 4-way handshake** — how PMK, PTK, ANonce, SNonce, and MIC interact.
3. **Why offline attacks work** — the handshake leaks enough material to
   test candidate passwords without further network interaction.
4. **Password entropy** — why `password123` falls in <1 second and
   `correct-horse-battery-staple` doesn't fall to a 14M-word list.
5. **Defensive countermeasures** — WPA3, PMF, long passphrases, WIDS.
6. **Why "one-click WiFi hackers" don't exist** — real attacks are chains
   of steps, each with preconditions.

### Suggested Exercises

1. **Baseline:** Crack `password123` — note the time (should be <5 sec).
2. **Weak passphrase:** Change Router 2's password to `Summer2024!` — crack
   again — does it succeed?
3. **Strong passphrase:** Change to `correct-horse-battery-staple` — does it
   crack with `rockyou.txt`? Try `10-million-password-list`?
4. **WPA3 comparison:** Enable WPA3 on Router 2 — does the attack still work?
5. **PMF comparison:** Enable 802.11w — does the deauth step still work?

---

## 📁 Project Structure

```
wifi-security-audit/
├── main.py                 # Main tool
├── captures/               # .cap files (git-ignored)
├── README.md               # This file
├── LICENSE                 # MIT + educational addendum
└── .gitignore              # Ignore captures/__pycache__, etc.
```

### `.gitignore`

```gitignore
# Captures and outputs
captures/
*.cap
*.csv
*.kismet.netxml

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# OS
.DS_Store
Thumbs.db
```

---

## ❓ FAQ

**Q: Is this legal?**
A: Only on networks you own or have **explicit written permission** to test.
Everything else is illegal, even "just scanning."

**Q: Why does it need root?**
A: Monitor mode and raw packet capture require `CAP_NET_ADMIN` and
`CAP_NET_RAW`, which are root-only.

**Q: Why does it need a client device?**
A: The 4-way handshake happens when a client joins. No client = no handshake.

**Q: Can it crack WPA3?**
A: No. WPA3-SAE is resistant to offline dictionary attacks. Different attack
classes (side-channel, downgrade) exist but are far more complex.

**Q: Why does my laptop card fail injection?**
A: Most integrated laptop WiFi cards (Intel, QCA6174, etc.) support monitor
mode but not injection. A USB adapter with an Atheros or Ralink chipset is
the standard solution.

**Q: Can I use this on a public network "just to test"?**
A: **No.** Public networks are not yours. Even scanning can be a crime
depending on jurisdiction.

**Q: How do I make my own network secure?**
A: Use WPA3 (or WPA2 with 802.11w), set a 20+ character passphrase, disable
WPS, and keep router firmware up to date.

**Q: What are the alternatives to writing this myself?**
A: Real tools exist — `aircrack-ng`, `wifite`, `airgeddon`, `wifiphisher`,
`hcxtools`. Use them to learn. Do not reinvent them for a lab.

**Q: Why did you block certain SSIDs?**
A: To prevent accidental targeting of ISP-owned or neighbor networks. If your
legitimate lab SSID matches an ISP pattern, edit `BLOCKED_PATTERNS` in `main.py`.

**Q: Can I run this on Windows or macOS?**
A: No. `aircrack-ng` and monitor mode are Linux-centric. Use Kali in a VM
(with USB passthrough) or bare metal.

**Q: Can I run this in a VM?**
A: Yes, but you must pass a **USB WiFi adapter** through to the VM. Built-in
laptop cards are not visible to VMs in a usable way.

**Q: Why does the tool need to restart NetworkManager?**
A: After monitor mode, the adapter is left in a state NetworkManager can't
use. Restarting it reconnects you to normal WiFi.

---

## 📚 References

### Standards & Specifications
- **IEEE 802.11-2020** — Wireless LAN MAC and PHY specifications
- **IEEE 802.11i-2004** — WPA2 / RSN specification
- **IEEE 802.11w-2009** — Protected Management Frames (PMF)
- **Wi-Fi Alliance WPA3 Specification** — SAE / Dragonfly handshake

### Tools & Documentation
- **aircrack-ng documentation** — https://www.aircrack-ng.org/documentation.html
- **Kali Linux wireless docs** — https://www.kali.org/docs/
- **Wireshark WPA analysis** — https://wiki.wireshark.org/HowToDecrypt802.11

### Learning Platforms
- **TryHackMe — Wifi Hacking 101** — https://tryhackme.com/
- **HackTheBox — Wireless labs** — https://www.hackthebox.com/
- **Cybrary — Penetration Testing** — https://www.cybrary.it/

### Recommended Reading
- *"802.11 Wireless Networks: The Definitive Guide"* — Matthew Gast (O'Reilly)
- *"Hacking Exposed Wireless"* — Johnny Cache, Joshua Wright (McGraw-Hill)
- *"Practical Wireless Exploitation"* — Various authors
- *"The Tangled Web"* — Michał Zalewski (for broader web security context)

### Research Papers
- Vanhoef, M., & Piessens, F. (2017). *"Key Reinstallation Attacks: Forcing
  Nonce Reuse in WPA2."* CCS '17.
- Vanhoef, M., & Ronen, E. (2020). *"Dragonblood: Analyzing the Dragonfly
  Handshake of WPA3 and EAP-pwd."* IEEE S&P '20.

---

## 📜 License & Disclaimer

MIT License — see `LICENSE` file.

### Additional Disclaimer

> This software is provided for **educational purposes only**. The author is
> not responsible for any misuse, damage, or legal consequences resulting from
> its use. By downloading, running, or modifying this software, you agree to
> use it exclusively on networks you own or have written authorization to test.
>
> Network intrusion is a serious crime. Understanding the techniques is part
> of becoming a competent security professional; using them without
> authorization is not. Be the professional, not the criminal.

### License Summary

| Permission | ✅ | Grant |
|---|---|---|
| Commercial use | ✅ | Allowed |
| Modification | ✅ | Allowed |
| Distribution | ✅ | Allowed |
| Private use | ✅ | Allowed |
| **Educational use only** | ⚠️ | Enforced by ethics, not by license |
| Warranty | ❌ | Provided "as is" |
| Liability | ❌ | Author not liable for misuse |

---

## 👤 Author

**Jenish [Last Name]**
Cybersecurity Student | Ethical Hacking Enthusiast
📍 Nepal
🔗 GitHub: [@jenishkali](https://github.com/jenishkali)

### About This Project

Built as a personal learning exercise to understand WPA2 auditing deeply.
The code prioritizes transparency and ethical guardrails over convenience,
reflecting the belief that **understanding the attack is the first step
toward building the defense**.

### Acknowledgments

- The `aircrack-ng` development team for world-class tooling
- Kali Linux maintainers for a security-focused distribution
- The security research community for openly documenting these techniques

---

## 🤝 Contributing

This is a personal educational project. Contributions are welcome if they:

- ✅ Improve documentation or clarity
- ✅ Add **defensive** or **detection** techniques
- ✅ Fix bugs or edge cases
- ✅ Add **WPA3-comparison** features to demonstrate why it's stronger

Contributions that extend offensive capabilities **will be rejected**, as
they fall outside the project's stated educational scope. This is not a
hacking toolkit; it is a study aid.

### Contribution Process

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes: `git commit -m "Add feature X"`.
4. Push to your branch: `git push origin feature/your-feature`.
5. Open a Pull Request with a clear description.

### Code Style

- Python: PEP 8, 4-space indents, 88-char lines
- Commit messages: Conventional Commits (`feat:`, `fix:`, `docs:`)
- Comments: Explain **why**, not **what**

---

## 📝 Changelog

### v1.0.0 (YYYY-MM-DD) — Initial Release

**Added:**
- Phase 1: Interface discovery via `iw dev`
- Phase 2: Recon via `nmcli` with SSID/BSSID/CH/SEC display
- Phase 3: Monitor mode with `airmon-ng` workflow
- Phase 4: Handshake capture (`airodump-ng` + `aireplay-ng`)
- Phase 5: Offline crack (`aircrack-ng` with configurable wordlist)
- Phase 6: Cleanup with auto NetworkManager restart
- Ethical acknowledgement gate (`I AGREE`)
- ISP blocklist for accidental-target prevention
- SSID re-type confirmation for ownership proof
- Graceful Ctrl+C handling
- Target selection by # or BSSID

**Known Issues:**
- Injection fails on Qualcomm QCA6174 (hardware limitation)
- Requires a client device connected to target
- No WPA3 support (by design)

### Roadmap (Future Versions)

- v1.1: Passive survey mode (list clients, probe requests)
- v1.2: Hidden SSID reveal from probe responses
- v1.3: Report generator (HTML/PDF export)
- v1.4: `hcxdumptool` integration for PMKID capture
- v1.5: WPA3 downgrade attack detection

---

## ⭐ Final Note

> *"With knowledge comes responsibility. Understanding how to break WiFi is
> the first step toward making it unbreakable. Use this knowledge to build,
> not to destroy."*

**If this project helped you learn, star the repo — and remember to stay
on the right side of the law.**

---

<p align="center">
  <b>Made with ❤️ for the cybersecurity community</b><br>
  <i>Educational use only — be ethical, be professional</i>
</p>