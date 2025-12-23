#!/usr/bin/env python3
"""
Build Forensics - Code Signing & Build Verification Toolkit

Collects and documents cryptographic signing artifacts, build identifiers,
certificate chains, and update metadata for forensic analysis.

This tool captures METADATA ONLY - it does not modify, intercept, or
interfere with any signing processes.
"""

import hashlib
import json
import os
import plistlib
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class SigningArtifactCollector:
    """Collect code signing artifacts and certificate metadata."""

    def __init__(self, output_dir: str = "forensics_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.collection_time = datetime.now(timezone.utc)

    def collect_macos_signing_info(self, app_path: str) -> dict:
        """Collect code signing info for a macOS application or binary."""
        result = {
            "path": app_path,
            "collection_time": self.collection_time.isoformat(),
            "exists": os.path.exists(app_path)
        }

        if not result["exists"]:
            return result

        # Get code signature details
        try:
            proc = subprocess.run(
                ["codesign", "-dvvv", app_path],
                capture_output=True, text=True, timeout=30
            )
            result["codesign_details"] = proc.stderr  # codesign outputs to stderr
            result["codesign_exit"] = proc.returncode
        except Exception as e:
            result["codesign_error"] = str(e)

        # Get certificate chain
        try:
            proc = subprocess.run(
                ["codesign", "-d", "--extract-certificates", app_path],
                capture_output=True, text=True, timeout=30,
                cwd=str(self.output_dir)
            )
            # Look for extracted certs
            cert_files = list(self.output_dir.glob("codesign*.cer"))
            result["extracted_certs"] = len(cert_files)

            # Get cert details
            cert_info = []
            for cert_file in cert_files:
                try:
                    cert_proc = subprocess.run(
                        ["openssl", "x509", "-inform", "DER", "-in", str(cert_file),
                         "-noout", "-subject", "-issuer", "-dates", "-serial",
                         "-fingerprint", "-sha256"],
                        capture_output=True, text=True, timeout=10
                    )
                    cert_info.append({
                        "file": cert_file.name,
                        "details": cert_proc.stdout
                    })
                except Exception as e:
                    cert_info.append({"file": cert_file.name, "error": str(e)})

            result["certificate_chain"] = cert_info
        except Exception as e:
            result["cert_extraction_error"] = str(e)

        # Verify signature
        try:
            proc = subprocess.run(
                ["codesign", "--verify", "--deep", "--strict", app_path],
                capture_output=True, text=True, timeout=60
            )
            result["signature_valid"] = proc.returncode == 0
            result["verify_output"] = proc.stderr or proc.stdout
        except Exception as e:
            result["verify_error"] = str(e)

        # Get entitlements
        try:
            proc = subprocess.run(
                ["codesign", "-d", "--entitlements", "-", app_path],
                capture_output=True, text=True, timeout=30
            )
            result["entitlements"] = proc.stdout
        except Exception as e:
            result["entitlements_error"] = str(e)

        return result

    def collect_system_build_info(self) -> dict:
        """Collect macOS system build identifiers and version info."""
        info = {
            "collection_time": self.collection_time.isoformat(),
            "platform": "macOS"
        }

        # sw_vers
        try:
            proc = subprocess.run(
                ["sw_vers"], capture_output=True, text=True, timeout=10
            )
            for line in proc.stdout.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    info[key.strip().lower().replace(' ', '_')] = val.strip()
        except Exception as e:
            info["sw_vers_error"] = str(e)

        # System version plist
        try:
            with open("/System/Library/CoreServices/SystemVersion.plist", 'rb') as f:
                plist = plistlib.load(f)
                info["system_version_plist"] = {k: str(v) for k, v in plist.items()}
        except Exception as e:
            info["plist_error"] = str(e)

        # Boot args / nvram
        try:
            proc = subprocess.run(
                ["nvram", "-p"], capture_output=True, text=True, timeout=10
            )
            # Only capture specific boot-related variables
            boot_vars = {}
            for line in proc.stdout.split('\n'):
                if any(k in line.lower() for k in ['boot', 'secure', 'csrutil']):
                    if '\t' in line:
                        key, val = line.split('\t', 1)
                        boot_vars[key] = val[:200]  # Limit length
            info["nvram_boot_vars"] = boot_vars
        except Exception as e:
            info["nvram_error"] = str(e)

        # SIP status
        try:
            proc = subprocess.run(
                ["csrutil", "status"], capture_output=True, text=True, timeout=10
            )
            info["sip_status"] = proc.stdout.strip()
        except Exception as e:
            info["sip_error"] = str(e)

        # Secure boot status (Apple Silicon)
        try:
            proc = subprocess.run(
                ["bputil", "-d"], capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0:
                info["secure_boot_policy"] = proc.stdout.strip()
        except Exception:
            pass  # Not available on Intel Macs

        return info

    def collect_update_history(self) -> dict:
        """Collect software update history and receipts."""
        info = {
            "collection_time": self.collection_time.isoformat()
        }

        # Software update history
        try:
            proc = subprocess.run(
                ["softwareupdate", "--history"],
                capture_output=True, text=True, timeout=30
            )
            info["update_history"] = proc.stdout.strip()
        except Exception as e:
            info["history_error"] = str(e)

        # Install history from receipts
        receipts_dir = Path("/var/db/receipts")
        if receipts_dir.exists():
            receipt_info = []
            for plist_file in sorted(receipts_dir.glob("*.plist"))[-50:]:  # Last 50
                try:
                    with open(plist_file, 'rb') as f:
                        plist = plistlib.load(f)
                        receipt_info.append({
                            "file": plist_file.name,
                            "package_id": plist.get("PackageIdentifier", ""),
                            "version": plist.get("PackageVersion", ""),
                            "install_date": str(plist.get("InstallDate", "")),
                            "install_prefixes": plist.get("InstallPrefixes", [])
                        })
                except Exception:
                    pass
            info["install_receipts"] = receipt_info

        # Check for unusual update sources
        try:
            proc = subprocess.run(
                ["defaults", "read", "/Library/Preferences/com.apple.SoftwareUpdate"],
                capture_output=True, text=True, timeout=10
            )
            info["softwareupdate_prefs"] = proc.stdout.strip()
        except Exception:
            pass

        return info

    def collect_trust_settings(self) -> dict:
        """Collect certificate trust settings and anchors."""
        info = {
            "collection_time": self.collection_time.isoformat()
        }

        # System roots
        try:
            proc = subprocess.run(
                ["security", "find-certificate", "-a", "-p",
                 "/System/Library/Keychains/SystemRootCertificates.keychain"],
                capture_output=True, text=True, timeout=60
            )
            # Count certificates
            cert_count = proc.stdout.count("-----BEGIN CERTIFICATE-----")
            info["system_root_cert_count"] = cert_count

            # Hash the entire output for change detection
            info["system_roots_hash"] = hashlib.sha256(
                proc.stdout.encode()
            ).hexdigest()
        except Exception as e:
            info["system_roots_error"] = str(e)

        # User-added trust overrides
        try:
            proc = subprocess.run(
                ["security", "dump-trust-settings"],
                capture_output=True, text=True, timeout=30
            )
            info["user_trust_settings"] = proc.stdout.strip()
        except Exception as e:
            info["trust_settings_error"] = str(e)

        # Admin trust settings
        try:
            proc = subprocess.run(
                ["security", "dump-trust-settings", "-d"],
                capture_output=True, text=True, timeout=30
            )
            info["admin_trust_settings"] = proc.stdout.strip()
        except Exception as e:
            pass

        return info

    def hash_binary(self, path: str) -> dict:
        """Compute multiple hashes of a binary for verification."""
        result = {"path": path}

        if not os.path.exists(path):
            result["error"] = "File not found"
            return result

        try:
            with open(path, 'rb') as f:
                data = f.read()

            result["size_bytes"] = len(data)
            result["md5"] = hashlib.md5(data).hexdigest()
            result["sha1"] = hashlib.sha1(data).hexdigest()
            result["sha256"] = hashlib.sha256(data).hexdigest()
            result["sha512"] = hashlib.sha512(data).hexdigest()

        except Exception as e:
            result["error"] = str(e)

        return result

    def collect_kernel_extensions(self) -> dict:
        """Document loaded kernel extensions."""
        info = {"collection_time": self.collection_time.isoformat()}

        try:
            proc = subprocess.run(
                ["kextstat"], capture_output=True, text=True, timeout=30
            )
            kexts = []
            for line in proc.stdout.strip().split('\n')[1:]:  # Skip header
                parts = line.split()
                if len(parts) >= 6:
                    kexts.append({
                        "index": parts[0],
                        "refs": parts[1],
                        "address": parts[2],
                        "size": parts[3],
                        "wired": parts[4],
                        "name": parts[5],
                        "version": parts[6] if len(parts) > 6 else ""
                    })
            info["loaded_kexts"] = kexts
            info["kext_count"] = len(kexts)
        except Exception as e:
            info["error"] = str(e)

        return info

    def full_collection(self) -> dict:
        """Perform full forensic collection."""
        print("Starting full forensic collection...")

        collection = {
            "collection_id": hashlib.sha256(
                self.collection_time.isoformat().encode()
            ).hexdigest()[:16],
            "timestamp": self.collection_time.isoformat()
        }

        print("  Collecting system build info...")
        collection["system_build"] = self.collect_system_build_info()

        print("  Collecting update history...")
        collection["update_history"] = self.collect_update_history()

        print("  Collecting trust settings...")
        collection["trust_settings"] = self.collect_trust_settings()

        print("  Collecting kernel extensions...")
        collection["kernel_extensions"] = self.collect_kernel_extensions()

        # Hash critical system binaries
        print("  Hashing critical binaries...")
        critical_binaries = [
            "/usr/libexec/security_authtrampoline",
            "/usr/bin/sudo",
            "/usr/bin/login",
            "/sbin/launchd",
            "/usr/libexec/securityd"
        ]
        collection["binary_hashes"] = [
            self.hash_binary(b) for b in critical_binaries if os.path.exists(b)
        ]

        # Save full collection
        output_file = self.output_dir / f"forensic_collection_{collection['collection_id']}.json"
        with open(output_file, 'w') as f:
            json.dump(collection, f, indent=2, default=str)

        print(f"\nCollection saved to: {output_file}")
        print(f"Collection ID: {collection['collection_id']}")

        return collection


class BuildComparator:
    """Compare builds across time to detect anomalies."""

    def __init__(self, forensics_dir: str = "forensics_output"):
        self.forensics_dir = Path(forensics_dir)

    def load_collections(self) -> list:
        """Load all forensic collections."""
        collections = []
        for f in sorted(self.forensics_dir.glob("forensic_collection_*.json")):
            with open(f) as fh:
                collections.append(json.load(fh))
        return collections

    def compare_builds(self) -> dict:
        """Compare all collected builds for anomalies."""
        collections = self.load_collections()

        if len(collections) < 2:
            return {"error": "Need at least 2 collections to compare"}

        report = {
            "comparison_time": datetime.now(timezone.utc).isoformat(),
            "collections_compared": len(collections),
            "anomalies": []
        }

        # Compare consecutive collections
        for i in range(1, len(collections)):
            prev = collections[i-1]
            curr = collections[i]

            # Check for build version changes
            prev_build = prev.get("system_build", {}).get("buildversion", "")
            curr_build = curr.get("system_build", {}).get("buildversion", "")

            if prev_build != curr_build:
                report["anomalies"].append({
                    "type": "build_version_change",
                    "from_collection": prev.get("collection_id"),
                    "to_collection": curr.get("collection_id"),
                    "from_build": prev_build,
                    "to_build": curr_build
                })

            # Check for trust settings changes
            prev_hash = prev.get("trust_settings", {}).get("system_roots_hash", "")
            curr_hash = curr.get("trust_settings", {}).get("system_roots_hash", "")

            if prev_hash and curr_hash and prev_hash != curr_hash:
                report["anomalies"].append({
                    "type": "trust_roots_changed",
                    "from_collection": prev.get("collection_id"),
                    "to_collection": curr.get("collection_id")
                })

            # Check for binary hash changes
            prev_hashes = {h["path"]: h.get("sha256") for h in prev.get("binary_hashes", [])}
            curr_hashes = {h["path"]: h.get("sha256") for h in curr.get("binary_hashes", [])}

            for path, prev_sha in prev_hashes.items():
                curr_sha = curr_hashes.get(path)
                if curr_sha and prev_sha != curr_sha:
                    report["anomalies"].append({
                        "type": "binary_changed",
                        "path": path,
                        "from_collection": prev.get("collection_id"),
                        "to_collection": curr.get("collection_id"),
                        "from_sha256": prev_sha,
                        "to_sha256": curr_sha
                    })

            # Check for new kernel extensions
            prev_kexts = {k["name"] for k in prev.get("kernel_extensions", {}).get("loaded_kexts", [])}
            curr_kexts = {k["name"] for k in curr.get("kernel_extensions", {}).get("loaded_kexts", [])}

            new_kexts = curr_kexts - prev_kexts
            if new_kexts:
                report["anomalies"].append({
                    "type": "new_kernel_extensions",
                    "from_collection": prev.get("collection_id"),
                    "to_collection": curr.get("collection_id"),
                    "new_kexts": list(new_kexts)
                })

        return report


def main():
    print("Build Forensics - Code Signing & Build Verification Toolkit")
    print()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python build_forensics.py collect              - Full forensic collection")
        print("  python build_forensics.py sign <app_path>      - Analyze app signing")
        print("  python build_forensics.py compare              - Compare collections")
        print("  python build_forensics.py hash <file>          - Hash a binary")
        return

    cmd = sys.argv[1].lower()
    collector = SigningArtifactCollector()

    if cmd == "collect":
        collector.full_collection()

    elif cmd == "sign":
        if len(sys.argv) < 3:
            print("Usage: python build_forensics.py sign <app_path>")
            return
        result = collector.collect_macos_signing_info(sys.argv[2])
        print(json.dumps(result, indent=2))

    elif cmd == "compare":
        comparator = BuildComparator()
        report = comparator.compare_builds()
        print(json.dumps(report, indent=2))

        if report.get("anomalies"):
            print(f"\n⚠ Found {len(report['anomalies'])} anomalies")

    elif cmd == "hash":
        if len(sys.argv) < 3:
            print("Usage: python build_forensics.py hash <file>")
            return
        result = collector.hash_binary(sys.argv[2])
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
