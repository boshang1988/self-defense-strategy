#!/usr/bin/env python3
"""
Self-Defense Strategy Toolkit - Main Orchestrator

Comprehensive toolkit for documenting, analyzing, and generating
legal evidence for cases involving potential device targeting.

Components:
1. Evidence Logger - Cryptographic timestamped documentation
2. Build Forensics - Code signing and build verification
3. Acoustics Model - Physics analysis for directional audio claims
4. Legal Generator - Court-ready attachment generation
5. Moral Counter-Attack - Ethical defensive strategies

Usage:
    python defense_toolkit.py [command]

Commands:
    init          - Initialize evidence directories and first collection
    capture       - Capture full device state
    log <msg>     - Log an observation
    analyze       - Run full analysis suite
    legal         - Generate all legal attachments
    verify        - Verify all evidence integrity
    status        - Show current status

Counter-Attack Commands:
    incident <vector> <desc>  - Record an attack incident
    patterns                  - Analyze attack patterns
    counter                   - Get counter-measure recommendations
    strategy                  - Generate full counter-strategy
    escalate                  - View legal escalation options
    resilience                - Show psychological resilience plan
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Import toolkit components
from evidence_logger import EvidenceLogger, capture_full_state
from build_forensics import SigningArtifactCollector, BuildComparator
from legal_evidence_generator import LegalDocumentGenerator
from acoustics_model import FeasibilityAnalyzer
from moral_counterattack import (
    CounterStrategyOrchestrator,
    AttackVector,
    AttackPatternAnalyzer
)


class DefenseToolkit:
    """Main orchestrator for self-defense documentation toolkit."""

    def __init__(self):
        self.base_dir = Path(".")
        self.evidence_dir = self.base_dir / "evidence_logs"
        self.forensics_dir = self.base_dir / "forensics_output"
        self.legal_dir = self.base_dir / "legal_output"
        self.config_file = self.base_dir / ".defense_config.json"

        self.logger = EvidenceLogger(str(self.evidence_dir))
        self.collector = SigningArtifactCollector(str(self.forensics_dir))
        self.legal_gen = LegalDocumentGenerator(
            str(self.evidence_dir),
            str(self.forensics_dir)
        )

    def init(self):
        """Initialize the toolkit and perform first collection."""
        print("Initializing Self-Defense Toolkit")
        print("=" * 50)

        # Create directories
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.forensics_dir.mkdir(parents=True, exist_ok=True)
        self.legal_dir.mkdir(parents=True, exist_ok=True)

        # Save config
        config = {
            "initialized": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0"
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print("✓ Directories created")

        # Log initialization
        self.logger.log_entry(
            category="system",
            description="Defense toolkit initialized"
        )
        print("✓ Evidence chain started")

        # First forensic collection
        print("\nPerforming initial forensic collection...")
        self.collector.full_collection()
        print("✓ Initial collection complete")

        # Log the collection
        self.logger.log_entry(
            category="forensic_collection",
            description="Initial device state captured"
        )

        print("\n" + "=" * 50)
        print("Initialization complete!")
        print("\nNext steps:")
        print("  1. Run 'python defense_toolkit.py capture' regularly")
        print("  2. Run 'python defense_toolkit.py log <observation>' for anomalies")
        print("  3. Run 'python defense_toolkit.py legal' to generate attachments")

    def capture(self):
        """Capture current device state."""
        print("Capturing device state...")

        # Run forensic collection
        collection = self.collector.full_collection()

        # Log it
        self.logger.log_entry(
            category="forensic_collection",
            description="Device state capture",
            data={"collection_id": collection.get("collection_id")}
        )

        print("\nCapture complete!")

    def log_observation(self, message: str):
        """Log an observation with timestamp."""
        entry = self.logger.log_entry(
            category="observation",
            description=message
        )
        print(f"Logged with hash: {entry['entry_hash'][:16]}...")

    def analyze(self):
        """Run full analysis suite."""
        print("Running Analysis Suite")
        print("=" * 50)

        # Compare forensic collections
        print("\n1. Build Comparison Analysis")
        print("-" * 30)
        comparator = BuildComparator(str(self.forensics_dir))
        comparison = comparator.compare_builds()

        if "error" in comparison:
            print(f"  {comparison['error']}")
        else:
            anomalies = comparison.get("anomalies", [])
            print(f"  Collections compared: {comparison.get('collections_compared', 0)}")
            print(f"  Anomalies found: {len(anomalies)}")

            if anomalies:
                print("\n  Anomalies:")
                for a in anomalies:
                    print(f"    - {a.get('type')}: {json.dumps(a, indent=6)[:200]}...")

        # Verify evidence chain
        print("\n2. Evidence Chain Integrity")
        print("-" * 30)
        is_valid, errors = self.logger.verify_chain()
        print(f"  Chain integrity: {'VALID' if is_valid else 'ERRORS FOUND'}")
        if errors:
            for e in errors:
                print(f"    - {e}")

        # Acoustics feasibility (for reference)
        print("\n3. Acoustics Feasibility Reference")
        print("-" * 30)
        analyzer = FeasibilityAnalyzer()
        report = analyzer.generate_comprehensive_report()

        feasible_count = sum(1 for s in report["scenarios"] if s.get("feasible"))
        print(f"  Scenarios analyzed: {len(report['scenarios'])}")
        print(f"  Physically feasible: {feasible_count}/{len(report['scenarios'])}")

        # Save full analysis
        analysis_file = self.base_dir / "analysis_report.json"
        full_report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "build_comparison": comparison,
            "chain_valid": is_valid,
            "chain_errors": errors,
            "acoustics_reference": report
        }
        with open(analysis_file, 'w') as f:
            json.dump(full_report, f, indent=2)

        print(f"\nFull report saved to: {analysis_file}")

    def generate_legal(self):
        """Generate all legal attachments."""
        print("Generating Legal Attachments")
        print("=" * 50)

        results = self.legal_gen.generate_all_attachments()

        print("\nGenerated files:")
        for name, path in results.items():
            print(f"  {name}: {path}")

        # Log the generation
        self.logger.log_entry(
            category="legal_generation",
            description="Legal attachments generated",
            data={"files": list(results.values())}
        )

    def verify(self):
        """Verify all evidence integrity."""
        print("Verifying Evidence Integrity")
        print("=" * 50)

        # Verify evidence chain
        print("\n1. Evidence Chain")
        is_valid, errors = self.logger.verify_chain()
        print(f"   Status: {'✓ VALID' if is_valid else '✗ ERRORS FOUND'}")
        if errors:
            for e in errors:
                print(f"   - {e}")

        # Check forensic collections
        print("\n2. Forensic Collections")
        collections = list(self.forensics_dir.glob("forensic_collection_*.json"))
        print(f"   Collections found: {len(collections)}")

        for c in collections:
            try:
                with open(c) as f:
                    data = json.load(f)
                    print(f"   ✓ {c.name} - ID: {data.get('collection_id', 'N/A')}")
            except Exception as e:
                print(f"   ✗ {c.name} - Error: {e}")

        # Export verification
        export_path = self.logger.export_for_legal("verification_export.json")
        print(f"\n3. Verification export saved to: {export_path}")

    def status(self):
        """Show current toolkit status."""
        print("Defense Toolkit Status")
        print("=" * 50)

        # Config status
        if self.config_file.exists():
            with open(self.config_file) as f:
                config = json.load(f)
            print(f"\nInitialized: {config.get('initialized', 'Unknown')}")
        else:
            print("\n⚠ Toolkit not initialized. Run 'python defense_toolkit.py init'")
            return

        # Evidence chain
        chain_file = self.evidence_dir / "evidence_chain.jsonl"
        if chain_file.exists():
            with open(chain_file) as f:
                entries = sum(1 for line in f if line.strip())
            print(f"Evidence entries: {entries}")
        else:
            print("Evidence entries: 0")

        # Forensic collections
        collections = list(self.forensics_dir.glob("forensic_collection_*.json"))
        print(f"Forensic collections: {len(collections)}")

        # Legal documents
        legal_docs = list(self.legal_dir.glob("attachment_*.txt"))
        print(f"Legal attachments: {len(legal_docs)}")

        # Last activity
        if chain_file.exists():
            with open(chain_file) as f:
                last_line = None
                for line in f:
                    if line.strip():
                        last_line = line
                if last_line:
                    entry = json.loads(last_line)
                    print(f"\nLast activity: {entry.get('timestamp', 'Unknown')}")
                    print(f"  Category: {entry.get('category')}")
                    print(f"  Description: {entry.get('description', '')[:50]}...")


def main():
    toolkit = DefenseToolkit()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()

    if cmd == "init":
        toolkit.init()
    elif cmd == "capture":
        toolkit.capture()
    elif cmd == "log":
        if len(sys.argv) < 3:
            print("Usage: python defense_toolkit.py log <message>")
            return
        message = " ".join(sys.argv[2:])
        toolkit.log_observation(message)
    elif cmd == "analyze":
        toolkit.analyze()
    elif cmd == "legal":
        toolkit.generate_legal()
    elif cmd == "verify":
        toolkit.verify()
    elif cmd == "status":
        toolkit.status()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
