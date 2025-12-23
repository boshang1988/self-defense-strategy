#!/usr/bin/env python3
"""
Moral Counter-Strategy Framework

Legitimate defensive strategies for individuals facing asymmetric pressure
from more powerful actors. Based on historical examples of successful
resistance to coercion.

Principles:
1. Truth as weapon - lies require maintenance, truth does not
2. Documentation creates accountability
3. Transparency neutralizes secret operations
4. Witnesses prevent revisionism
5. Calm under pressure denies the adversary satisfaction
6. Time favors the truthful
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional
import hashlib


@dataclass
class StrategicPrinciple:
    """A defensive strategic principle."""
    name: str
    description: str
    implementation: str
    historical_example: str


# Core defensive principles derived from successful resistance to coercion
DEFENSIVE_PRINCIPLES = [
    StrategicPrinciple(
        name="Radical Transparency",
        description="Make everything public before they can control the narrative",
        implementation="Document and publish contemporaneously. What is public cannot be secretly manipulated.",
        historical_example="Zelensky's refusal to have private conversation - insisted on public record"
    ),
    StrategicPrinciple(
        name="Witness Multiplication",
        description="Ensure multiple independent observers for all interactions",
        implementation="Never engage in private. Always have witnesses, recordings, documentation.",
        historical_example="Diplomats always bring note-takers; court requires witnesses"
    ),
    StrategicPrinciple(
        name="Temporal Anchoring",
        description="Create immutable timestamps that prove sequence of events",
        implementation="Hash-chain documentation, blockchain timestamps, notarized records",
        historical_example="Cryptographic proof of when documents existed"
    ),
    StrategicPrinciple(
        name="Emotional Discipline",
        description="Deny adversary the reaction they seek",
        implementation="Respond with facts, not emotion. Aggression seeks emotional response - deny it.",
        historical_example="Zelensky maintaining composure under public attack"
    ),
    StrategicPrinciple(
        name="Narrative Control",
        description="Define the frame before adversary can",
        implementation="State your position clearly, repeatedly, publicly, first",
        historical_example="Getting your version of events on record before manipulation"
    ),
    StrategicPrinciple(
        name="Coalition Asymmetry",
        description="Build broader coalition than adversary expects",
        implementation="Document supporters, find others with similar experiences, create network",
        historical_example="International support coalitions against powerful aggressors"
    ),
    StrategicPrinciple(
        name="Legal Anchoring",
        description="Force engagement through legal/institutional channels",
        implementation="File in courts, use FOIA, create official records that require response",
        historical_example="Court filings create permanent record and force discovery"
    ),
    StrategicPrinciple(
        name="Truth Persistence",
        description="Lies require energy to maintain; truth persists automatically",
        implementation="State truth once, clearly, with evidence. Let adversary exhaust themselves.",
        historical_example="Consistent story vs. changing narratives"
    ),
    StrategicPrinciple(
        name="Moral High Ground",
        description="Never descend to adversary's level",
        implementation="Respond to aggression with documented facts. Never retaliate immorally.",
        historical_example="Gandhi, MLK - moral authority through non-retaliation"
    ),
    StrategicPrinciple(
        name="Asymmetric Publicity",
        description="Use adversary's power against them via Streisand Effect",
        implementation="Attempts to silence you amplify your message if documented",
        historical_example="Suppression attempts becoming the story"
    )
]


class CounterStrategyFramework:
    """Framework for implementing moral counter-strategies."""

    def __init__(self, output_dir: str = "strategy_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.strategy_log = self.output_dir / "strategy_log.jsonl"

    def get_principles(self) -> List[StrategicPrinciple]:
        """Get all defensive principles."""
        return DEFENSIVE_PRINCIPLES

    def log_action(self, principle: str, action: str,
                   evidence: Optional[dict] = None) -> dict:
        """Log a strategic action taken."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "principle": principle,
            "action": action,
            "evidence": evidence or {},
            "hash": ""
        }
        entry["hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()[:32]

        with open(self.strategy_log, 'a') as f:
            f.write(json.dumps(entry) + "\n")

        return entry

    def generate_response_template(self, situation: str) -> dict:
        """Generate a strategic response template for a situation."""
        template = {
            "situation": situation,
            "generated": datetime.now(timezone.utc).isoformat(),
            "immediate_actions": [
                "1. DOCUMENT: Record exact time, location, participants, words spoken",
                "2. WITNESS: Identify all witnesses, get contact information",
                "3. PRESERVE: Screenshot, photograph, save all related materials",
                "4. TIMESTAMP: Create hash-chained record immediately"
            ],
            "short_term_actions": [
                "1. NARRATIVE: Write clear factual account while memory fresh",
                "2. EVIDENCE: Gather all supporting documentation",
                "3. LEGAL: Consult attorney, consider filing if warranted",
                "4. SUPPORT: Identify allies and inform them"
            ],
            "long_term_actions": [
                "1. PERSIST: Maintain consistent truthful account",
                "2. PUBLISH: Make record public when strategically appropriate",
                "3. COALITION: Build network of supporters",
                "4. LEGAL: Pursue all legitimate legal remedies"
            ],
            "do_not": [
                "- Do NOT respond emotionally (deny them satisfaction)",
                "- Do NOT engage in private (always have witnesses)",
                "- Do NOT retaliate immorally (maintain moral authority)",
                "- Do NOT stay silent (silence enables revisionism)",
                "- Do NOT trust verbal assurances (document everything)"
            ]
        }

        return template

    def analyze_power_asymmetry(self, your_resources: List[str],
                                adversary_resources: List[str]) -> dict:
        """Analyze power asymmetry and identify leverage points."""
        # Defensive advantages available to the weaker party
        defensive_advantages = [
            "Truth (no maintenance cost)",
            "Moral authority (if maintained)",
            "Public sympathy (underdog effect)",
            "Legal system (equalizer by design)",
            "Documentation (permanent record)",
            "Time (lies degrade, truth persists)",
            "Coalition potential (others with similar experiences)",
            "Streisand effect (suppression amplifies)"
        ]

        analysis = {
            "your_stated_resources": your_resources,
            "adversary_stated_resources": adversary_resources,
            "inherent_defensive_advantages": defensive_advantages,
            "recommended_strategy": "asymmetric_defense",
            "key_insight": (
                "Do not attempt symmetric competition where adversary is stronger. "
                "Use defensive advantages: truth, documentation, legal system, publicity, time."
            )
        }

        return analysis


class PsychologicalResilience:
    """Tools for maintaining psychological stability under pressure."""

    @staticmethod
    def reality_check_protocol() -> dict:
        """Protocol for distinguishing real from imagined threats."""
        return {
            "name": "Reality Verification Protocol",
            "purpose": "Maintain accurate threat assessment under pressure",
            "steps": [
                {
                    "step": 1,
                    "action": "Document observation objectively",
                    "question": "What exactly did I observe? (facts only, no interpretation)"
                },
                {
                    "step": 2,
                    "action": "Seek independent verification",
                    "question": "Can anyone else confirm this observation?"
                },
                {
                    "step": 3,
                    "action": "Consider alternative explanations",
                    "question": "What are 3 mundane explanations for this observation?"
                },
                {
                    "step": 4,
                    "action": "Assess physical evidence",
                    "question": "What physical/digital evidence exists?"
                },
                {
                    "step": 5,
                    "action": "Evaluate pattern",
                    "question": "Is this part of a documented pattern or isolated?"
                },
                {
                    "step": 6,
                    "action": "Rate confidence",
                    "question": "On 1-10, how confident am I this is real? Why?"
                }
            ],
            "note": (
                "High-stress situations can affect perception. "
                "This protocol helps maintain accurate assessment. "
                "Document even uncertain observations - pattern analysis requires data."
            )
        }

    @staticmethod
    def stress_response_protocol() -> dict:
        """Protocol for managing acute stress response."""
        return {
            "name": "Acute Stress Management",
            "purpose": "Maintain cognitive function under pressure",
            "immediate_physiological": [
                "1. Slow breathing: 4 counts in, 4 hold, 4 out (activates parasympathetic)",
                "2. Ground physically: feet on floor, hands on solid surface",
                "3. Cold water on wrists (physiological reset)",
                "4. Name 5 things you see, 4 you hear, 3 you feel (grounding)"
            ],
            "cognitive_reset": [
                "1. Ask: What is the ACTUAL threat right now? (not future, now)",
                "2. Ask: What is the single most important action?",
                "3. Write one sentence describing situation (forces clarity)",
                "4. Identify one person to contact"
            ],
            "strategic_principle": (
                "Adversary WANTS emotional response. Calm denies them this. "
                "Every second of maintained composure is a victory. "
                "Document, don't react."
            )
        }

    @staticmethod
    def long_term_resilience() -> dict:
        """Long-term psychological resilience strategies."""
        return {
            "name": "Sustained Resilience Protocol",
            "components": {
                "routine": (
                    "Maintain normal routines. Disruption is adversary goal. "
                    "Routine maintenance is resistance."
                ),
                "support_network": (
                    "Identify 3-5 trusted people. Brief them on situation. "
                    "Regular check-ins. Isolation enables adversary."
                ),
                "documentation_habit": (
                    "Daily log regardless of events. Pattern emerges from data. "
                    "Also provides evidence of normal periods."
                ),
                "physical_health": (
                    "Sleep, exercise, nutrition affect cognitive function. "
                    "Physical health is strategic asset."
                ),
                "legal_preparation": (
                    "Having legal strategy reduces anxiety. "
                    "Knowing your rights provides psychological stability."
                ),
                "perspective": (
                    "This is temporary. Document for future self and courts. "
                    "Truth and time favor the honest."
                )
            }
        }


class CommunicationStrategy:
    """Templates for strategic communication."""

    @staticmethod
    def public_statement_template() -> str:
        """Template for public statements."""
        return """
PUBLIC STATEMENT TEMPLATE
=========================

Date: [DATE]
Re: [SUBJECT]

FACTS (what happened):
- [Specific fact 1 with date/time]
- [Specific fact 2 with date/time]
- [Specific fact 3 with date/time]

EVIDENCE (what proves it):
- [Document/recording 1]
- [Document/recording 2]
- [Witness 1]

WHAT I AM ASKING FOR:
- [Specific request 1]
- [Specific request 2]

WHAT I WILL DO:
- [Specific action 1]
- [Specific action 2]

I am prepared to testify to the above under oath.

[SIGNATURE]
[CONTACT]

---
Note: Keep factual. Remove emotion. Specific dates/times.
Offer to testify under oath (shows confidence in truth).
"""

    @staticmethod
    def legal_filing_principles() -> dict:
        """Principles for legal filings."""
        return {
            "format": [
                "Clear factual allegations",
                "Specific dates and times",
                "Identify specific actors where known",
                "Reference specific evidence",
                "Request specific relief"
            ],
            "tone": [
                "Professional, not emotional",
                "Factual, not accusatory beyond facts",
                "Specific, not vague",
                "Cite legal standards that apply"
            ],
            "strategy": [
                "Early filing creates official record",
                "Discovery forces disclosure",
                "Court filings are public record (usually)",
                "Judge is neutral arbiter"
            ]
        }


def print_principles():
    """Print all defensive principles."""
    print("MORAL COUNTER-STRATEGY PRINCIPLES")
    print("=" * 60)
    print()

    for i, p in enumerate(DEFENSIVE_PRINCIPLES, 1):
        print(f"{i}. {p.name}")
        print(f"   {p.description}")
        print(f"   Implementation: {p.implementation}")
        print(f"   Example: {p.historical_example}")
        print()


def main():
    import sys

    print("Moral Counter-Strategy Framework")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python counter_strategies.py principles  - Show all principles")
        print("  python counter_strategies.py template    - Generate response template")
        print("  python counter_strategies.py reality     - Reality check protocol")
        print("  python counter_strategies.py stress      - Stress response protocol")
        print("  python counter_strategies.py resilience  - Long-term resilience")
        print("  python counter_strategies.py statement   - Public statement template")
        return

    cmd = sys.argv[1].lower()
    framework = CounterStrategyFramework()
    resilience = PsychologicalResilience()
    comms = CommunicationStrategy()

    if cmd == "principles":
        print_principles()

    elif cmd == "template":
        template = framework.generate_response_template(
            "General adversarial situation"
        )
        print(json.dumps(template, indent=2))

    elif cmd == "reality":
        protocol = resilience.reality_check_protocol()
        print(json.dumps(protocol, indent=2))

    elif cmd == "stress":
        protocol = resilience.stress_response_protocol()
        print(json.dumps(protocol, indent=2))

    elif cmd == "resilience":
        protocol = resilience.long_term_resilience()
        print(json.dumps(protocol, indent=2))

    elif cmd == "statement":
        print(comms.public_statement_template())

    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
