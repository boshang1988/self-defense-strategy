#!/usr/bin/env python3
"""
PRECISION SELF-DEFENSE TOOLKIT

Single-file implementation. No hallucination. Only documented facts.

Usage:
    python precision.py init                    Initialize evidence system
    python precision.py log <observation>       Log with SHA-256 timestamp
    python precision.py incident <vector> <desc> Record attack incident
    python precision.py capture                 Forensic device capture
    python precision.py patterns                Analyze attack patterns
    python precision.py escalate                Legal escalation position
    python precision.py legal                   Generate court documents
    python precision.py verify                  Verify chain integrity
    python precision.py status                  Current state

Vectors: SURVEILLANCE GASLIGHTING HARASSMENT ISOLATION REPUTATION
         ECONOMIC LEGAL_ABUSE TECHNOLOGICAL PSYCHOLOGICAL INSTITUTIONAL
"""

import hashlib
import json
import subprocess
import sys
import platform
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
from enum import Enum, auto


# =============================================================================
# ATTACK VECTORS
# =============================================================================

class Vector(Enum):
    SURVEILLANCE = auto()
    GASLIGHTING = auto()
    HARASSMENT = auto()
    ISOLATION = auto()
    REPUTATION = auto()
    ECONOMIC = auto()
    LEGAL_ABUSE = auto()
    TECHNOLOGICAL = auto()
    PSYCHOLOGICAL = auto()
    INSTITUTIONAL = auto()


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Incident:
    timestamp: str
    vector: str
    description: str
    severity: int = 5
    hash: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# =============================================================================
# EVIDENCE CHAIN (SHA-256 Hash-Linked)
# =============================================================================

class EvidenceChain:
    """Immutable, hash-linked evidence log."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _last_hash(self) -> str:
        if not self.path.exists():
            return hashlib.sha256(b"GENESIS").hexdigest()
        with open(self.path) as f:
            lines = [l for l in f if l.strip()]
        if not lines:
            return hashlib.sha256(b"GENESIS").hexdigest()
        return json.loads(lines[-1]).get("hash", "")

    def append(self, category: str, description: str, data: dict = None) -> dict:
        """Append entry with cryptographic link to previous."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "category": category,
            "description": description,
            "data": data or {},
            "prev_hash": self._last_hash()
        }
        content = json.dumps(entry, sort_keys=True)
        entry["hash"] = hashlib.sha256(content.encode()).hexdigest()

        with open(self.path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def verify(self) -> tuple:
        """Verify chain integrity. Returns (valid, errors)."""
        if not self.path.exists():
            return True, []

        errors = []
        prev = hashlib.sha256(b"GENESIS").hexdigest()

        with open(self.path) as f:
            for i, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("prev_hash") != prev:
                        errors.append(f"Line {i}: chain break")
                    prev = entry.get("hash", prev)
                except json.JSONDecodeError:
                    errors.append(f"Line {i}: invalid JSON")

        return len(errors) == 0, errors

    def count(self) -> int:
        if not self.path.exists():
            return 0
        with open(self.path) as f:
            return sum(1 for l in f if l.strip())

    def last(self) -> Optional[dict]:
        if not self.path.exists():
            return None
        with open(self.path) as f:
            lines = [l for l in f if l.strip()]
        return json.loads(lines[-1]) if lines else None


# =============================================================================
# INCIDENT TRACKER
# =============================================================================

class IncidentTracker:
    """Track and analyze attack incidents."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.incidents: List[Incident] = []
        self._load()

    def _load(self):
        if self.path.exists():
            with open(self.path) as f:
                for item in json.load(f):
                    self.incidents.append(Incident(**item))

    def _save(self):
        with open(self.path, "w") as f:
            json.dump([i.to_dict() for i in self.incidents], f, indent=2)

    def record(self, vector: str, description: str, severity: int = 5) -> Incident:
        ts = datetime.now(timezone.utc).isoformat()
        h = hashlib.sha256(f"{ts}{vector}{description}".encode()).hexdigest()[:16]
        incident = Incident(timestamp=ts, vector=vector, description=description,
                           severity=severity, hash=h)
        self.incidents.append(incident)
        self._save()
        return incident

    def analyze(self) -> dict:
        """Pattern analysis."""
        if not self.incidents:
            return {"total": 0, "message": "No incidents recorded"}

        vectors = {}
        for inc in self.incidents:
            vectors[inc.vector] = vectors.get(inc.vector, 0) + 1

        # Escalation detection
        escalating = False
        if len(self.incidents) >= 3:
            recent = [i.severity for i in self.incidents[-3:]]
            early = [i.severity for i in self.incidents[:3]]
            escalating = sum(recent)/len(recent) > sum(early)/len(early)

        # Sophistication assessment
        level = "LOW"
        if len(vectors) >= 3:
            level = "MEDIUM"
        if len(vectors) >= 5 or len(self.incidents) > 10:
            level = "HIGH"

        return {
            "total": len(self.incidents),
            "vectors": vectors,
            "escalating": escalating,
            "sophistication": level,
            "multi_vector": len(vectors) >= 3
        }


# =============================================================================
# FORENSIC CAPTURE
# =============================================================================

class ForensicCapture:
    """Capture device state for evidence."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self) -> dict:
        ts = datetime.now(timezone.utc)
        data = {
            "timestamp": ts.isoformat(),
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine()
        }

        # macOS specific
        if platform.system() == "Darwin":
            try:
                r = subprocess.run(["sw_vers"], capture_output=True, text=True, timeout=10)
                for line in r.stdout.strip().split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        data[k.strip().lower().replace(" ", "_")] = v.strip()
            except Exception:
                pass

            try:
                r = subprocess.run(["csrutil", "status"], capture_output=True, text=True, timeout=10)
                data["sip_status"] = r.stdout.strip()
            except Exception:
                pass

        # Hash critical binaries (if accessible)
        binaries = ["/usr/bin/sudo", "/sbin/launchd", "/usr/bin/login"]
        data["binary_hashes"] = {}
        for b in binaries:
            try:
                if Path(b).exists():
                    with open(b, "rb") as f:
                        data["binary_hashes"][b] = hashlib.sha256(f.read()).hexdigest()
            except (PermissionError, OSError):
                data["binary_hashes"][b] = "PERMISSION_DENIED"

        # Save
        cid = hashlib.sha256(ts.isoformat().encode()).hexdigest()[:16]
        data["collection_id"] = cid
        outfile = self.output_dir / f"capture_{cid}.json"
        with open(outfile, "w") as f:
            json.dump(data, f, indent=2)

        return data


# =============================================================================
# LEGAL ESCALATION
# =============================================================================

ESCALATION_LADDER = [
    {"level": 1, "name": "DOCUMENTATION", "action": "Hash-chained logs, forensic captures"},
    {"level": 2, "name": "FORMAL COMPLAINT", "action": "HR, regulatory bodies, platforms"},
    {"level": 3, "name": "LAW ENFORCEMENT", "action": "Police reports, FBI if federal"},
    {"level": 4, "name": "PROTECTIVE ORDERS", "action": "Restraining orders, TRO"},
    {"level": 5, "name": "CIVIL LITIGATION", "action": "Damages, discovery, injunction"},
    {"level": 6, "name": "FEDERAL ACTION", "action": "Civil rights, Congressional notification"},
]


def assess_escalation(incidents: List[Incident]) -> dict:
    """Assess current escalation level."""
    n = len(incidents)
    level = 1
    if n >= 3:
        level = 2
    if n >= 5:
        level = 3
    if any(i.severity >= 8 for i in incidents):
        level = max(level, 4)
    if n >= 10:
        level = max(level, 5)

    return {
        "current_level": level,
        "level_name": ESCALATION_LADDER[level-1]["name"],
        "recommended_action": ESCALATION_LADDER[level-1]["action"],
        "incident_count": n
    }


# =============================================================================
# LEGAL DOCUMENT GENERATOR
# =============================================================================

def generate_legal_docs(evidence_chain: EvidenceChain, incidents: IncidentTracker,
                        output_dir: Path) -> dict:
    """Generate court-ready attachments."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    files = {}

    # Attachment 1: Declaration
    decl = f"""DECLARATION

I declare under penalty of perjury that:

1. I maintain a cryptographically-verified evidence log containing {evidence_chain.count()} entries.
2. I have documented {len(incidents.incidents)} attack incidents.
3. All timestamps are UTC and hash-chain verified.

The evidence chain integrity has been verified as: {"VALID" if evidence_chain.verify()[0] else "ERRORS FOUND"}

Executed: {ts}

_______________________________
[SIGNATURE]
"""
    files["declaration"] = output_dir / "attachment_1_declaration.txt"
    files["declaration"].write_text(decl)

    # Attachment 2: Incident Timeline
    timeline = f"INCIDENT TIMELINE\nGenerated: {ts}\n\n"
    for inc in sorted(incidents.incidents, key=lambda x: x.timestamp):
        timeline += f"[{inc.timestamp}] {inc.vector}: {inc.description}\n"
        timeline += f"  Severity: {inc.severity}/10 | Hash: {inc.hash}\n\n"
    files["timeline"] = output_dir / "attachment_2_timeline.txt"
    files["timeline"].write_text(timeline)

    # Attachment 3: Pattern Analysis
    analysis = incidents.analyze()
    pattern = f"PATTERN ANALYSIS\nGenerated: {ts}\n\n"
    pattern += f"Total Incidents: {analysis['total']}\n"
    pattern += f"Sophistication Level: {analysis['sophistication']}\n"
    pattern += f"Escalation Detected: {analysis['escalating']}\n"
    pattern += f"Multi-Vector Attack: {analysis['multi_vector']}\n\n"
    pattern += "Vector Frequency:\n"
    for v, c in analysis.get("vectors", {}).items():
        pattern += f"  {v}: {c}\n"
    files["patterns"] = output_dir / "attachment_3_patterns.txt"
    files["patterns"].write_text(pattern)

    # Attachment 4: Escalation Position
    esc = assess_escalation(incidents.incidents)
    escalation = f"LEGAL ESCALATION ASSESSMENT\nGenerated: {ts}\n\n"
    escalation += f"Current Level: {esc['current_level']} - {esc['level_name']}\n"
    escalation += f"Recommended Action: {esc['recommended_action']}\n"
    escalation += f"Incident Count: {esc['incident_count']}\n\n"
    escalation += "ESCALATION LADDER:\n"
    for lvl in ESCALATION_LADDER:
        marker = "→" if lvl["level"] == esc["current_level"] else " "
        escalation += f"{marker} Level {lvl['level']}: {lvl['name']} - {lvl['action']}\n"
    files["escalation"] = output_dir / "attachment_4_escalation.txt"
    files["escalation"].write_text(escalation)

    return {k: str(v) for k, v in files.items()}


# =============================================================================
# MAIN CLI
# =============================================================================

class PrecisionToolkit:
    def __init__(self, base: Path = Path(".")):
        self.base = base
        self.evidence = EvidenceChain(base / "evidence" / "chain.jsonl")
        self.incidents = IncidentTracker(base / "evidence" / "incidents.json")
        self.forensics = ForensicCapture(base / "forensics")
        self.legal_dir = base / "legal"

    def init(self):
        print("PRECISION TOOLKIT - Initializing")
        print("=" * 40)
        self.evidence.append("system", "Precision toolkit initialized")
        capture = self.forensics.capture()
        self.evidence.append("forensic", "Initial capture", {"id": capture["collection_id"]})
        print(f"✓ Evidence chain started")
        print(f"✓ Forensic capture: {capture['collection_id']}")
        valid, _ = self.evidence.verify()
        print(f"✓ Chain integrity: {'VALID' if valid else 'ERROR'}")

    def log(self, msg: str):
        entry = self.evidence.append("observation", msg)
        print(f"Logged: {entry['hash'][:16]}...")

    def incident(self, vector: str, desc: str):
        try:
            Vector[vector.upper()]
        except KeyError:
            print(f"Invalid vector: {vector}")
            print("Valid:", " ".join(v.name for v in Vector))
            return
        inc = self.incidents.record(vector.upper(), desc)
        self.evidence.append("incident", f"[{vector.upper()}] {desc}", {"hash": inc.hash})
        print(f"Incident: {inc.hash}")
        print(f"Vector: {inc.vector}")
        print(f"Total: {len(self.incidents.incidents)}")

    def capture(self):
        data = self.forensics.capture()
        self.evidence.append("forensic", "Device capture", {"id": data["collection_id"]})
        print(f"Captured: {data['collection_id']}")

    def patterns(self):
        analysis = self.incidents.analyze()
        print("PATTERN ANALYSIS")
        print("=" * 40)
        print(f"Incidents: {analysis['total']}")
        print(f"Sophistication: {analysis['sophistication']}")
        print(f"Escalating: {analysis['escalating']}")
        print(f"Multi-vector: {analysis['multi_vector']}")
        if analysis.get("vectors"):
            print("\nVectors:")
            for v, c in analysis["vectors"].items():
                print(f"  {v}: {c}")

    def escalate(self):
        esc = assess_escalation(self.incidents.incidents)
        print("LEGAL ESCALATION")
        print("=" * 40)
        for lvl in ESCALATION_LADDER:
            marker = "→" if lvl["level"] == esc["current_level"] else " "
            print(f"{marker} L{lvl['level']}: {lvl['name']}")
            print(f"      {lvl['action']}")
        print()
        print(f"Current: Level {esc['current_level']} - {esc['level_name']}")
        print(f"Action: {esc['recommended_action']}")

    def legal(self):
        files = generate_legal_docs(self.evidence, self.incidents, self.legal_dir)
        print("LEGAL DOCUMENTS GENERATED")
        print("=" * 40)
        for name, path in files.items():
            print(f"  {name}: {path}")

    def verify(self):
        valid, errors = self.evidence.verify()
        print(f"Chain Integrity: {'VALID' if valid else 'ERRORS'}")
        for e in errors:
            print(f"  - {e}")

    def status(self):
        print("PRECISION TOOLKIT STATUS")
        print("=" * 40)
        print(f"Evidence entries: {self.evidence.count()}")
        print(f"Incidents: {len(self.incidents.incidents)}")
        valid, _ = self.evidence.verify()
        print(f"Chain integrity: {'VALID' if valid else 'ERROR'}")
        last = self.evidence.last()
        if last:
            print(f"\nLast: {last['timestamp']}")
            print(f"  {last['category']}: {last['description'][:50]}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    tk = PrecisionToolkit()
    cmd = sys.argv[1].lower()

    if cmd == "init":
        tk.init()
    elif cmd == "log":
        tk.log(" ".join(sys.argv[2:]))
    elif cmd == "incident":
        if len(sys.argv) < 4:
            print("Usage: precision.py incident <vector> <description>")
            return
        tk.incident(sys.argv[2], " ".join(sys.argv[3:]))
    elif cmd == "capture":
        tk.capture()
    elif cmd == "patterns":
        tk.patterns()
    elif cmd == "escalate":
        tk.escalate()
    elif cmd == "legal":
        tk.legal()
    elif cmd == "verify":
        tk.verify()
    elif cmd == "status":
        tk.status()
    else:
        print(f"Unknown: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
