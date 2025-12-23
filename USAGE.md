# Self-Defense Strategy Toolkit - Usage Guide

## Overview

This toolkit provides cryptographically-verified evidence documentation for cases involving potential device targeting. It creates tamper-evident logs and court-ready attachments.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize the toolkit (creates directories, first collection)
python defense_toolkit.py init

# Take regular device state captures
python defense_toolkit.py capture

# Log observations/anomalies
python defense_toolkit.py log "Observed unusual behavior at 3:15 PM"

# Generate legal attachments
python defense_toolkit.py legal

# Verify evidence integrity
python defense_toolkit.py verify
```

## Components

### 1. Evidence Logger (`evidence_logger.py`)

Creates cryptographically-chained logs with SHA-256 verification.

```bash
# Capture device state with timestamp
python evidence_logger.py capture

# Log an observation
python evidence_logger.py log "Description of what was observed"

# Verify chain integrity
python evidence_logger.py verify

# Export for legal use
python evidence_logger.py export
```

**Key Features:**
- Hash-chained entries (tamper-evident)
- UTC timestamps
- Attachment hashing
- Legal export format

### 2. Build Forensics (`build_forensics.py`)

Collects code signing artifacts and build verification data.

```bash
# Full forensic collection
python build_forensics.py collect

# Analyze specific app's signing
python build_forensics.py sign /Applications/Safari.app

# Compare collections for changes
python build_forensics.py compare

# Hash a specific binary
python build_forensics.py hash /usr/bin/sudo
```

**Collects:**
- System build versions
- Code signing certificates
- Trust anchor settings
- Kernel extensions
- Software update history
- Critical binary hashes

### 3. Network Monitor (`network_monitor.py`)

Documents network state and connections.

```bash
# Take network snapshot
python network_monitor.py snapshot

# Create baseline of normal state
python network_monitor.py baseline

# Compare current state to baseline
python network_monitor.py compare

# Log connections over time
python network_monitor.py log 300  # 5 minutes

# Analyze logged connections
python network_monitor.py analyze
```

### 4. Acoustics Model (`acoustics_model.py`)

Physics simulation for directional audio feasibility analysis.

```bash
# Generate feasibility report
python acoustics_model.py report

# Interactive analysis
python acoustics_model.py analyze

# Calculate effective range
python acoustics_model.py range 1000 100 0.5  # freq power aperture
```

### 5. Legal Evidence Generator (`legal_evidence_generator.py`)

Generates court-ready attachments from collected evidence.

```bash
# Generate all attachments
python legal_evidence_generator.py all

# Generate declaration only
python legal_evidence_generator.py declaration

# Verify evidence chain
python legal_evidence_generator.py verify
```

**Generates:**
- Attachment 1: Declaration template
- Attachment 2: Timeline + Device Inventory
- Attachment 3: Build/Firmware Evidence
- Attachment 4: Trust/Signing Evidence
- Attachment 5: Consistency Indicators

## Recommended Workflow

### Daily
```bash
python defense_toolkit.py capture
```

### When observing anomalies
```bash
python defense_toolkit.py log "Detailed description of anomaly"
python network_monitor.py snapshot
```

### Weekly
```bash
python defense_toolkit.py analyze
python network_monitor.py compare
```

### Before legal filing
```bash
python defense_toolkit.py verify
python defense_toolkit.py legal
```

## Evidence Chain Format

Each evidence entry contains:

```json
{
  "prev_hash": "sha256 of previous entry",
  "entry_hash": "sha256 of this entry + prev_hash",
  "timestamp": "2024-01-15T10:30:00Z",
  "category": "observation|device_state|forensic_collection",
  "description": "Human readable description",
  "data": {},
  "platform": {}
}
```

## Directory Structure

```
self-defense-strategy/
├── evidence_logs/           # Cryptographic evidence chain
│   ├── evidence_chain.jsonl
│   └── verification_export.json
├── forensics_output/        # Forensic collections
│   └── forensic_collection_*.json
├── network_logs/            # Network monitoring data
│   ├── connections.jsonl
│   ├── baseline.json
│   └── snapshot_*.json
├── legal_output/            # Court-ready attachments
│   ├── attachment_1_declaration.txt
│   ├── attachment_2_timeline.txt
│   ├── attachment_3_build_evidence.txt
│   ├── attachment_4_trust_signing.txt
│   └── attachment_5_consistency.txt
└── analysis_report.json     # Analysis results
```

## Integrity Verification

The evidence chain uses SHA-256 hash chaining. Each entry's hash includes the previous entry's hash, creating a tamper-evident chain similar to blockchain.

To verify:
```bash
python evidence_logger.py verify
```

If any entry is modified, the chain will break at that point.

## Legal Notes

1. This toolkit creates **documentation only**
2. It does not intercept, modify, or interfere with any systems
3. All collection uses standard system APIs and commands
4. Evidence is timestamped in UTC for legal clarity
5. Hash chains provide cryptographic proof of temporal ordering

## Technical Requirements

- Python 3.8+
- macOS (primary), Linux (partial support)
- numpy (for acoustics calculations)
- No elevated privileges required for most functions
