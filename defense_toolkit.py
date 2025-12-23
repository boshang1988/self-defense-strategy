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
        self.counter_strategy = CounterStrategyOrchestrator(
            self.base_dir / "counter_strategy"
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

    # ============================================================
    # MORAL COUNTER-ATTACK METHODS
    # ============================================================

    def record_incident(self, vector_str: str, description: str):
        """Record an attack incident for pattern analysis."""
        # Load existing incidents
        self.counter_strategy.load_incidents()

        try:
            vector = AttackVector[vector_str.upper()]
        except KeyError:
            print(f"Unknown attack vector: {vector_str}")
            print("\nValid vectors:")
            for v in AttackVector:
                print(f"  - {v.name}")
            return

        incident_id = self.counter_strategy.record_incident(
            vector=vector,
            description=description
        )

        # Also log to main evidence chain
        self.logger.log_entry(
            category="attack_incident",
            description=f"[{vector.name}] {description}",
            data={"incident_id": incident_id, "vector": vector.name}
        )

        print(f"Incident recorded: {incident_id}")
        print(f"Vector: {vector.name}")
        print(f"Description: {description}")
        print(f"\nTotal incidents recorded: {len(self.counter_strategy.incidents)}")

    def analyze_patterns(self):
        """Analyze attack patterns from recorded incidents."""
        print("Attack Pattern Analysis")
        print("=" * 50)

        self.counter_strategy.load_incidents()

        if not self.counter_strategy.incidents:
            print("\nNo incidents recorded yet.")
            print("Use 'incident <vector> <description>' to record incidents.")
            return

        report = self.counter_strategy.pattern_analyzer.generate_pattern_report()

        print(f"\nTotal incidents: {report['total_incidents']}")

        # Temporal patterns
        temporal = report.get("temporal_patterns", {})
        if temporal.get("escalation_detected"):
            print("\n⚠ ESCALATION DETECTED - Severity increasing over time")

        # Vector analysis
        vector_patterns = report.get("vector_patterns", {})
        print("\nAttack Vectors Used:")
        for vector, count in vector_patterns.get("vector_frequency", {}).items():
            print(f"  - {vector}: {count} incident(s)")

        if vector_patterns.get("multi_vector_attack"):
            print("\n⚠ MULTI-VECTOR ATTACK - Coordinated campaign likely")

        # Campaign sophistication
        campaign = report.get("campaign_assessment", {})
        print(f"\nCampaign Assessment: {campaign.get('level', 'Unknown')}")
        for factor in campaign.get("contributing_factors", []):
            print(f"  - {factor}")

        # Predictions
        predictions = report.get("predictions", [])
        if predictions:
            print("\nPredicted Next Attack Vectors:")
            for pred in predictions:
                print(f"  - {pred['vector']} (confidence: {pred['confidence']*100:.0f}%)")
                print(f"    Preparation: {pred['recommended_preparation']}")

        # Save report
        report_path = self.base_dir / "pattern_analysis.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nFull report saved to: {report_path}")

    def recommend_countermeasures(self):
        """Get counter-measure recommendations."""
        print("Counter-Measure Recommendations")
        print("=" * 50)

        self.counter_strategy.load_incidents()

        if not self.counter_strategy.incidents:
            print("\nNo incidents recorded. Record incidents first.")
            return

        measures = self.counter_strategy.recommend_counter_measures()

        print(f"\nBased on {len(self.counter_strategy.incidents)} recorded incidents:\n")

        for idx, measure in enumerate(measures, 1):
            print(f"{idx}. [{measure.measure_type.name}]")
            print(f"   {measure.description}")
            print(f"   Target: {measure.target_vector.name}")
            if measure.legal_basis:
                print(f"   Legal basis: {measure.legal_basis}")
            if measure.resources_needed:
                print(f"   Resources: {', '.join(measure.resources_needed)}")
            print()

    def generate_counter_strategy(self):
        """Generate full counter-strategy document."""
        print("Generating Full Counter-Strategy")
        print("=" * 50)

        self.counter_strategy.load_incidents()

        if not self.counter_strategy.incidents:
            print("\nNo incidents recorded. Record incidents first.")
            return

        strategy = self.counter_strategy.generate_full_counter_strategy()

        print(f"\nStrategy generated for {len(self.counter_strategy.incidents)} incidents")

        # Summary
        assessment = strategy.get("situation_assessment", {})
        campaign = assessment.get("campaign_sophistication", {})
        print(f"\nCampaign Level: {campaign.get('level', 'Unknown')}")

        # Immediate actions
        print("\nImmediate Actions:")
        for action in strategy.get("immediate_actions", []):
            print(f"  • {action}")

        # Legal position
        legal = strategy.get("legal_position", {})
        print(f"\nLegal Escalation Level: {legal.get('current_level', 1)} - {legal.get('level_name', 'Documentation')}")

        # Exposure readiness
        exposure = strategy.get("exposure_readiness", {})
        ready_channels = [ch for ch, info in exposure.items() if info.get("ready")]
        if ready_channels:
            print(f"\nReady for exposure via: {', '.join(ready_channels)}")

        print(f"\nFull strategy saved to: counter_strategy/")

    def show_escalation_options(self):
        """Show legal escalation ladder and recommendations."""
        print("Legal Escalation Framework")
        print("=" * 50)

        self.counter_strategy.load_incidents()

        # Show the ladder
        print("\nEscalation Ladder:")
        for level in self.counter_strategy.legal_escalation.ESCALATION_LADDER:
            marker = "→" if level["level"] == self.counter_strategy.legal_escalation.current_level else " "
            print(f"\n{marker} Level {level['level']}: {level['name']}")
            print(f"   {level['description']}")
            print("   Actions:")
            for action in level["actions"]:
                print(f"     - {action}")

        # Show current position
        if self.counter_strategy.incidents:
            position = self.counter_strategy.legal_escalation.assess_current_position(
                self.counter_strategy.incidents
            )
            print(f"\n{'=' * 50}")
            print(f"Current Position: Level {position['current_level']} - {position['level_name']}")

            # Applicable theories
            if position.get("applicable_legal_theories"):
                print("\nApplicable Legal Theories:")
                for theory in position["applicable_legal_theories"]:
                    print(f"  - {theory['theory'].upper()}")

            # Recommendation
            rec = self.counter_strategy.legal_escalation.recommend_escalation(
                self.counter_strategy.incidents, "documented"
            )
            if rec["escalate"]:
                print("\n⚠ ESCALATION RECOMMENDED:")
                for reason in rec["reasoning"]:
                    print(f"  - {reason}")

    def show_resilience_plan(self):
        """Show psychological resilience strategies."""
        print("Psychological Resilience Plan")
        print("=" * 50)

        plan = self.counter_strategy.psych_defense.generate_resilience_plan()

        # Strategies
        print("\nResilience Strategies:")
        for name, info in plan["strategies"].items():
            print(f"\n• {name.replace('_', ' ').title()}")
            print(f"  {info['description']}")
            print(f"  Mechanism: {info['mechanism']}")

        # Gaslighting defenses
        print("\n" + "=" * 50)
        print("Anti-Gaslighting Defenses")
        print("\nReality Anchors:")
        for anchor in plan["gaslighting_defenses"]["reality_anchors"]:
            print(f"  • {anchor}")

        print("\nCognitive Defenses:")
        for defense in plan["gaslighting_defenses"]["cognitive_defenses"]:
            print(f"  • {defense}")

        # Implementation checklist
        print("\n" + "=" * 50)
        print("Implementation Checklist:")
        for item in plan["implementation_checklist"]:
            status = "[ ]" if item["status"] == "pending" else "[x]"
            print(f"  {status} {item['task']}")


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
    # Counter-attack commands
    elif cmd == "incident":
        if len(sys.argv) < 4:
            print("Usage: python defense_toolkit.py incident <vector> <description>")
            print("\nAvailable vectors:")
            for v in AttackVector:
                print(f"  - {v.name}")
            return
        vector = sys.argv[2]
        description = " ".join(sys.argv[3:])
        toolkit.record_incident(vector, description)
    elif cmd == "patterns":
        toolkit.analyze_patterns()
    elif cmd == "counter":
        toolkit.recommend_countermeasures()
    elif cmd == "strategy":
        toolkit.generate_counter_strategy()
    elif cmd == "escalate":
        toolkit.show_escalation_options()
    elif cmd == "resilience":
        toolkit.show_resilience_plan()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
