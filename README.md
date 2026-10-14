# DE Learning

An interactive study hub for **data engineering interview preparation**, aimed at Lead Data Engineer and Data Architect roles.

It's a small static website: plain HTML, CSS and JavaScript, with no build step and no backend. It has two parts:

- **Topic tracker** (`index.html`): 75 interview topics in seven areas. Readers tick topics off as they learn them, and progress is saved in their own browser.
- **Learning paths**: interactive pages that teach one area in depth, with diagrams, worked examples, failure scenarios, debug flows and ready-to-use interview answers.

## Why this repo exists

The hub started as a personal prep tool and is now open to friends for review and contributions. Git keeps a full history, so every change is visible, reviewable and reversible.

## What's inside

| Path | What it is |
| --- | --- |
| `index.html` | Hub: topic tracker and list of learning paths |
| `spark-architecture.html` | Spark Core module 1: driver, executors, jobs/stages/tasks, memory model, dynamic allocation |
| `spark-execution.html` | Spark Core module 2: spark-submit flow, lazy evaluation, narrow vs wide, stages |
| `spark-optimizer.html` | Spark Core module 3: Catalyst, pushdown and pruning, explain(), joins, AQE, UDFs |
| `spark-tuning.html` | Spark Core module 4: debug flow, six failure scenarios, shuffle, partition and executor sizing |
| `styles.css` | Shared design tokens and components (light and dark themes) |
| `scripts/check.py` | Automated checks run on every pull request |
| `AGENTS.md` | Conventions for AI coding agents (and humans) editing the site |
| `CONTRIBUTING.md` | How to propose changes |

## Topic areas and status

| Area | Topics | Learning path |
| --- | --- | --- |
| Spark core | 24 | Available (4 modules) |
| Structured Streaming | 10 | Planned next |
| Delta Lake & Databricks | 16 | Planned |
| Iceberg & table formats | 5 | Planned |
| Data modelling & SQL | 6 | Planned |
| Pipelines, orchestration & quality | 10 | Planned |
| Governance & cloud | 4 | Planned |

## Viewing it

- **Online:** via GitHub Pages, once enabled (Settings → Pages → deploy from `main`, root folder).
- **Locally:** open `index.html` in a browser. To make cross-page links behave exactly as they do online, serve the folder:

  ```bash
  python3 -m http.server 8000
  # then open http://localhost:8000
  ```

## Each module page follows the same learning flow

1. **Concept**: what it is and why it matters, in plain language
2. **Picture**: a diagram of the mechanism
3. **Worked example**: real code, plans or numbers
4. **What breaks**: traps, failure scenarios and how to debug them
5. **Say it in an interview**: a short answer you can give out loud
6. **Check yourself**: questions with answers hidden until clicked

## Contributing

Corrections, clearer explanations, new scenarios and new learning paths are all welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. If you're using an AI coding agent, point it at [AGENTS.md](AGENTS.md) first.

All changes go through a pull request into `main` and are reviewed by the maintainer.

## Maintainer

Saksham Gupta
