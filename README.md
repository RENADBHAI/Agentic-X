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

**Important:** Notebooks here are starter outlines; they are not implemented or tested yet. All backend logic will be stored in reusable Python modules, not duplicated in notebooks.

## Course

CAI461 — Agent-Based Systems, Project 2.
