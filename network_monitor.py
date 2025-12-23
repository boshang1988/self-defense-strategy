#!/usr/bin/env python3
"""
Network Monitor - Connection Documentation Tool

Documents network connections, DNS queries, and traffic metadata
for forensic analysis. Does NOT intercept or modify traffic.

This tool captures metadata only - connection endpoints, timing,
and protocol information for evidentiary documentation.
"""

import json
import subprocess
import sys
import time
import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class ConnectionRecord:
    """A single network connection record."""
    timestamp: str
    protocol: str
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    state: str
    process: str
    pid: Optional[int]


class NetworkMonitor:
    """Monitor and document network connections."""

    def __init__(self, output_dir: str = "network_logs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.output_dir / "connections.jsonl"
        self.baseline_file = self.output_dir / "baseline.json"

    def get_current_connections(self) -> list:
        """Get current network connections using netstat/lsof."""
        connections = []
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            # Use lsof for detailed connection info on macOS
            result = subprocess.run(
                ["lsof", "-i", "-n", "-P"],
                capture_output=True, text=True, timeout=30
            )

            for line in result.stdout.strip().split('\n')[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 9:
                    try:
                        # Parse lsof output
                        command = parts[0]
                        pid = int(parts[1]) if parts[1].isdigit() else None
                        protocol = parts[7] if len(parts) > 7 else "unknown"

                        # Parse address info
                        name = parts[-1] if parts else ""
                        state = parts[-2] if len(parts) > 9 else ""

                        # Parse local->remote
                        if "->" in name:
                            local, remote = name.split("->")
                        else:
                            local = name
                            remote = ""

                        # Parse addresses
                        def parse_addr(addr_str):
                            if ":" in addr_str:
                                parts = addr_str.rsplit(":", 1)
                                return parts[0], int(parts[1]) if parts[1].isdigit() else 0
                            return addr_str, 0

                        local_addr, local_port = parse_addr(local)
                        remote_addr, remote_port = parse_addr(remote) if remote else ("", 0)

                        conn = ConnectionRecord(
                            timestamp=timestamp,
                            protocol=protocol.lower(),
                            local_address=local_addr,
                            local_port=local_port,
                            remote_address=remote_addr,
                            remote_port=remote_port,
                            state=state if state in ["ESTABLISHED", "LISTEN", "TIME_WAIT", "CLOSE_WAIT"] else "",
                            process=command,
                            pid=pid
                        )
                        connections.append(conn)
                    except (ValueError, IndexError):
                        continue

        except Exception as e:
            print(f"Error getting connections: {e}")

        return connections

    def get_dns_servers(self) -> list:
        """Get configured DNS servers."""
        servers = []

        try:
            result = subprocess.run(
                ["scutil", "--dns"],
                capture_output=True, text=True, timeout=10
            )

            for line in result.stdout.split('\n'):
                if 'nameserver' in line.lower():
                    parts = line.split(':')
                    if len(parts) > 1:
                        server = parts[1].strip()
                        if server and server not in servers:
                            servers.append(server)
        except Exception:
            pass

        # Also check resolv.conf
        try:
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        parts = line.split()
                        if len(parts) > 1:
                            servers.append(parts[1])
        except Exception:
            pass

        return list(set(servers))

    def get_routing_table(self) -> str:
        """Get current routing table."""
        try:
            result = subprocess.run(
                ["netstat", "-rn"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error: {e}"

    def get_arp_table(self) -> str:
        """Get ARP table."""
        try:
            result = subprocess.run(
                ["arp", "-a"],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout
        except Exception as e:
            return f"Error: {e}"

    def get_listening_ports(self) -> list:
        """Get all listening ports."""
        listening = []
        timestamp = datetime.now(timezone.utc).isoformat()

        try:
            result = subprocess.run(
                ["lsof", "-i", "-n", "-P", "-sTCP:LISTEN"],
                capture_output=True, text=True, timeout=30
            )

            for line in result.stdout.strip().split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 9:
                    listening.append({
                        "process": parts[0],
                        "pid": parts[1],
                        "address": parts[-1],
                        "timestamp": timestamp
                    })
        except Exception:
            pass

        return listening

    def create_baseline(self) -> dict:
        """Create a baseline of normal network state."""
        print("Creating network baseline...")

        baseline = {
            "created": datetime.now(timezone.utc).isoformat(),
            "dns_servers": self.get_dns_servers(),
            "routing_table_hash": hashlib.sha256(
                self.get_routing_table().encode()
            ).hexdigest(),
            "listening_ports": self.get_listening_ports(),
            "connection_count": len(self.get_current_connections())
        }

        with open(self.baseline_file, 'w') as f:
            json.dump(baseline, f, indent=2)

        print(f"Baseline saved to: {self.baseline_file}")
        return baseline

    def compare_to_baseline(self) -> dict:
        """Compare current state to baseline."""
        if not self.baseline_file.exists():
            return {"error": "No baseline exists. Run 'baseline' command first."}

        with open(self.baseline_file) as f:
            baseline = json.load(f)

        current = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dns_servers": self.get_dns_servers(),
            "routing_table_hash": hashlib.sha256(
                self.get_routing_table().encode()
            ).hexdigest(),
            "listening_ports": self.get_listening_ports()
        }

        changes = {
            "baseline_created": baseline["created"],
            "comparison_time": current["timestamp"],
            "changes": []
        }

        # Check DNS
        baseline_dns = set(baseline.get("dns_servers", []))
        current_dns = set(current["dns_servers"])

        if baseline_dns != current_dns:
            changes["changes"].append({
                "type": "dns_servers_changed",
                "baseline": list(baseline_dns),
                "current": list(current_dns),
                "added": list(current_dns - baseline_dns),
                "removed": list(baseline_dns - current_dns)
            })

        # Check routing
        if baseline.get("routing_table_hash") != current["routing_table_hash"]:
            changes["changes"].append({
                "type": "routing_table_changed",
                "baseline_hash": baseline.get("routing_table_hash"),
                "current_hash": current["routing_table_hash"]
            })

        # Check listening ports
        baseline_ports = {p["address"] for p in baseline.get("listening_ports", [])}
        current_ports = {p["address"] for p in current["listening_ports"]}

        new_ports = current_ports - baseline_ports
        if new_ports:
            changes["changes"].append({
                "type": "new_listening_ports",
                "ports": list(new_ports)
            })

        return changes

    def log_connections(self, duration_seconds: int = 60, interval: int = 5):
        """Log connections over a time period."""
        print(f"Logging connections for {duration_seconds} seconds (interval: {interval}s)")

        start_time = time.time()
        samples = 0

        while time.time() - start_time < duration_seconds:
            connections = self.get_current_connections()

            with open(self.log_file, 'a') as f:
                for conn in connections:
                    f.write(json.dumps(asdict(conn)) + "\n")

            samples += 1
            print(f"  Sample {samples}: {len(connections)} connections")

            time.sleep(interval)

        print(f"\nLogged {samples} samples to {self.log_file}")

    def analyze_logged_connections(self) -> dict:
        """Analyze logged connections for patterns."""
        if not self.log_file.exists():
            return {"error": "No connection log found"}

        connections = []
        with open(self.log_file) as f:
            for line in f:
                if line.strip():
                    connections.append(json.loads(line))

        # Analyze patterns
        remote_hosts = {}
        processes = {}
        ports = {}

        for conn in connections:
            remote = conn.get("remote_address", "")
            if remote:
                remote_hosts[remote] = remote_hosts.get(remote, 0) + 1

            proc = conn.get("process", "")
            if proc:
                processes[proc] = processes.get(proc, 0) + 1

            remote_port = conn.get("remote_port", 0)
            if remote_port:
                ports[remote_port] = ports.get(remote_port, 0) + 1

        # Sort by frequency
        top_hosts = sorted(remote_hosts.items(), key=lambda x: x[1], reverse=True)[:20]
        top_processes = sorted(processes.items(), key=lambda x: x[1], reverse=True)[:20]
        top_ports = sorted(ports.items(), key=lambda x: x[1], reverse=True)[:20]

        return {
            "total_connections_logged": len(connections),
            "unique_remote_hosts": len(remote_hosts),
            "top_remote_hosts": top_hosts,
            "top_processes": top_processes,
            "top_remote_ports": top_ports
        }

    def snapshot(self) -> dict:
        """Take a complete network snapshot."""
        print("Taking network snapshot...")

        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "connections": [asdict(c) for c in self.get_current_connections()],
            "listening_ports": self.get_listening_ports(),
            "dns_servers": self.get_dns_servers(),
            "routing_table": self.get_routing_table(),
            "arp_table": self.get_arp_table()
        }

        # Compute hash of snapshot
        snapshot["snapshot_hash"] = hashlib.sha256(
            json.dumps(snapshot, sort_keys=True).encode()
        ).hexdigest()[:32]

        output_file = self.output_dir / f"snapshot_{snapshot['snapshot_hash']}.json"
        with open(output_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"Snapshot saved: {output_file}")
        print(f"  Connections: {len(snapshot['connections'])}")
        print(f"  Listening ports: {len(snapshot['listening_ports'])}")
        print(f"  DNS servers: {snapshot['dns_servers']}")

        return snapshot


def main():
    print("Network Monitor - Connection Documentation Tool")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python network_monitor.py snapshot     - Take network snapshot")
        print("  python network_monitor.py baseline     - Create baseline")
        print("  python network_monitor.py compare      - Compare to baseline")
        print("  python network_monitor.py log [secs]   - Log connections (default 60s)")
        print("  python network_monitor.py analyze      - Analyze logged connections")
        print("  python network_monitor.py listen       - Show listening ports")
        return

    cmd = sys.argv[1].lower()
    monitor = NetworkMonitor()

    if cmd == "snapshot":
        monitor.snapshot()

    elif cmd == "baseline":
        monitor.create_baseline()

    elif cmd == "compare":
        changes = monitor.compare_to_baseline()
        print(json.dumps(changes, indent=2))

        if changes.get("changes"):
            print(f"\n⚠ Found {len(changes['changes'])} changes from baseline")

    elif cmd == "log":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        monitor.log_connections(duration)

    elif cmd == "analyze":
        analysis = monitor.analyze_logged_connections()
        print(json.dumps(analysis, indent=2))

    elif cmd == "listen":
        ports = monitor.get_listening_ports()
        print(f"\nListening ports ({len(ports)}):")
        for p in ports:
            print(f"  {p['process']} (PID {p['pid']}): {p['address']}")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
