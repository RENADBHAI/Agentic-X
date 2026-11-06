"""Explicit MOCK engine for parallel development of notebooks 05, 06, 07.

This is NOT the real AI/negotiation backend. It needs no API keys.
Never use these fixture decisions or messages as real Agentic X evaluation results.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4

AGENTS = ("creative", "finance", "operations", "safety")
MOCK_CASES = {
    "SCR-DEMO": {
        "scenario": "Screen Failure",
        "incident": "Main event screen stopped working",
        "budget_sar": 5000,
        "time_left_min": 30,
        "crew_count_available": 3,
        "backup_available": True,
        "options": [
            {"option_id": "SCR-D-O1", "option_name": "Use backup screen", "cost_sar": 2000, "duration_min": 15, "crew_required": 2, "needs_backup": True, "safety_ok": True, "quality_score": 80},
            {"option_id": "SCR-D-O2", "option_name": "Rent replacement display", "cost_sar": 4000, "duration_min": 25, "crew_required": 2, "needs_backup": False, "safety_ok": True, "quality_score": 90},
            {"option_id": "SCR-D-O3", "option_name": "Install premium display", "cost_sar": 8000, "duration_min": 60, "crew_required": 3, "needs_backup": False, "safety_ok": True, "quality_score": 98},
        ],
    },
    "BDG-DEMO": {
        "scenario": "Budget Overrun",
        "incident": "Projected event spending exceeds approved budget",
        "budget_sar": 3000,
        "initial_budget_sar": 20000,
        "projected_total_spend_sar": 22000,
        "time_left_min": 60,
        "crew_count_available": 4,
        "backup_available": False,
        "options": [
            {"option_id": "BDG-D-O1", "option_name": "Simplify decoration package", "cost_sar": 500, "gross_savings_sar": 3000, "duration_min": 30, "crew_required": 2, "needs_backup": False, "safety_ok": True, "quality_score": 74},
            {"option_id": "BDG-D-O2", "option_name": "Switch to standard AV", "cost_sar": 1100, "gross_savings_sar": 3600, "duration_min": 40, "crew_required": 3, "needs_backup": False, "safety_ok": True, "quality_score": 84},
            {"option_id": "BDG-D-O3", "option_name": "Keep premium package", "cost_sar": 0, "gross_savings_sar": 0, "duration_min": 0, "crew_required": 0, "needs_backup": False, "safety_ok": True, "quality_score": 96},
        ],
    },
    "SFT-DEMO": {
        "scenario": "Safety Conflict",
        "incident": "Emergency exit blocked by stage equipment",
        "budget_sar": 3000,
        "time_left_min": 40,
        "crew_count_available": 3,
        "backup_available": False,
        "options": [
            {"option_id": "SFT-D-O1", "option_name": "Leave layout unchanged", "cost_sar": 0, "duration_min": 0, "crew_required": 0, "needs_backup": False, "safety_ok": False, "quality_score": 95},
            {"option_id": "SFT-D-O2", "option_name": "Relocate equipment to clear exit", "cost_sar": 800, "duration_min": 20, "crew_required": 2, "needs_backup": False, "safety_ok": True, "quality_score": 82},
            {"option_id": "SFT-D-O3", "option_name": "Rebuild stage layout", "cost_sar": 2700, "duration_min": 55, "crew_required": 3, "needs_backup": False, "safety_ok": True, "quality_score": 92},
        ],
    },
}


def get_mock_case(case_id: str) -> dict:
    """Return a detached fixture; never mutate global examples."""
    if case_id not in MOCK_CASES:
        raise ValueError(f"Unknown MOCK case: {case_id}; choose {list(MOCK_CASES)}")
    case = deepcopy(MOCK_CASES[case_id])
    case["case_id"] = case_id
    return case


def _violations(case: dict, option: dict) -> list[str]:
    reasons = []
    if option["cost_sar"] > case["budget_sar"]:
        reasons.append("insufficient remaining action budget")
    if option["duration_min"] > case["time_left_min"]:
        reasons.append("deadline exceeded")
    if option["crew_required"] > case["crew_count_available"]:
        reasons.append("insufficient crew")
    if option["needs_backup"] and not case["backup_available"]:
        reasons.append("backup unavailable")
    if not option["safety_ok"]:
        reasons.append("safety requirement failed")
    if case["scenario"] == "Budget Overrun":
        after = case["projected_total_spend_sar"] + option["cost_sar"] - option.get("gross_savings_sar", 0)
        if after > case["initial_budget_sar"]:
            reasons.append("projected total remains above approved budget")
    return reasons


class MockEngine:
    """Interface-compatible fixture engine. Not an AI agent or negotiation system."""

    def run(self, case_id: str, overrides: dict | None = None) -> dict:
        case = get_mock_case(case_id)
        allowed = {"budget_sar", "time_left_min", "crew_count_available", "backup_available"}
        overrides = overrides or {}
        unknown = set(overrides) - allowed
        if unknown:
            raise ValueError(f"Unsupported override(s): {sorted(unknown)}")
        for field, value in overrides.items():
            if field == "backup_available":
                if not isinstance(value, bool):
                    raise ValueError("backup_available must be bool")
            elif not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"{field} must be a nonnegative integer")
            case[field] = value

        evaluations = []
        for option in case["options"]:
            reasons = _violations(case, option)
            evaluations.append({
                "option_id": option["option_id"],
                "acceptable": not reasons,
                "violations": reasons,
            })

        feasible = [o for o, ev in zip(case["options"], evaluations) if ev["acceptable"]]
        # Deterministic selection FOR MOCK PURPOSES ONLY; not real agent reasoning.
        chosen = max(feasible, key=lambda o: (o["quality_score"], -o["cost_sar"])) if feasible else None
        run_id = "mock-" + uuid4().hex[:10]
        now = datetime.now(timezone.utc).isoformat()
        messages = []
        def message(sender, receiver, performative, content, round_no=1):
            messages.append({
                "message_id": f"{run_id}-m{len(messages)+1}",
                "conversation_id": run_id,
                "case_id": case_id,
                "round": round_no,
                "sender": sender,
                "receiver": receiver,
                "performative": performative,
                "content": content,
                "in_reply_to": None,
                "ontology": "event-crisis",
                "timestamp": now,
                "is_mock": True,
            })
        message("operations", "creative", "CFP", {"request": "Review candidate options"})
        for ev in evaluations:
            message("finance", "operations", "INFORM", {"option_id": ev["option_id"], "feasible": ev["acceptable"], "issues": ev["violations"]})
        if chosen is not None:
            message("creative", "safety", "PROPOSE", {"option_id": chosen["option_id"]})
            message("safety", "operations", "ACCEPT", {"option_id": chosen["option_id"]})
            status = "AGREED"
            reason = "MOCK selection among options satisfying simplified checks; not an AI-negotiated decision."
        else:
            message("safety", "operations", "REFUSE", {"reason": "No option passes mock checks"})
            status = "ESCALATED"
            reason = "MOCK escalation: no feasible options under supplied constraints."
        events = [
            {"type": "agent_status", "agent_id": agent, "status": "MOCK_COMPLETE", "is_mock": True}
            for agent in AGENTS
        ] + [{"type": "acl_message", "message": m, "is_mock": True} for m in messages] + [
            {"type": "decision", "status": status, "selected_option_id": chosen["option_id"] if chosen else None, "is_mock": True}
        ]
        return {
            "run_id": run_id,
            "case_id": case_id,
            "status": status,
            "selected_option_id": chosen["option_id"] if chosen else None,
            "reason": reason,
            "rounds": 1,
            "agent_evaluations": [],
            "messages": messages,
            "constraint_checks": {ev["option_id"]: ev for ev in evaluations},
            "events": events,
            "trace_id": None,
            "is_mock": True,
        }


def run_scenario(case_id: str, engine, overrides: dict | None = None) -> dict:
    """Shared adapter for notebooks and the UI; real engine should implement .run."""
    result = engine.run(case_id, overrides=overrides)
    required = {"run_id", "case_id", "status", "selected_option_id", "messages", "events", "is_mock"}
    missing = required - set(result)
    if missing:
        raise ValueError(f"Engine result missing keys: {sorted(missing)}")
    return result
