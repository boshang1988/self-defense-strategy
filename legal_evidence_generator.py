#!/usr/bin/env python3
"""
Legal Evidence Generator

Generates properly formatted legal documentation from collected evidence.
Outputs attachments suitable for federal court filings based on
forensic collections and evidence logs.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import sys


class LegalDocumentGenerator:
    """Generate legal attachments from forensic evidence."""

    def __init__(self, evidence_dir: str = "evidence_logs",
                 forensics_dir: str = "forensics_output"):
        self.evidence_dir = Path(evidence_dir)
        self.forensics_dir = Path(forensics_dir)
        self.output_dir = Path("legal_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_evidence_chain(self) -> list:
        """Load the cryptographic evidence chain."""
        chain_file = self.evidence_dir / "evidence_chain.jsonl"
        entries = []

        if chain_file.exists():
            with open(chain_file) as f:
                for line in f:
                    if line.strip():
                        entries.append(json.loads(line))

        return entries

    def load_forensic_collections(self) -> list:
        """Load all forensic collections."""
        collections = []
        for f in sorted(self.forensics_dir.glob("forensic_collection_*.json")):
            with open(f) as fh:
                collections.append(json.load(fh))
        return collections

    def generate_timeline_attachment(self) -> str:
        """
        Generate Attachment 2: Timeline + Device/Account Inventory

        Format suitable for federal court filing.
        """
        evidence = self.load_evidence_chain()
        collections = self.load_forensic_collections()

        doc = []
        doc.append("ATTACHMENT 2 — TIMELINE + DEVICE/ACCOUNT INVENTORY")
        doc.append("=" * 60)
        doc.append("")
        doc.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        doc.append(f"Evidence entries: {len(evidence)}")
        doc.append(f"Forensic collections: {len(collections)}")
        doc.append("")

        # Device Inventory
        doc.append("SECTION A: DEVICE INVENTORY")
        doc.append("-" * 40)
        doc.append("")

        if collections:
            latest = collections[-1]
            sys_info = latest.get("system_build", {})

            doc.append("Primary Device:")
            doc.append(f"  Platform: {sys_info.get('platform', 'N/A')}")
            doc.append(f"  Product Name: {sys_info.get('productname', 'N/A')}")
            doc.append(f"  Product Version: {sys_info.get('productversion', 'N/A')}")
            doc.append(f"  Build Version: {sys_info.get('buildversion', 'N/A')}")
            doc.append("")

        # Timeline
        doc.append("SECTION B: CHRONOLOGICAL TIMELINE")
        doc.append("-" * 40)
        doc.append("")

        if evidence:
            for entry in evidence:
                timestamp = entry.get("timestamp", "Unknown")
                category = entry.get("category", "unknown")
                description = entry.get("description", "")
                entry_hash = entry.get("entry_hash", "")[:16]

                doc.append(f"[{timestamp}]")
                doc.append(f"  Category: {category}")
                doc.append(f"  Description: {description}")
                doc.append(f"  Evidence Hash: {entry_hash}...")
                doc.append("")

        # Write output
        output_file = self.output_dir / "attachment_2_timeline.txt"
        content = "\n".join(doc)
        with open(output_file, 'w') as f:
            f.write(content)

        return str(output_file)

    def generate_build_evidence_attachment(self) -> str:
        """
        Generate Attachment 3: System Update / Firmware / Build Evidence
        """
        collections = self.load_forensic_collections()

        doc = []
        doc.append("ATTACHMENT 3 — SYSTEM UPDATE / FIRMWARE / BUILD EVIDENCE")
        doc.append("=" * 60)
        doc.append("")
        doc.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        doc.append("")

        for i, collection in enumerate(collections):
            doc.append(f"COLLECTION {i+1}: {collection.get('collection_id', 'N/A')}")
            doc.append(f"Timestamp: {collection.get('timestamp', 'N/A')}")
            doc.append("-" * 40)

            sys_build = collection.get("system_build", {})
            doc.append("")
            doc.append("System Build Information:")
            doc.append(f"  Product Name: {sys_build.get('productname', 'N/A')}")
            doc.append(f"  Product Version: {sys_build.get('productversion', 'N/A')}")
            doc.append(f"  Build Version: {sys_build.get('buildversion', 'N/A')}")
            doc.append(f"  SIP Status: {sys_build.get('sip_status', 'N/A')}")

            # System version plist details
            plist = sys_build.get("system_version_plist", {})
            if plist:
                doc.append("")
                doc.append("  SystemVersion.plist Details:")
                for key, val in plist.items():
                    doc.append(f"    {key}: {val}")

            # Update history
            update_history = collection.get("update_history", {})
            if update_history.get("update_history"):
                doc.append("")
                doc.append("Software Update History:")
                for line in update_history["update_history"].split('\n')[:20]:
                    doc.append(f"  {line}")

            # Binary hashes
            binary_hashes = collection.get("binary_hashes", [])
            if binary_hashes:
                doc.append("")
                doc.append("Critical Binary Hashes:")
                for bh in binary_hashes:
                    doc.append(f"  {bh.get('path', 'N/A')}")
                    doc.append(f"    SHA-256: {bh.get('sha256', 'N/A')}")
                    doc.append(f"    Size: {bh.get('size_bytes', 'N/A')} bytes")

            doc.append("")
            doc.append("")

        output_file = self.output_dir / "attachment_3_build_evidence.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(doc))

        return str(output_file)

    def generate_trust_signing_attachment(self) -> str:
        """
        Generate Attachment 4: Trust / Signing Evidence
        """
        collections = self.load_forensic_collections()

        doc = []
        doc.append("ATTACHMENT 4 — TRUST / SIGNING EVIDENCE")
        doc.append("=" * 60)
        doc.append("")
        doc.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        doc.append("")
        doc.append("This attachment documents certificate chain metadata, trust")
        doc.append("settings, and signing verification indicators collected from")
        doc.append("the Plaintiff's devices.")
        doc.append("")

        for i, collection in enumerate(collections):
            doc.append(f"COLLECTION {i+1}: {collection.get('collection_id', 'N/A')}")
            doc.append("-" * 40)

            trust = collection.get("trust_settings", {})

            doc.append("")
            doc.append("System Root Certificates:")
            doc.append(f"  Certificate Count: {trust.get('system_root_cert_count', 'N/A')}")
            doc.append(f"  Collective Hash: {trust.get('system_roots_hash', 'N/A')}")

            if trust.get("user_trust_settings"):
                doc.append("")
                doc.append("User Trust Settings Modifications:")
                settings = trust["user_trust_settings"][:500]  # Limit length
                for line in settings.split('\n'):
                    doc.append(f"  {line}")

            if trust.get("admin_trust_settings"):
                doc.append("")
                doc.append("Admin Trust Settings:")
                settings = trust["admin_trust_settings"][:500]
                for line in settings.split('\n'):
                    doc.append(f"  {line}")

            # Kernel extensions (trust-related)
            kexts = collection.get("kernel_extensions", {})
            if kexts.get("loaded_kexts"):
                doc.append("")
                doc.append(f"Loaded Kernel Extensions: {kexts.get('kext_count', 0)}")
                # List non-Apple kexts
                non_apple = [k for k in kexts["loaded_kexts"]
                            if not k.get("name", "").startswith("com.apple")]
                if non_apple:
                    doc.append("Non-Apple Kernel Extensions:")
                    for k in non_apple:
                        doc.append(f"    {k.get('name', 'N/A')} ({k.get('version', '')})")

            doc.append("")
            doc.append("")

        output_file = self.output_dir / "attachment_4_trust_signing.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(doc))

        return str(output_file)

    def generate_consistency_attachment(self) -> str:
        """
        Generate Attachment 5: Cross-Platform Consistency Indicators
        """
        collections = self.load_forensic_collections()

        doc = []
        doc.append("ATTACHMENT 5 — CROSS-PLATFORM CONSISTENCY INDICATORS")
        doc.append("=" * 60)
        doc.append("")
        doc.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        doc.append("")

        if len(collections) < 2:
            doc.append("Insufficient collections for consistency analysis.")
            doc.append("Minimum 2 forensic collections required.")
        else:
            doc.append("CHANGE DETECTION ANALYSIS")
            doc.append("-" * 40)
            doc.append("")

            for i in range(1, len(collections)):
                prev = collections[i-1]
                curr = collections[i]

                doc.append(f"Comparison: Collection {i} → Collection {i+1}")
                doc.append(f"  Period: {prev.get('timestamp', 'N/A')} to {curr.get('timestamp', 'N/A')}")
                doc.append("")

                # Build version changes
                prev_build = prev.get("system_build", {}).get("buildversion", "")
                curr_build = curr.get("system_build", {}).get("buildversion", "")

                if prev_build != curr_build:
                    doc.append(f"  ⚠ BUILD VERSION CHANGED")
                    doc.append(f"    From: {prev_build}")
                    doc.append(f"    To: {curr_build}")
                    doc.append("")

                # Trust settings changes
                prev_hash = prev.get("trust_settings", {}).get("system_roots_hash", "")
                curr_hash = curr.get("trust_settings", {}).get("system_roots_hash", "")

                if prev_hash and curr_hash and prev_hash != curr_hash:
                    doc.append(f"  ⚠ SYSTEM ROOT CERTIFICATES CHANGED")
                    doc.append(f"    Previous hash: {prev_hash[:32]}...")
                    doc.append(f"    Current hash: {curr_hash[:32]}...")
                    doc.append("")

                # Binary changes
                prev_hashes = {h["path"]: h.get("sha256") for h in prev.get("binary_hashes", [])}
                curr_hashes = {h["path"]: h.get("sha256") for h in curr.get("binary_hashes", [])}

                for path, prev_sha in prev_hashes.items():
                    curr_sha = curr_hashes.get(path)
                    if curr_sha and prev_sha != curr_sha:
                        doc.append(f"  ⚠ BINARY CHANGED: {path}")
                        doc.append(f"    Previous SHA-256: {prev_sha[:32]}...")
                        doc.append(f"    Current SHA-256: {curr_sha[:32]}...")
                        doc.append("")

                # New kernel extensions
                prev_kexts = {k["name"] for k in prev.get("kernel_extensions", {}).get("loaded_kexts", [])}
                curr_kexts = {k["name"] for k in curr.get("kernel_extensions", {}).get("loaded_kexts", [])}

                new_kexts = curr_kexts - prev_kexts
                if new_kexts:
                    doc.append(f"  ⚠ NEW KERNEL EXTENSIONS LOADED")
                    for k in new_kexts:
                        doc.append(f"    - {k}")
                    doc.append("")

                doc.append("")

        output_file = self.output_dir / "attachment_5_consistency.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(doc))

        return str(output_file)

    def generate_declaration(self, plaintiff_name: str = "[PLAINTIFF NAME]") -> str:
        """
        Generate Attachment 1: Declaration template
        """
        evidence = self.load_evidence_chain()
        collections = self.load_forensic_collections()

        doc = []
        doc.append("ATTACHMENT 1 — DECLARATION OF " + plaintiff_name.upper())
        doc.append("=" * 60)
        doc.append("")
        doc.append("I, " + plaintiff_name + ", declare under penalty of perjury")
        doc.append("that the following is true and correct:")
        doc.append("")
        doc.append("1. I am the Plaintiff in this matter and make this declaration")
        doc.append("   based on my personal knowledge.")
        doc.append("")
        doc.append("2. I have collected forensic evidence from my devices using")
        doc.append("   cryptographically-verified logging tools. The evidence chain")
        doc.append(f"   contains {len(evidence)} entries with SHA-256 hash verification.")
        doc.append("")
        doc.append(f"3. I have performed {len(collections)} forensic collections")
        doc.append("   documenting system builds, trust settings, and binary hashes.")
        doc.append("")

        if collections:
            latest = collections[-1]
            sys_info = latest.get("system_build", {})
            doc.append("4. My primary device is configured as follows:")
            doc.append(f"   - Platform: {sys_info.get('productname', 'N/A')}")
            doc.append(f"   - OS Version: {sys_info.get('productversion', 'N/A')}")
            doc.append(f"   - Build: {sys_info.get('buildversion', 'N/A')}")
            doc.append("")

        doc.append("5. The attached evidence documents [describe specific anomalies")
        doc.append("   observed, with reference to specific entries by hash].")
        doc.append("")
        doc.append("6. I declare under penalty of perjury under the laws of the")
        doc.append("   United States of America that the foregoing is true and correct.")
        doc.append("")
        doc.append("")
        doc.append("Executed on: [DATE]")
        doc.append("")
        doc.append("")
        doc.append("_______________________________")
        doc.append(plaintiff_name)
        doc.append("")

        output_file = self.output_dir / "attachment_1_declaration.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(doc))

        return str(output_file)

    def generate_chain_verification(self) -> str:
        """Generate verification report for evidence chain integrity."""
        chain_file = self.evidence_dir / "evidence_chain.jsonl"

        doc = []
        doc.append("EVIDENCE CHAIN VERIFICATION REPORT")
        doc.append("=" * 60)
        doc.append("")
        doc.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
        doc.append("")

        if not chain_file.exists():
            doc.append("No evidence chain found.")
        else:
            errors = []
            prev_hash = hashlib.sha256(b"GENESIS").hexdigest()
            entry_count = 0

            with open(chain_file) as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue

                    entry_count += 1
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError as e:
                        errors.append(f"Line {line_num}: Invalid JSON")
                        continue

                    if entry.get("prev_hash") != prev_hash:
                        errors.append(f"Line {line_num}: Chain break detected")

                    prev_hash = entry.get("entry_hash", prev_hash)

            doc.append(f"Total entries: {entry_count}")
            doc.append(f"Chain integrity: {'VALID' if not errors else 'ERRORS FOUND'}")
            doc.append("")

            if errors:
                doc.append("Errors detected:")
                for e in errors:
                    doc.append(f"  - {e}")
            else:
                doc.append("All hash links verified successfully.")
                doc.append("Evidence chain has not been tampered with.")

        output_file = self.output_dir / "chain_verification.txt"
        with open(output_file, 'w') as f:
            f.write("\n".join(doc))

        return str(output_file)

    def generate_all_attachments(self) -> dict:
        """Generate all legal attachments."""
        print("Generating legal attachments...")

        results = {}

        print("  Generating Declaration (Attachment 1)...")
        results["attachment_1"] = self.generate_declaration()

        print("  Generating Timeline (Attachment 2)...")
        results["attachment_2"] = self.generate_timeline_attachment()

        print("  Generating Build Evidence (Attachment 3)...")
        results["attachment_3"] = self.generate_build_evidence_attachment()

        print("  Generating Trust/Signing Evidence (Attachment 4)...")
        results["attachment_4"] = self.generate_trust_signing_attachment()

        print("  Generating Consistency Indicators (Attachment 5)...")
        results["attachment_5"] = self.generate_consistency_attachment()

        print("  Generating Chain Verification...")
        results["verification"] = self.generate_chain_verification()

        print(f"\nAll attachments saved to: {self.output_dir}/")
        return results


def main():
    print("Legal Evidence Generator")
    print("=" * 40)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python legal_evidence_generator.py all          - Generate all attachments")
        print("  python legal_evidence_generator.py declaration  - Generate declaration only")
        print("  python legal_evidence_generator.py verify       - Verify evidence chain")
        return

    cmd = sys.argv[1].lower()
    generator = LegalDocumentGenerator()

    if cmd == "all":
        results = generator.generate_all_attachments()
        print("\nGenerated files:")
        for name, path in results.items():
            print(f"  {name}: {path}")

    elif cmd == "declaration":
        path = generator.generate_declaration()
        print(f"Declaration saved to: {path}")

    elif cmd == "verify":
        path = generator.generate_chain_verification()
        print(f"Verification report: {path}")

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
