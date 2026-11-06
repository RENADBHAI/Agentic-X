# Agentic X

**Agentic X** is a Python multi-agent decision-support simulation for event crisis management at the fictional **Studio 67**.

Four autonomous agents — **Creative**, **Finance**, **Operations**, and **Safety** — evaluate alternatives, exchange ACL-like messages, negotiate, and propose an acceptable solution or escalate when no feasible solution exists.

## Project notebooks

| # | Notebook | Purpose |
|---|---|---|
| 01 | Environment & Data | Read and validate synthetic scenarios and alternatives |
| 02 | Agent Development | Implement four agents, behavior, and PEAS analysis |
| 03 | Agent Communication | Implement ACL-like message structures and delivery |
| 04 | Negotiation Engine | Implement proposal evaluation and negotiation rounds |
| 05 | Scenario Execution | Run screen failure, budget overrun, and safety conflict |
| 06 | Testing & Evaluation | Test scenario coverage, compliance, and performance |
| 07 | Integration & Export | Expose the Python engine to a Streamlit interface |

## Repository layout

- `notebooks/`: executable Colab notebooks (starter outlines at present).
- `agents/`: Python agent implementations (to be added).
- `core/`: environment, messaging, and negotiation engine (to be added).
- `data/`: synthetic testing workbook (to be added).
- `tests/`: automated tests (to be added).
- `app.py`: Streamlit UI (to be added).

## Colab workflow

1. Open a notebook from GitHub using Google Colab's GitHub tab, or replace `github.com` with `colab.research.google.com/github` in its GitHub URL.
2. Edit and run the notebook in Colab.
3. Select **File → Save a copy in GitHub**; select `RENADBHAI/Agentic-X`, the intended branch, and the same notebook path.
4. Check the resulting commit in GitHub.

**Important:** Notebooks contain updated, detailed starter plans and a small runnable setup check, not the completed MAS implementation. No LLM or evaluation results have been generated yet. All backend logic will be stored in reusable Python modules, not duplicated in notebooks.

## Agreed development architecture

- **AI:** Creative is LLM-powered; Operations uses LLM assistance and deterministic feasibility tools. Finance and Safety use reliable deterministic checks, with Safety enforcing a non-overridable veto.
- **Frameworks:** Python + LangChain for AI integration, **LangSmith tracing and evaluation**; LangGraph and CrewAI are optional.
- **Coordination:** ACL-like messages with actual negotiation rounds; concurrent independent initial evaluations where appropriate.
- **Testing:** 150 synthetic cases / 450 options for evaluation, not training. Three mandatory demo scenarios and an agent-conflict/failure demonstration.
- **Team parallelism:** See [`docs/INTERFACES.md`](docs/INTERFACES.md) for shared schemas, module boundaries and branch/PR workflow. Notebooks 04–07 may start early with clearly marked mock engines.
- **UI:** Python Streamlit with live agent state, genuine ACL message log, controls and final decision.

The validated Excel workbook is **not yet uploaded to this repository**. Never commit keys; use Colab secrets/environment variables.

## Course

CAI461 — Agent-Based Systems, Project 2.
