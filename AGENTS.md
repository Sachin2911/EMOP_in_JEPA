# Agent notes

## TLDR

This Honours project asks whether **selection pressure can substitute for reward engineering** in safe RL. A frozen JEPA world model (LeWM) imagines plans in latent space; a multi-objective evolutionary planner (NSGA-II) trades off task performance against structural safety signals from the model itself, returning a Pareto front so the safety-performance operating point is chosen at deployment rather than fixed before training.

## Project snapshot

- **Title:** Evolutionary Multi-Objective Planning in JEPA (EMOP in JEPA)
- **Slogan:** Selection pressure as an alternative to hand-crafted reward penalties
- **Student:** Sachin Mohan (2699183), BSc Honours CS, University of the Witwatersrand
- **Supervisor:** Geraud Nangue Tasse
- **Guiding move:** swap *tuning* (penalty weights, hand-crafted costs) for *search* (Pareto front over imagined plans)

### Method (four phases)

1. Reproduce LeWM on Reacher and Push-T; freeze the world model.
2. Replace CEM with NSGA-II (single-objective first, then multi-objective Pareto plans).
3. Add structural safety objectives: prediction surprise, latent energy/jerk, small learned probes (not a hand-crafted cost).
4. Evaluate against baselines; optional later: value bootstrapping, MAP-Elites on trajectory embeddings.

### Evaluation

- **Primary envs:** Reacher, Push-T. OGBench-Cube only if schedule allows.
- **Baselines:** vanilla CEM, penalty-tuned CEM, CPO / Lagrangian PPO, ROSARL.
- **Metrics:** hypervolume (HV), inverted generational distance (IGD), task success; violation-of-expectation study for surprise as a safety signal.

## Docs map

| Path | Role |
|------|------|
| `docs/ideation/` | Current distilled direction (living LaTeX / `ID.pdf`). Prefer this for ongoing writing. |
| `docs/researchProp/` | Full research proposal. Frozen content: `submitted/RP.pdf`. Living `latex/main.tex` may be a shell. |
| `docs/AB/` | Annotated bibliography. Frozen: `submitted/AB.pdf`. See `whiteBoard.md` for the 7-paper list. |
| `docs/litReview/` | Literature review. Frozen: `submitted/LR.pdf`. Older framing (EA / LLM alignment); do not treat as current method. |
| `docs/papers/geraudsPapers/` | Supervisor-suggested papers + `.md` dumps (MAP-Elites, DQD-RL, Safety-Gymnasium, ROSARL). |
| `docs/papers/myPapers/` | Student-chosen papers (LeWM, HWM, etc.). |
| `docs/projectPresentation/`, `docs/projectReport/` | Placeholders for later deliverables. |
| `readme.md` | Short project pitch; still reflects an earlier “Safe AI via Evolutionary Algorithms” framing. |

## Doc authority

When sources conflict, follow this order:

1. `docs/ideation/` (living direction)
2. `docs/researchProp/submitted/RP.pdf` (submitted JEPA + EMOP plan)
3. Everything else (`docs/litReview/`, early `readme.md`, AB framing)

Do not let the older LLM-alignment / CoEvoRL story override the JEPA latent-planning + NSGA-II plan.

## Glossary

- **EMOP:** Evolutionary Multi-Objective Planning
- **JEPA:** Joint-Embedding Predictive Architecture (predict in embedding space, not pixels)
- **LeWM:** Le World Model; JEPA substrate used as the frozen planner world model
- **CEM:** Cross-Entropy Method; LeWM’s default single-objective planner (baseline to replace)
- **NSGA-II:** Multi-objective evolutionary algorithm used for planning over action sequences
- **Structural safety signals:** Surprise (prediction error / OOD), latent energy and jerk (smoothness), small probes; not a hand-crafted cost
- **MPC:** Model predictive control (execute first actions of a plan, then replan)
- **ROSARL:** Reward-Only Safe RL (supervisor work; Minmax penalty; scalar baseline, not Pareto)
- **MAP-Elites / QD:** Quality-diversity illumination of behaviour space; optional extension
- **HV / IGD:** Hypervolume and inverted generational distance (Pareto-front metrics)

## Agent must-know

- Current thesis is **JEPA latent planning + NSGA-II Pareto safety**, not the lit review’s LLM/CoEvoRL story.
- Prefer **ideation + submitted RP** over AB, LR, or `readme.md` when they conflict.
- World model is **frozen LeWM**; novelty is the planner and structural safety objectives.
- Safety is a **separate objective on the Pareto front**, not a tuned λ penalty in a scalar reward.
- Primary envs are **Reacher** and **Push-T**; match CEM planning success before multi-objective work.
- Must compare to **penalty-tuned CEM, constrained RL, and ROSARL**.
- Follow the writing and PDF rules below.

## No em dashes

Never use em dashes in project writing (LaTeX `---`, Unicode `—`, or pasted en/em dash characters used as clause breaks). Prefer commas, parentheses, colons, or a full stop. For compound modifiers such as safety-performance, use a plain hyphen (`-`), not `--` or `–`. When editing existing docs, remove any em dashes you find rather than leaving them.

## Compress paper PDFs before committing

Papers under `docs/papers/` often ship with high-resolution embedded figures and can be tens of megabytes each. After adding or replacing any PDF in that tree, compress it with Ghostscript `/ebook` (downsamples images ~150 DPI; does **not** remove images or text).

```bash
# Compress one paper in place (only replace if smaller)
in="docs/papers/.../Paper.pdf"
tmp="${in}.tmp.pdf"
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
  -dNOPAUSE -dQUIET -dBATCH \
  -sOutputFile="$tmp" "$in"
# if tmp is smaller than in: mv "$tmp" "$in"; else rm "$tmp"
```

Batch all papers:

```bash
find docs/papers -name '*.pdf' -print0 | while IFS= read -r -d '' f; do
  tmp="${f}.tmp.pdf"
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
    -dNOPAUSE -dQUIET -dBATCH -sOutputFile="$tmp" "$f"
  if [ -s "$tmp" ] && [ "$(stat -c%s "$tmp")" -lt "$(stat -c%s "$f")" ]; then
    mv "$tmp" "$f"
  else
    rm -f "$tmp"
  fi
done
```

Quality presets if `/ebook` figures look too soft: `/printer` (~300 DPI, larger) or `/screen` (~72 DPI, smaller). Prefer `/ebook` by default.
