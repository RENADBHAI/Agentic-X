# Agentic X — Shared Interfaces (v0.1 draft)

This document defines **integration contracts** so teammates can build notebooks 01–07 in parallel. It is a **proposal**, not an implemented interface or observed result. Changes require agreement and a PR.

## Repository modules

- `core/schemas.py`: typed `CaseContext`, `Option`, `ACLMessage`, `AgentEvaluation`, `RunResult` structures.
- `core/data_loader.py`: load scenarios and exclude QA-only labels from agent-visible content.
- `agents/creative.py`, `agents/operations.py`, `agents/finance.py`, `agents/safety.py`: independent evaluators.
- `core/communication.py`: ACL-like message delivery and event log.
- `core/negotiation.py`: negotiation, consensus/failed resolution, and escalation.
- `core/runner.py`: unified `run_scenario` entrypoint.
- `app.py`: Streamlit UI.

## CaseContext (agent-visible input)

```json
{
  "case_id": "SCR-001",
  "scenario": "Screen Failure",
  "incident": "Event screen stopped working",
  "budget_sar": 5000,
  "time_left_min": 30,
  "severity": "high",
  "backup_available": true,
  "crew_count_available": 3,
  "venue_access": true,
  "required_quality_min": 70,
  "options": [
    {
      "option_id": "SCR-001-O1",
      "option_name": "Use backup screen",
      "cost_sar": 2000,
      "duration_min": 15,
      "quality_score": 80,
      "crew_required": 2,
      "risk_level": "low"
    }
  ]
}
```

**Example only:** the sample values above are illustrative and not a specific extracted workbook record.

- Fields must be mapped and validated from the actual workbook. All available agent-observable constraints (permit, supplier, mitigation evidence, actual incident details and risk estimates) may also be passed explicitly.
- **Do not send QA-only labels to the LLM or agent evaluation code:** `addresses_incident`, `projected_overrun_after_sar`, reference feasibility labels, `Run Results` and `QA Summary`. Note: the finance agent can compute budget status from disclosed cost, projected spend and estimated savings; Safety can check observed hazard/mitigation descriptions.
- For the Budget Overrun scenario, send **observable raw figures** such as `initial_budget_sar`, `committed_spend_sar`, `unplanned_charge_sar`, `projected_total_spend_sar`, and `gross_savings_sar`. Independent validators must recompute net savings and overrun.

## AgentEvaluation (draft)

```json
{
  "case_id": "SCR-001",
  "agent_id": "creative",
  "candidate_option_id": "SCR-001-O1",
  "acceptable": true,
  "preference_score": 0.82,
  "reason": "Adequate quality within the deadline",
  "proposed_option_id": "SCR-001-O1",
  "tool_results": [],
  "trace_id": null
}
```

- All fields are structured; the LLM must not invent option IDs. Scores must have documented meaning and ranges.
- Final hard constraints are validated in deterministic Python, never delegated solely to LLM output.

## ACLMessage (draft)

```json
{
  "message_id": "m-001",
  "conversation_id": "run-001",
  "case_id": "SCR-001",
  "round": 1,
  "sender": "creative",
  "receiver": "finance",
  "performative": "PROPOSE",
  "content": {"option_id": "SCR-001-O1", "reason": "Good audience quality"},
  "in_reply_to": null,
  "ontology": "event-crisis",
  "timestamp": "ISO-8601 timestamp"
}
```

Valid performatives: `REQUEST`, `INFORM`, `CFP`, `PROPOSE`, `ACCEPT`, `REFUSE`.

## RunResult (draft; UI-facing)

```json
{
  "run_id": "run-001",
  "case_id": "SCR-001",
  "status": "AGREED",
  "selected_option_id": "SCR-001-O1",
  "reason": "Approved by all agents and hard-constraint checks",
  "rounds": 2,
  "agent_evaluations": [],
  "messages": [],
  "constraint_checks": {},
  "events": [],
  "trace_id": null,
  "is_mock": false
}
```

- Status enum: `AGREED`, `ESCALATED`, `FAILED`; `selected_option_id` must be null if no safe option is agreed.
- Intermediate events: `agent_status`, `acl_message`, `candidate_evaluation`, `decision`, `error`.
- Mock results **must** set `is_mock=true` and must not be presented as completed simulation metrics.

## Integration entrypoint

```python
def run_scenario(case_id: str, engine, overrides: dict | None = None):
    """Return RunResult and emit structured events; implementation pending."""
    ...
```

A student building notebook 05 or 07 can supply a mock `engine` implementing the same contract; notebook 04 later supplies the production engine.

## Architecture decisions

1. Python-only project, Streamlit UI, Google Colab for development and GitHub for version control.
2. Four agents: Creative (LLM), Operations (LLM-assisted), Finance (deterministic), Safety (deterministic veto). LLM agents must use meaningful tool/reasoning steps, not only role labels.
3. LangChain for LLM agent integration, LangSmith for trace and evaluation.
4. LangGraph and CrewAI are **optional** and not necessary to satisfy this plan.
5. Independent concurrent assessments are appropriate, while negotiation rounds remain causally ordered.
6. Preserve API credentials in environment/Colab secrets, never GitHub.
7. Three demo incidents: Screen Failure, Budget Overrun, Safety Conflict; demonstrate actual conflict or agent failure.
8. 150 synthetic cases are testing fixtures, not model training data. Do not claim any test performance before execution.

## Team workflow

Each contributor works on a separate `feature/*` branch, saves notebook commits into that branch from Colab, and sends a Pull Request after tests. Avoid parallel edits to the same notebook. Document schema edits before merging.
