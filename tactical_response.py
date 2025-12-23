#!/usr/bin/env python3
"""
Tactical Response Generator

Generates specific tactical responses to adversarial situations
using moral counter-strategy principles.

Key insight: When facing a more powerful adversary, symmetric
competition loses. Asymmetric defense leverages truth, documentation,
legal systems, and publicity - domains where power differential
is neutralized or reversed.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict
import hashlib


class TacticalResponse:
    """Generate tactical responses for specific situations."""

    def __init__(self):
        self.output_dir = Path("tactical_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def respond_to_public_attack(self) -> Dict:
        """
        Response template for public attack/humiliation attempt.

        Like Feb 28 2025 Oval Office - when adversary uses public
        setting to pressure/humiliate.
        """
        return {
            "scenario": "Public Attack / Humiliation Attempt",
            "adversary_goal": "Force emotional reaction, establish dominance, create exploitable moment",
            "your_goal": "Maintain composure, document everything, preserve moral authority",

            "immediate_response": {
                "do": [
                    "Breathe slowly (4-4-4 pattern) - physiological calm",
                    "Maintain neutral expression - deny satisfaction",
                    "Respond only to facts, not provocations",
                    "State your position once, clearly",
                    "Request official record/transcript",
                    "Note all witnesses present"
                ],
                "say": [
                    "'I want to ensure this is on the record.'",
                    "'Let me state the facts clearly...'",
                    "'I disagree with that characterization. The facts are...'",
                    "'I'm happy to discuss this with witnesses/counsel present.'",
                ],
                "do_not": [
                    "Raise voice (matches their energy = they win)",
                    "Make threats (gives them ammunition)",
                    "Walk out (unless safety requires - can be spun as weakness)",
                    "Agree to anything under pressure",
                    "Engage in private side conversation"
                ]
            },

            "within_1_hour": [
                "Write detailed contemporaneous notes while memory fresh",
                "Identify all witnesses, get contact info if possible",
                "Secure any recordings/evidence",
                "Contact attorney if warranted",
                "Do NOT post on social media yet (strategic timing matters)"
            ],

            "within_24_hours": [
                "Create hash-timestamped written account",
                "Consult with attorney on legal options",
                "Brief trusted supporters",
                "Prepare factual public statement if needed",
                "Assess: Is this part of pattern? Document connection."
            ],

            "strategic_principle": (
                "Public attacks are designed to provoke response that can be used against you. "
                "The MORE aggressive the attack, the MORE calm you should be. "
                "Composure is victory. Documentation is revenge. Courts are equalizers."
            )
        }

    def respond_to_gaslighting(self) -> Dict:
        """Response to reality-denial/gaslighting attempts."""
        return {
            "scenario": "Gaslighting / Reality Denial",
            "adversary_goal": "Make you doubt your perception, appear unreliable to others",
            "your_goal": "Anchor to documented facts, maintain clear record",

            "defense_mechanism": {
                "document_immediately": (
                    "The moment something happens, document it with timestamp. "
                    "Do not wait. Memory degrades, documents persist."
                ),
                "multiple_formats": (
                    "Written notes, screenshots, photographs, audio if legal. "
                    "Multiple formats make denial harder."
                ),
                "independent_witnesses": (
                    "Tell trusted others contemporaneously. "
                    "Their memory corroborates yours."
                ),
                "hash_chain": (
                    "Use the evidence_logger to create cryptographic proof of "
                    "when you documented something. Cannot be backdated."
                )
            },

            "when_they_say_it_didnt_happen": [
                "Refer to your documentation: 'I documented this at [TIME] on [DATE]'",
                "Reference witnesses: '[PERSON] was present and can confirm'",
                "Remain calm: Anger makes you look unstable (their goal)",
                "State facts once, clearly, then stop arguing",
                "Let your documentation speak in formal proceedings"
            ],

            "psychological_anchor": (
                "You are not crazy. Gaslighting is a known manipulation technique. "
                "Your documentation exists. Your witnesses exist. "
                "Their denial does not change documented reality."
            )
        }

    def respond_to_surveillance(self) -> Dict:
        """Response to suspected surveillance/monitoring."""
        return {
            "scenario": "Suspected Surveillance / Device Compromise",
            "adversary_goal": "Information gathering, intimidation, control",
            "your_goal": "Document evidence, legal channels, operational security",

            "documentation_priority": [
                "Use forensic tools to capture device state (build_forensics.py)",
                "Document anomalies with timestamps",
                "Create network baselines and monitor for changes",
                "Preserve evidence before it can be wiped"
            ],

            "legal_channels": [
                "File FOIA requests with relevant agencies",
                "Consult attorney about legal discovery options",
                "File complaint in court (creates official record)",
                "Request specific 'fact of use' admissions"
            ],

            "operational_security": [
                "Assume monitored devices may report what you type/say",
                "Use separate clean devices for sensitive communications",
                "Have sensitive conversations in person, outdoors",
                "Use end-to-end encrypted messaging on clean devices",
                "Air-gapped devices for critical documentation"
            ],

            "psychological_aspect": (
                "The PURPOSE of surveillance may be as much intimidation as intelligence. "
                "Don't let awareness of surveillance paralyze you. "
                "Continue documenting, continue legal action. "
                "Awareness is power - now you know to document and adapt."
            ),

            "key_insight": (
                "If surveillance is real and illegal, documentation + legal filing is your weapon. "
                "If surveillance is imagined, documentation helps you reality-test. "
                "Either way: document, legal channels, maintain function."
            )
        }

    def respond_to_isolation_attempt(self) -> Dict:
        """Response to attempts to isolate you from support."""
        return {
            "scenario": "Isolation Attempt",
            "adversary_goal": "Cut you off from support, make you easier to manipulate",
            "your_goal": "Maintain and expand support network",

            "counter_tactics": [
                "Proactively reach out to supporters before adversary can poison relationships",
                "Document your version of events to share with supporters",
                "Find others in similar situations (you're rarely the only one)",
                "Use public forums where isolation is harder",
                "Legal filings are public record - harder to isolate from"
            ],

            "build_coalition": [
                "Civil liberties organizations (ACLU, EFF, etc.)",
                "Journalists who cover relevant topics",
                "Others who have experienced similar targeting",
                "Legal community (attorneys may take interest)",
                "Academic researchers studying relevant phenomena"
            ],

            "communication_strategy": [
                "Clear, factual, documented communication",
                "Avoid sounding paranoid (stick to facts and evidence)",
                "Lead with evidence, not claims",
                "Be the calm, reasonable one in every interaction"
            ]
        }

    def generate_action_plan(self, situation_type: str) -> Dict:
        """Generate complete action plan for a situation type."""
        responses = {
            "public_attack": self.respond_to_public_attack,
            "gaslighting": self.respond_to_gaslighting,
            "surveillance": self.respond_to_surveillance,
            "isolation": self.respond_to_isolation_attempt
        }

        if situation_type not in responses:
            return {"error": f"Unknown situation type. Options: {list(responses.keys())}"}

        response = responses[situation_type]()

        # Add common elements
        response["universal_principles"] = {
            "document_everything": "Every interaction, every anomaly, with timestamps",
            "never_private": "Always have witnesses or records",
            "stay_calm": "Emotional reactions help adversary, hurt you",
            "legal_channels": "Courts and FOIA are equalizers",
            "truth_persists": "Lies require maintenance, truth stands alone",
            "time_favors_truth": "Short term may be hard, long term favors the honest"
        }

        response["daily_habits"] = [
            "Morning: Review and document any overnight anomalies",
            "Throughout day: Note any significant events with timestamps",
            "Evening: Daily log entry even if 'nothing happened'",
            "Weekly: Run forensic collection, verify evidence chain",
            "Monthly: Review patterns, update legal strategy"
        ]

        # Save the plan
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"action_plan_{situation_type}_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=2)

        return response

    def zelensky_analysis(self) -> Dict:
        """
        Analysis of the Feb 28 2025 Oval Office confrontation.
        What worked, what can be learned.
        """
        return {
            "event": "Feb 28 2025 Oval Office Meeting",
            "situation": "Invited to meeting that became public confrontation/pressure attempt",

            "what_zelensky_did_right": [
                "Maintained composure under public attack",
                "Did not agree to unfavorable terms under pressure",
                "Stated his position clearly",
                "Did not match aggression with aggression",
                "Let the world witness the behavior",
                "Did not engage in private side deals"
            ],

            "strategic_lessons": {
                "public_witness": (
                    "The public nature meant millions witnessed the pressure tactics. "
                    "This built sympathy and coalition support."
                ),
                "composure_as_weapon": (
                    "By staying calm while being attacked, Zelensky appeared reasonable "
                    "while adversary appeared aggressive. Contrast helps."
                ),
                "refusing_private": (
                    "Insisting on public record prevented manipulation of what was said."
                ),
                "not_capitulating": (
                    "Did not agree to terms under pressure. Walked away instead."
                ),
                "subsequent_action": (
                    "Used the incident to strengthen coalition support internationally."
                )
            },

            "applicable_principles": [
                "Radical Transparency - keep everything public",
                "Emotional Discipline - deny them the reaction",
                "Witness Multiplication - everyone was watching",
                "Narrative Control - his composure told the story",
                "Coalition Asymmetry - incident strengthened international support",
                "Moral High Ground - never descended to aggression"
            ],

            "key_insight": (
                "When facing a more powerful adversary in public, "
                "YOUR COMPOSURE IS YOUR WEAPON. "
                "Their aggression, witnessed by others, damages them. "
                "Your calm, witnessed by others, builds your credibility. "
                "Do not match their energy. Let contrast tell the story."
            )
        }


def main():
    import sys

    print("Tactical Response Generator")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python tactical_response.py public_attack  - Response to public attack")
        print("  python tactical_response.py gaslighting    - Response to gaslighting")
        print("  python tactical_response.py surveillance   - Response to surveillance")
        print("  python tactical_response.py isolation      - Response to isolation attempt")
        print("  python tactical_response.py zelensky       - Feb 28 2025 analysis")
        return

    cmd = sys.argv[1].lower()
    tactical = TacticalResponse()

    if cmd == "zelensky":
        result = tactical.zelensky_analysis()
        print(json.dumps(result, indent=2))
    elif cmd in ["public_attack", "gaslighting", "surveillance", "isolation"]:
        result = tactical.generate_action_plan(cmd)
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
