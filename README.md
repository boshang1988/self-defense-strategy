# Self-Defense Strategy Toolkit

A comprehensive Python toolkit for documenting, analyzing, and generating legally-admissible evidence for cases involving targeted harassment, device tampering, or coordinated attack campaigns. All evidence is cryptographically timestamped and chain-verified for court use.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
  - [Core Commands](#core-commands)
  - [Counter-Attack Commands](#counter-attack-commands)
- [Modules](#modules)
  - [Evidence Logger](#1-evidence-logger)
  - [Build Forensics](#2-build-forensics)
  - [Legal Evidence Generator](#3-legal-evidence-generator)
  - [Acoustics Model](#4-acoustics-model)
  - [Moral Counter-Attack](#5-moral-counter-attack)
- [Output Files](#output-files)
- [Legal Considerations](#legal-considerations)
- [Workflow Examples](#workflow-examples)
- [Troubleshooting](#troubleshooting)

---

## Overview

This toolkit provides a systematic approach to documenting and responding to targeted attacks through:

1. **Cryptographic Evidence Logging** - SHA-256 hash-chained logs that prove temporal ordering and detect tampering
2. **Device State Forensics** - Capture system builds, certificates, binaries, and kernel extensions
3. **Legal Document Generation** - Court-ready attachments formatted for federal filings
4. **Attack Pattern Analysis** - Identify patterns, predict future vectors, assess campaign sophistication
5. **Counter-Strategy Framework** - Ethical, legal defensive measures and escalation paths

All strategies are designed to be **lawful**, **documented**, and **suitable for legal proceedings**.

---

## Key Features

| Feature | Description |
|---------|-------------|
| Hash-Chained Evidence | Every log entry is SHA-256 linked to the previous, creating tamper-evident records |
| Cross-Platform | Works on macOS, Linux, and Windows |
| Forensic Collections | Captures OS builds, trust settings, binary hashes, kernel extensions |
| Anomaly Detection | Compares collections over time to detect unauthorized changes |
| Legal Attachments | Generates formatted documents for court filings (Attachments 1-5) |
| Pattern Analysis | Temporal, vector, and perpetrator network analysis |
| Escalation Framework | 6-level legal escalation ladder with specific actions |
| Psychological Resilience | Gaslighting defenses and mental fortification strategies |

---

## Installation

### Requirements

- Python 3.8 or higher
- macOS, Linux, or Windows

### Setup

```bash
# Clone the repository
git clone https://github.com/boshang1988/self-defense-strategy.git
cd self-defense-strategy

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

| Package | Purpose | Required |
|---------|---------|----------|
| `numpy` | Acoustics physics calculations | Optional (fallback available) |
| `matplotlib` | Visualization | Optional |

The toolkit primarily uses Python standard library modules (hashlib, json, subprocess, pathlib, datetime, dataclasses, plistlib).

---

## Quick Start

```bash
# 1. Initialize the toolkit (creates directories, first forensic collection)
python defense_toolkit.py init

# 2. Log observations as they occur
python defense_toolkit.py log "Observed unusual network traffic at 3:15 AM"

# 3. Capture device state periodically
python defense_toolkit.py capture

# 4. Record attack incidents
python defense_toolkit.py incident HARASSMENT "Received threatening phone call"

# 5. Analyze patterns
python defense_toolkit.py patterns

# 6. Generate legal documents
python defense_toolkit.py legal

# 7. Verify evidence integrity
python defense_toolkit.py verify
```

---

## Command Reference

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize toolkit, create directories, perform first collection | `python defense_toolkit.py init` |
| `capture` | Capture current device state | `python defense_toolkit.py capture` |
| `log <message>` | Log an observation with cryptographic timestamp | `python defense_toolkit.py log "Strange clicking sounds observed"` |
| `analyze` | Run full analysis suite (build comparison, chain integrity, acoustics) | `python defense_toolkit.py analyze` |
| `legal` | Generate all legal attachments for court filing | `python defense_toolkit.py legal` |
| `verify` | Verify evidence chain integrity | `python defense_toolkit.py verify` |
| `status` | Show current toolkit status | `python defense_toolkit.py status` |

### Counter-Attack Commands

| Command | Description | Example |
|---------|-------------|---------|
| `incident <vector> <description>` | Record an attack incident | `python defense_toolkit.py incident SURVEILLANCE "Noticed phone battery draining unusually fast"` |
| `patterns` | Analyze attack patterns from recorded incidents | `python defense_toolkit.py patterns` |
| `counter` | Get counter-measure recommendations | `python defense_toolkit.py counter` |
| `strategy` | Generate full counter-strategy document | `python defense_toolkit.py strategy` |
| `escalate` | View legal escalation options | `python defense_toolkit.py escalate` |
| `resilience` | Show psychological resilience plan | `python defense_toolkit.py resilience` |

### Attack Vectors

When recording incidents, use one of these vector types:

| Vector | Description |
|--------|-------------|
| `SURVEILLANCE` | Unauthorized monitoring |
| `HARASSMENT` | Direct harassment or stalking |
| `REPUTATION` | Defamation, smear campaigns |
| `GASLIGHTING` | Reality manipulation tactics |
| `ISOLATION` | Cutting off support networks |
| `ECONOMIC` | Financial attacks, employment interference |
| `LEGAL_ABUSE` | Frivolous lawsuits, false reports |
| `TECHNOLOGICAL` | Device tampering, hacking |
| `PSYCHOLOGICAL` | Intimidation, threats |
| `INSTITUTIONAL` | Abuse through organizations/authorities |
| `PROXY_HARASSMENT` | Using third parties to attack |
| `INFORMATION_WARFARE` | Disinformation campaigns |

---

## Modules

### 1. Evidence Logger

**File:** `evidence_logger.py`

Creates tamper-evident logs using SHA-256 hash chains. Every entry is cryptographically linked to the previous, making any modification detectable.

```bash
# Standalone usage
python evidence_logger.py capture     # Capture full device state
python evidence_logger.py log <desc>  # Log an observation
python evidence_logger.py verify      # Verify chain integrity
python evidence_logger.py export      # Export for legal use
```

**Features:**
- Cryptographic hash chain (SHA-256)
- Automatic platform detection (macOS/Linux/Windows)
- Device state capture (system info, network, processes, certificates)
- Chain integrity verification
- Legal export formatting

**Evidence Chain Structure:**
```json
{
  "prev_hash": "abc123...",
  "entry_hash": "def456...",
  "timestamp": "2024-01-15T10:30:00+00:00",
  "category": "observation",
  "description": "Observed unusual behavior",
  "platform": { "system": "Darwin", "release": "23.0.0", ... }
}
```

---

### 2. Build Forensics

**File:** `build_forensics.py`

Collects code signing artifacts, build identifiers, certificate chains, and system metadata for forensic analysis.

```bash
# Standalone usage
python build_forensics.py collect           # Full forensic collection
python build_forensics.py sign <app_path>   # Analyze app signing
python build_forensics.py compare           # Compare collections over time
python build_forensics.py hash <file>       # Hash a binary
```

**Collects:**
- System build information (sw_vers, SystemVersion.plist)
- SIP status and secure boot policy
- Software update history and install receipts
- Trust settings and certificate roots
- Critical binary hashes (sudo, login, launchd, securityd)
- Loaded kernel extensions

**Anomaly Detection:**
Compares consecutive collections to detect:
- Build version changes
- Trust root modifications
- Binary hash changes
- New kernel extensions

---

### 3. Legal Evidence Generator

**File:** `legal_evidence_generator.py`

Generates properly formatted legal documentation suitable for federal court filings.

```bash
# Standalone usage
python legal_evidence_generator.py all          # Generate all attachments
python legal_evidence_generator.py declaration  # Generate declaration only
python legal_evidence_generator.py verify       # Verify evidence chain
```

**Generated Attachments:**

| Attachment | Contents |
|------------|----------|
| **Attachment 1** | Declaration under penalty of perjury |
| **Attachment 2** | Timeline + Device/Account Inventory |
| **Attachment 3** | System Update / Firmware / Build Evidence |
| **Attachment 4** | Trust / Signing Evidence |
| **Attachment 5** | Cross-Platform Consistency Indicators |
| **Verification** | Evidence chain integrity report |

---

### 4. Acoustics Model

**File:** `acoustics_model.py`

Physics-based analysis of directional audio technology feasibility. Useful for evaluating claims about directional sound transmission.

```bash
# Standalone usage
python acoustics_model.py report                    # Full feasibility report
python acoustics_model.py analyze                   # Interactive analysis
python acoustics_model.py range <freq> <power> <aperture>  # Calculate range
```

**Implements:**
- Diffraction physics (beamwidth calculations)
- Atmospheric absorption (ISO 9613-1 model)
- Geometric spreading loss (inverse square law)
- Parametric array analysis (ultrasonic conversion)

**Example Scenarios Analyzed:**
- Whisper at 10m (500Hz)
- Conversation at 50m (1kHz)
- Loud speech at 100m (2kHz)
- Voice at 500m (1kHz)

---

### 5. Moral Counter-Attack

**File:** `moral_counterattack.py`

Implements ethical, legal defensive strategies for neutralizing coordinated attacks.

```bash
# Standalone usage
python moral_counterattack.py record <vector> <desc>  # Record incident
python moral_counterattack.py analyze                  # Analyze patterns
python moral_counterattack.py recommend                # Get recommendations
python moral_counterattack.py strategy                 # Generate strategy
python moral_counterattack.py legal                    # Generate legal docs
python moral_counterattack.py resilience               # Show resilience plan
```

**Key Principles:**
1. **Truth as Weapon** - Accurate documentation defeats false narratives
2. **Transparency** - Public accountability through proper channels
3. **Legal Escalation** - Courts as the ultimate arbiter
4. **Resilience** - Psychological fortification against harassment
5. **Pattern Recognition** - Predict and preempt attack vectors

**Components:**

#### Attack Pattern Analyzer
- Temporal pattern detection (escalation, frequency trends)
- Vector analysis (identify primary attack methods)
- Coordination detection (multi-vector, proxy use, institutional abuse)
- Perpetrator network mapping
- Predictive analysis (anticipate next attack vectors)

#### Exposure Strategy
Legal channels for ethical exposure:
- Legal filings (privileged)
- Regulatory complaints (whistleblower protection)
- FOIA requests
- Legislative testimony
- Investigative journalism

#### Legal Escalation Ladder

| Level | Name | Actions |
|-------|------|---------|
| 1 | Documentation | Incident log, preserve communications, identify witnesses |
| 2 | Formal Complaint | HR complaints, regulatory bodies, platform reports |
| 3 | Law Enforcement | Police reports, FBI if interstate/federal |
| 4 | Protective Orders | Restraining orders, court protection |
| 5 | Civil Litigation | Sue for damages and injunctive relief |
| 6 | Federal Action | Federal civil rights, FBI, Congressional notification |

#### Legal Theories Supported
- Harassment
- Stalking
- Defamation
- Intentional infliction of emotional distress
- Civil conspiracy
- Civil rights violations

#### Psychological Defense
Strategies for maintaining resilience:
- Documentation therapy
- Support network fortification
- Narrative control
- Information hygiene
- Professional support
- Physical resilience
- Meaning making

**Gaslighting Defenses:**
- Reality anchors (written records, photos, recordings, witnesses)
- Cognitive defenses (recognize DARVO, identify circular logic)

---

## Output Files

After running the toolkit, these directories and files are created:

```
self-defense-strategy/
├── .defense_config.json          # Toolkit configuration
├── evidence_logs/
│   └── evidence_chain.jsonl      # Hash-chained evidence log
├── forensics_output/
│   └── forensic_collection_*.json # Device state snapshots
├── legal_output/
│   ├── attachment_1_declaration.txt
│   ├── attachment_2_timeline.txt
│   ├── attachment_3_build_evidence.txt
│   ├── attachment_4_trust_signing.txt
│   ├── attachment_5_consistency.txt
│   └── chain_verification.txt
├── counter_strategy/
│   ├── incidents.json            # Recorded attack incidents
│   └── counter_strategy_*.json   # Generated strategies
├── analysis_report.json          # Full analysis output
└── pattern_analysis.json         # Attack pattern report
```

---

## Legal Considerations

### What This Toolkit Does

- Creates **documentation only**
- Does not intercept, modify, or interfere with any systems
- Collects **metadata only** from your own devices
- Generates evidence suitable for legal proceedings

### What This Toolkit Does NOT Do

- Does not hack or access others' systems
- Does not intercept communications
- Does not install monitoring software
- Does not modify system files

### Evidence Admissibility

For evidence to be admissible in court:

1. **Chain of Custody** - The hash chain provides cryptographic proof of temporal ordering
2. **Authenticity** - Contemporaneous timestamps and platform data
3. **Integrity** - Verification system detects any tampering
4. **Relevance** - Legal attachment format designed for federal filings

### Recommended Practices

1. Run `capture` regularly (daily or after significant events)
2. Log observations immediately when they occur
3. Never modify evidence files directly
4. Export evidence before any system changes
5. Consult with an attorney before legal action

---

## Workflow Examples

### Documenting Ongoing Harassment

```bash
# Initial setup
python defense_toolkit.py init

# When incidents occur, log immediately
python defense_toolkit.py log "Received threatening message via SMS at 2:30 PM"
python defense_toolkit.py incident HARASSMENT "Third threatening call this week"

# Capture device state after suspicious activity
python defense_toolkit.py capture

# Weekly pattern analysis
python defense_toolkit.py patterns
python defense_toolkit.py counter

# When ready for legal action
python defense_toolkit.py legal
python defense_toolkit.py verify
```

### Investigating Device Tampering

```bash
# Establish baseline
python defense_toolkit.py init
python build_forensics.py collect

# After suspected tampering
python defense_toolkit.py capture
python defense_toolkit.py log "Device behaving abnormally after overnight update"

# Analyze changes
python defense_toolkit.py analyze
python build_forensics.py compare

# Generate evidence
python defense_toolkit.py legal
```

### Building a Legal Case

```bash
# Record all incidents systematically
python defense_toolkit.py incident REPUTATION "False statement posted on social media"
python defense_toolkit.py incident PROXY_HARASSMENT "Third party contacted my employer"
python defense_toolkit.py incident ECONOMIC "Job offer rescinded after background check"

# Analyze campaign sophistication
python defense_toolkit.py patterns
python defense_toolkit.py strategy

# Review escalation options
python defense_toolkit.py escalate

# Generate legal package
python defense_toolkit.py legal
```

---

## Troubleshooting

### Common Issues

**"Chain integrity: ERRORS FOUND"**
- Evidence chain has been modified
- Run `python evidence_logger.py verify` for details
- Do not modify files in `evidence_logs/` directly

**"Need at least 2 collections to compare"**
- Run `python defense_toolkit.py capture` multiple times
- Comparisons require baseline and subsequent captures

**"No incidents recorded"**
- Use `python defense_toolkit.py incident <vector> <description>` to record
- Valid vectors listed in [Attack Vectors](#attack-vectors)

**Permission denied errors**
- Some forensic commands require elevated privileges
- Run with `sudo` if needed for system-level data

**NumPy not found**
- Acoustics module will use fallback math implementation
- Install with `pip install numpy` for full functionality

### Getting Help

- Review command documentation: `python defense_toolkit.py` (no arguments)
- Check module help: `python evidence_logger.py` (no arguments)
- Report issues: https://github.com/boshang1988/self-defense-strategy/issues

---

## License

This toolkit is provided for lawful documentation and defense purposes only. Users are responsible for ensuring compliance with all applicable laws in their jurisdiction.

---

## Acknowledgments

This toolkit implements principles of:
- Cryptographic evidence integrity
- Forensic best practices
- Trauma-informed documentation
- Ethical counter-strategy frameworks
