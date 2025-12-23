#!/usr/bin/env python3
"""
Evidence Logger - Cryptographically Timestamped Documentation System

Creates tamper-evident logs of device states, observations, and evidence
for legal documentation purposes. Uses SHA-256 hash chains to prove
temporal ordering and detect any modifications.

Legal Note: This tool creates documentation only. It does not intercept,
modify, or interfere with any systems.
"""

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class EvidenceLogger:
    """Maintains a hash-chained log of evidence entries."""

    def __init__(self, log_dir: str = "evidence_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "evidence_chain.jsonl"
        self.last_hash = self._get_last_hash()

    def _get_last_hash(self) -> str:
        """Get the hash of the last entry, or genesis hash if empty."""
        if not self.log_file.exists():
            return hashlib.sha256(b"GENESIS").hexdigest()

        last_line = ""
        with open(self.log_file, 'r') as f:
            for line in f:
                if line.strip():
                    last_line = line

        if not last_line:
            return hashlib.sha256(b"GENESIS").hexdigest()

        try:
            entry = json.loads(last_line)
            return entry.get("entry_hash", hashlib.sha256(b"GENESIS").hexdigest())
        except json.JSONDecodeError:
            return hashlib.sha256(b"GENESIS").hexdigest()

    def _compute_hash(self, data: dict, prev_hash: str) -> str:
        """Compute SHA-256 hash of entry data chained to previous hash."""
        content = json.dumps(data, sort_keys=True) + prev_hash
        return hashlib.sha256(content.encode()).hexdigest()

    def log_entry(self, category: str, description: str,
                  data: Optional[dict] = None,
                  attachments: Optional[list] = None) -> dict:
        """
        Log an evidence entry with cryptographic timestamp chain.

        Args:
            category: Type of evidence (observation, device_state, anomaly, etc.)
            description: Human-readable description
            data: Structured data to record
            attachments: List of file paths to hash and reference

        Returns:
            The complete logged entry
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        entry_data = {
            "timestamp": timestamp,
            "category": category,
            "description": description,
            "data": data or {},
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "python": platform.python_version()
            }
        }

        # Hash any attachments
        if attachments:
            attachment_hashes = []
            for filepath in attachments:
                path = Path(filepath)
                if path.exists():
                    with open(path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    attachment_hashes.append({
                        "filename": path.name,
                        "path": str(path.absolute()),
                        "sha256": file_hash,
                        "size_bytes": path.stat().st_size
                    })
            entry_data["attachments"] = attachment_hashes

        # Create hash chain
        entry_hash = self._compute_hash(entry_data, self.last_hash)

        full_entry = {
            "prev_hash": self.last_hash,
            "entry_hash": entry_hash,
            **entry_data
        }

        # Append to log
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(full_entry) + "\n")

        self.last_hash = entry_hash

        print(f"[{timestamp}] Logged: {category} - {description[:50]}...")
        print(f"  Hash: {entry_hash[:16]}...")

        return full_entry

    def verify_chain(self) -> tuple[bool, list]:
        """
        Verify the integrity of the entire evidence chain.

        Returns:
            (is_valid, list of any errors found)
        """
        if not self.log_file.exists():
            return True, []

        errors = []
        prev_hash = hashlib.sha256(b"GENESIS").hexdigest()

        with open(self.log_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    errors.append(f"Line {line_num}: Invalid JSON - {e}")
                    continue

                # Verify previous hash link
                if entry.get("prev_hash") != prev_hash:
                    errors.append(
                        f"Line {line_num}: Chain break - expected prev_hash "
                        f"{prev_hash[:16]}..., got {entry.get('prev_hash', 'MISSING')[:16]}..."
                    )

                # Verify entry hash
                entry_data = {
                    "timestamp": entry.get("timestamp"),
                    "category": entry.get("category"),
                    "description": entry.get("description"),
                    "data": entry.get("data", {}),
                    "platform": entry.get("platform", {})
                }
                if "attachments" in entry:
                    entry_data["attachments"] = entry["attachments"]

                computed_hash = self._compute_hash(entry_data, entry.get("prev_hash", ""))
                if computed_hash != entry.get("entry_hash"):
                    errors.append(
                        f"Line {line_num}: Hash mismatch - entry may have been modified"
                    )

                prev_hash = entry.get("entry_hash", prev_hash)

        return len(errors) == 0, errors

    def export_for_legal(self, output_file: str = "evidence_export.json") -> str:
        """Export the full chain with verification metadata for legal use."""
        is_valid, errors = self.verify_chain()

        entries = []
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))

        export = {
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "chain_valid": is_valid,
            "verification_errors": errors,
            "total_entries": len(entries),
            "first_entry": entries[0]["timestamp"] if entries else None,
            "last_entry": entries[-1]["timestamp"] if entries else None,
            "entries": entries
        }

        output_path = self.log_dir / output_file
        with open(output_path, 'w') as f:
            json.dump(export, f, indent=2)

        print(f"Exported {len(entries)} entries to {output_path}")
        print(f"Chain integrity: {'VALID' if is_valid else 'ERRORS FOUND'}")

        return str(output_path)


class DeviceStateCapture:
    """Capture current device state for documentation."""

    @staticmethod
    def get_system_info() -> dict:
        """Get basic system information."""
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node()
        }

    @staticmethod
    def get_os_build_info() -> dict:
        """Get OS build/version information."""
        info = {"platform": platform.system()}

        if platform.system() == "Darwin":
            # macOS
            try:
                result = subprocess.run(
                    ["sw_vers"], capture_output=True, text=True, timeout=10
                )
                for line in result.stdout.strip().split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        info[key.strip().lower().replace(' ', '_')] = val.strip()
            except Exception as e:
                info["error"] = str(e)

            # Get build info
            try:
                result = subprocess.run(
                    ["system_profiler", "SPSoftwareDataType"],
                    capture_output=True, text=True, timeout=30
                )
                info["system_profiler_software"] = result.stdout.strip()
            except Exception:
                pass

        elif platform.system() == "Linux":
            # Linux - try to get distribution info
            try:
                with open("/etc/os-release", 'r') as f:
                    for line in f:
                        if '=' in line:
                            key, val = line.strip().split('=', 1)
                            info[key.lower()] = val.strip('"')
            except FileNotFoundError:
                pass

            # Kernel version
            try:
                result = subprocess.run(
                    ["uname", "-a"], capture_output=True, text=True, timeout=10
                )
                info["kernel"] = result.stdout.strip()
            except Exception:
                pass

        elif platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["systeminfo"], capture_output=True, text=True, timeout=60
                )
                info["systeminfo"] = result.stdout.strip()
            except Exception as e:
                info["error"] = str(e)

        return info

    @staticmethod
    def get_network_interfaces() -> dict:
        """Get network interface information."""
        info = {}

        try:
            if platform.system() == "Darwin" or platform.system() == "Linux":
                result = subprocess.run(
                    ["ifconfig"], capture_output=True, text=True, timeout=10
                )
                info["ifconfig"] = result.stdout.strip()
            elif platform.system() == "Windows":
                result = subprocess.run(
                    ["ipconfig", "/all"], capture_output=True, text=True, timeout=10
                )
                info["ipconfig"] = result.stdout.strip()
        except Exception as e:
            info["error"] = str(e)

        return info

    @staticmethod
    def get_running_processes() -> list:
        """Get list of running processes."""
        processes = []

        try:
            if platform.system() == "Darwin" or platform.system() == "Linux":
                result = subprocess.run(
                    ["ps", "aux"], capture_output=True, text=True, timeout=10
                )
                processes = result.stdout.strip().split('\n')
            elif platform.system() == "Windows":
                result = subprocess.run(
                    ["tasklist"], capture_output=True, text=True, timeout=10
                )
                processes = result.stdout.strip().split('\n')
        except Exception as e:
            processes = [f"Error: {e}"]

        return processes

    @staticmethod
    def get_installed_certificates() -> dict:
        """Get information about installed certificates (metadata only)."""
        info = {}

        try:
            if platform.system() == "Darwin":
                # List keychains
                result = subprocess.run(
                    ["security", "list-keychains"],
                    capture_output=True, text=True, timeout=10
                )
                info["keychains"] = result.stdout.strip().split('\n')

                # Count certificates in system keychain
                result = subprocess.run(
                    ["security", "find-certificate", "-a", "/Library/Keychains/System.keychain"],
                    capture_output=True, text=True, timeout=30
                )
                cert_count = result.stdout.count('keychain:')
                info["system_cert_count"] = cert_count

        except Exception as e:
            info["error"] = str(e)

        return info


def capture_full_state(logger: EvidenceLogger) -> dict:
    """Capture and log complete device state."""
    capture = DeviceStateCapture()

    state = {
        "system_info": capture.get_system_info(),
        "os_build": capture.get_os_build_info(),
        "network": capture.get_network_interfaces(),
        "process_count": len(capture.get_running_processes()),
        "certificates": capture.get_installed_certificates()
    }

    entry = logger.log_entry(
        category="device_state",
        description="Full device state capture",
        data=state
    )

    return entry


def main():
    """Main CLI interface."""
    logger = EvidenceLogger()

    if len(sys.argv) < 2:
        print("Evidence Logger - Cryptographically Timestamped Documentation")
        print()
        print("Usage:")
        print("  python evidence_logger.py capture     - Capture full device state")
        print("  python evidence_logger.py log <desc>  - Log an observation")
        print("  python evidence_logger.py verify      - Verify chain integrity")
        print("  python evidence_logger.py export      - Export for legal use")
        print()
        return

    cmd = sys.argv[1].lower()

    if cmd == "capture":
        print("Capturing device state...")
        entry = capture_full_state(logger)
        print(f"\nState captured. Entry hash: {entry['entry_hash']}")

    elif cmd == "log":
        if len(sys.argv) < 3:
            print("Usage: python evidence_logger.py log <description>")
            return
        description = " ".join(sys.argv[2:])
        entry = logger.log_entry(
            category="observation",
            description=description
        )
        print(f"\nLogged. Entry hash: {entry['entry_hash']}")

    elif cmd == "verify":
        print("Verifying evidence chain integrity...")
        is_valid, errors = logger.verify_chain()
        if is_valid:
            print("Chain integrity: VALID")
        else:
            print("Chain integrity: ERRORS FOUND")
            for error in errors:
                print(f"  - {error}")

    elif cmd == "export":
        print("Exporting evidence for legal use...")
        path = logger.export_for_legal()
        print(f"Export complete: {path}")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
